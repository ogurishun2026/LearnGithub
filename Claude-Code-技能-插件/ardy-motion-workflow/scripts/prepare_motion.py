"""Prepare an ARDY Core27 clip and explicit export contract for Blender."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import numpy as np
from scipy.spatial.transform import Rotation
from bvh_writer import write_bvh


def validate_motion(data, loop=False):
    p, r = np.asarray(data['posed_joints']), np.asarray(data['global_rot_mats'])
    fps = float(data['fps'])
    if p.ndim != 3 or p.shape[1:] != (27,3) or len(p) < 2:
        raise ValueError('Only ARDY Core27 motion with at least two frames is supported')
    if r.shape != (len(p),27,3,3) or not np.isfinite(fps) or fps <= 0:
        raise ValueError('Invalid rotation shape or FPS')
    if not np.isfinite(p).all() or not np.isfinite(r).all():
        raise ValueError('Nonfinite joint data')
    if np.max(np.abs(r @ r.swapaxes(-1,-2)-np.eye(3))) > 1e-3 or np.max(np.abs(np.linalg.det(r)-1)) > 1e-3:
        raise ValueError('Invalid rotation matrices')
    if loop and (len(p)<3 or np.max(np.abs(p[-1]-p[0])) > 1e-6 or np.max(np.abs(r[-1]-r[0])) > 1e-5):
        raise ValueError('--loop requires an already closed clip with a duplicate endpoint; it does not create a loop')
    return len(p), fps


def motion_root(data, mode):
    positions = np.asarray(data['posed_joints'], dtype=float)
    n = len(positions)
    if mode == 'fixed':
        return np.zeros((n,3)), np.tile(np.eye(3),(n,1,1))
    if mode != 'planar':
        raise ValueError('Root mode must be fixed or planar')
    heading = np.asarray(data['global_root_heading'])
    if heading.shape != (n,2) or not np.isfinite(heading).all() or np.any(np.linalg.norm(heading,axis=1)<1e-8):
        raise ValueError('Planar root requires finite nonzero [frames,2] heading vectors')
    angle = np.unwrap(np.arctan2(heading[:,1],heading[:,0]))
    root = positions[:,0].copy()
    root[:,1] = 0
    return root, Rotation.from_euler('Y',angle[:,None]).as_matrix()


def main():
    from ardy.skeleton import CoreSkeleton27
    parser = argparse.ArgumentParser()
    parser.add_argument('motion', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--name', required=True, help='ASCII clip/Action name, e.g. CombatIdle_v2')
    parser.add_argument('--root-mode', choices=['fixed','planar'], required=True)
    parser.add_argument('--loop', action='store_true', help='Input includes one verified duplicate endpoint')
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]{0,79}',args.name):
        raise ValueError('Use a simple ASCII clip name')
    with np.load(args.motion, allow_pickle=False) as source:
        data = {k: source[k] for k in source.files}
    n, fps = validate_motion(data, args.loop)
    root_p, root_r = motion_root(data,args.root_mode)
    skeleton = CoreSkeleton27()
    with np.load(Path(skeleton.folder)/'skin_standard.npz',allow_pickle=False) as source:
        skin = {k:source[k] for k in source.files}
    names = ['root','pelvis',*skeleton.bone_order_names[1:]]
    parents = [-1,*[int(p)+1 for p in skeleton.joint_parents]]
    rest = np.concatenate([np.zeros((1,3)),skeleton.neutral_joints.numpy()+skin['bind_rig_transform'][0,:3,3]])
    world_p = np.concatenate([root_p[:,None], data['posed_joints']],axis=1)
    world_r = np.concatenate([root_r[:,None], data['global_rot_mats']],axis=1)
    if args.loop and (np.max(np.abs(world_p[-1]-world_p[0]))>1e-6 or np.max(np.abs(world_r[-1]-world_r[0]))>1e-5):
        raise ValueError('Export root does not close across the loop boundary')
    if args.out.exists() and any(args.out.iterdir()):
        raise ValueError('Use a new empty output directory; existing artifacts are preserved')
    args.out.mkdir(parents=True,exist_ok=True)
    write_bvh(args.out/f'{args.name}.bvh',names[1:],skeleton.joint_parents.tolist(),
              skeleton.neutral_joints.numpy(), data['posed_joints'],data['global_rot_mats'],fps,root_translation_only=True)
    np.savez(args.out/'source_reference.npz',positions=world_p,rotations=world_r,
             names=np.array(names),parents=np.array(parents),rest=rest,fps=fps,**skin)
    contract = {'name':args.name,'root_mode':args.root_mode,'loop':args.loop,'frames':n,'fps':fps,
                'playback_end':n-1 if args.loop else n,'time_span_seconds':(n-1)/fps,
                'source_sha256':hashlib.sha256(args.motion.read_bytes()).hexdigest(),
                'skeleton':'Core27 + independent root; Hips renamed pelvis',
                'root_displacement_m':float(np.linalg.norm(root_p[-1]-root_p[0])),
                'bvh_units':'centimeters','source_up':'+Y','blender_up':'+Z'}
    (args.out/'motion.json').write_text(json.dumps(contract,indent=2),encoding='utf-8')
    shutil.copyfile(Path(__file__).resolve().parent.parent/'assets/LICENSE-ARDY.txt',args.out/'LICENSE-ARDY.txt')
    (args.out/'NOTICE.txt').write_text(
        'Reference skeleton/skin: NVIDIA nv-tlabs/ardy, ardy/assets/skeletons/cskel27/skin_standard.npz.\n'
        'Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.\n'
        'See LICENSE-ARDY.txt (Apache License 2.0). Model weights have separate terms.\n'
        'Modified: coordinate conversion, Hips renamed pelvis, independent root, four-weight pruning and preview scene.\n'
        'Any additional loop/contact processing is documented separately.\n',encoding='utf-8')
    print(json.dumps(contract,indent=2))


if __name__ == '__main__':
    main()
