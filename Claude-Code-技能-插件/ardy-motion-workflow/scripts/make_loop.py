"""Loop a selected ARDY guard segment, retain bone lengths, and plant both feet."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.spatial.transform import Rotation
from ardy.skeleton import CoreSkeleton27
from loop_math import periodic_values, periodic_rotations, rotation_between, solve_knee
from prepare_motion import validate_motion


def fk(local, root, rest, parents):
    positions, global_rots = np.empty((len(rest), 3)), np.empty_like(local)
    for i, parent in enumerate(parents):
        if parent < 0:
            positions[i], global_rots[i] = root, local[i]
        else:
            positions[i] = positions[parent] + global_rots[parent] @ (rest[i] - rest[parent])
            global_rots[i] = global_rots[parent] @ local[i]
    return positions, global_rots


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('motion', type=Path)
    parser.add_argument('--start', type=int, required=True, help='First source frame, zero based')
    parser.add_argument('--stop', type=int, required=True, help='Exclusive end source frame')
    parser.add_argument('--frames', type=int, default=80, help='Unique frames, plus one identical endpoint')
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise ValueError('Use a new loop output path; existing data is preserved')
    source = np.load(args.motion, allow_pickle=False)
    validate_motion(source, loop=False)
    skeleton = CoreSkeleton27()
    names, parents = skeleton.bone_order_names, skeleton.joint_parents.tolist()
    rest = skeleton.neutral_joints.numpy().astype(float)
    selected = source['local_rot_mats'][args.start:args.stop]
    if not 0 <= args.start < args.stop <= len(source['posed_joints']):
        raise ValueError('Invalid source segment')
    frames = args.frames
    local = np.stack([periodic_rotations(selected[:, j], frames) for j in range(27)], axis=1)
    source_root = source['posed_joints'][args.start:args.stop, 0].astype(float)
    origin = np.mean(source_root, axis=0) * np.array([1., 0., 1.])
    root = periodic_values(source_root - origin, frames)
    targets = {}
    for side in ('Left', 'Right'):
        ids = [names.index(side + s) for s in ('UpLeg', 'Leg', 'Foot', 'ToeBase')]
        thigh, knee, foot, toe = ids
        targets[side] = {
            'indices': ids,
            'position': np.median(source['posed_joints'][args.start:args.stop, foot], axis=0) - origin,
            'rotation': Rotation.from_matrix(source['global_rot_mats'][args.start:args.stop, foot]).mean().as_matrix(),
            'toe_rotation': Rotation.from_matrix(selected[:, toe]).mean().as_matrix(),
            'lengths': [np.linalg.norm(rest[knee]-rest[thigh]), np.linalg.norm(rest[foot]-rest[knee])],
        }
    def bake_planted():
        positions, global_rots = [], []
        for f in range(frames+1):
            p, g = fk(local[f], root[f], rest, parents)
            for side, target in targets.items():
                thigh, knee, foot, toe = target['indices']
                hip, ankle = p[thigh], target['position']
                pole = p[knee] - hip
                k = solve_knee(hip, ankle, pole, *target['lengths'])
                thigh_rot = rotation_between(p[knee]-hip, k-hip) @ g[thigh]
                shin_rot = rotation_between(p[foot]-p[knee], ankle-k) @ g[knee]
                local[f, thigh] = g[parents[thigh]].T @ thigh_rot
                local[f, knee] = thigh_rot.T @ shin_rot
                local[f, foot] = shin_rot.T @ target['rotation']
                local[f, toe] = target['toe_rotation']
                p, g = fk(local[f], root[f], rest, parents)
            positions.append(p)
            global_rots.append(g)
        return np.array(positions), np.array(global_rots)

    positions, global_rots = bake_planted()
    # Correct contact using the actual four-weight reference skin, not joint heights.
    skin = np.load(Path(skeleton.folder)/'skin_standard.npz', allow_pickle=False)
    weights = skin['lbs_weights'].copy()
    if weights.shape[1] > 4:
        weights[np.arange(len(weights))[:, None], np.argsort(weights, axis=1)[:, :-4]] = 0
    weights /= weights.sum(axis=1, keepdims=True)
    transforms = np.tile(np.eye(4), (27,1,1))
    transforms[:,:3,:3], transforms[:,:3,3] = global_rots[0], positions[0]
    affine = transforms @ np.linalg.inv(skin['bind_rig_transform'])
    vertices = skin['bind_vertices']
    homogeneous = np.concatenate([vertices, np.ones((len(vertices),1))], axis=1)
    influences = np.einsum('vwij,vj->vwi', affine[skin['lbs_indices'], :3, :], homogeneous)
    posed_skin = np.sum(influences*weights[:,:,None], axis=1)
    sole_corrections = {}
    for side in ('Left','Right'):
        ids = (vertices[:,1] < .02) & (vertices[:,0] > 0 if side=='Left' else vertices[:,0] < 0)
        correction = .0001 - float(posed_skin[ids,1].min())
        targets[side]['position'][1] += correction
        sole_corrections[side] = correction
    positions, global_rots = bake_planted()
    positions[-1], global_rots[-1], local[-1] = positions[0], global_rots[0], local[0]
    foot_ids = [names.index(side+s) for side in ('Left', 'Right') for s in ('Foot', 'ToeBase')]
    floor_offset = float(np.min(positions[:, [names.index('LeftToeBase'), names.index('RightToeBase')], 1]))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(args.out, posed_joints=positions, local_rot_mats=local,
                        global_rot_mats=global_rots, root_positions=root,
                        global_root_heading=np.tile([1., 0.], (frames+1, 1)),
                        fps=source['fps'], text=source['text'])
    feet_drift = float(np.max(np.linalg.norm(positions[:, foot_ids] - positions[0, foot_ids], axis=-1)))
    report = {
        'source': args.motion.name, 'source_sha256': hashlib.sha256(args.motion.read_bytes()).hexdigest(),
        'source_frames_zero_based': [args.start, args.stop-1],
        'method': 'Two-harmonic periodic fit of local rotations about SO(3) means and pelvis positions; analytic leg IK fixes ankles and foot orientation; fixed independent root',
        'frames_unique': frames, 'frames_with_endpoint': frames+1, 'fps': float(source['fps']),
        'cycle_seconds': frames / float(source['fps']),
        'loop_endpoint_joint_error_m': float(np.linalg.norm(positions[-1]-positions[0], axis=-1).max()),
        'loop_endpoint_rotation_error': float(np.max(np.abs(global_rots[-1]-global_rots[0]))),
        'foot_joint_drift_m': feet_drift,
        'min_toe_joint_height_m': floor_offset,
        'sole_ground_correction_m': sole_corrections,
        'root_motion': 'Independent root fixed; natural pelvis sway retained',
        'pelvis_excursion_m': np.ptp(root[:-1], axis=0).tolist(),
        'visual_status': 'Pending render review',
    }
    if feet_drift > 1e-6:
        raise RuntimeError(f'Foot lock failed: {feet_drift}')
    report_path = args.out.with_suffix('.json')
    report_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
