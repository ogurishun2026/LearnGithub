"""Export the Core27 sample in centimeters, with a separate planar motion root."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.spatial.transform import Rotation


def write_bvh(path, names, parents, rest, positions, global_rotations, fps, root_translation_only=False):
    rest, positions, global_rotations = map(np.asarray, (rest, positions, global_rotations))
    if not all(np.isfinite(v).all() for v in (rest, positions, global_rotations)) or fps <= 0:
        raise ValueError('Invalid motion')
    children = {i: [] for i in range(len(names))}
    for i, parent in enumerate(parents):
        if parent >= 0:
            children[parent].append(i)
    lines, order = ['HIERARCHY'], []

    def joint(i, depth):
        indent = '  ' * depth
        order.append(i)
        lines.extend([f'{indent}{"ROOT" if parents[i] < 0 else "JOINT"} {names[i]}', indent + '{'])
        offset = rest[i] if parents[i] < 0 else rest[i] - rest[parents[i]]
        lines.append(indent + '  OFFSET ' + ' '.join(f'{v * 100:.9f}' for v in offset))
        lines.append(indent + ('  CHANNELS 6 Xposition Yposition Zposition Zrotation Yrotation Xrotation'
                              if i == 0 or not root_translation_only else '  CHANNELS 3 Zrotation Yrotation Xrotation'))
        for child in children[i]:
            joint(child, depth + 1)
        if not children[i]:
            lines.extend([indent + '  End Site', indent + '  {', indent + '    OFFSET 0.0 5.0 0.0', indent + '  }'])
        lines.append(indent + '}')

    joint(0, 0)
    lines.extend(['MOTION', f'Frames: {len(positions)}', f'Frame Time: {1 / fps:.12f}'])
    for frame in range(len(positions)):
        values = []
        for i in order:
            p = parents[i]
            if p < 0:
                translation = positions[frame, i] - rest[i]
                rotation = global_rotations[frame, i]
            else:
                translation = global_rotations[frame, p].T @ (positions[frame, i] - positions[frame, p]) - (rest[i] - rest[p])
                rotation = global_rotations[frame, p].T @ global_rotations[frame, i]
            if i == 0 or not root_translation_only:
                values.extend(translation * 100)
            elif np.linalg.norm(translation) > 1e-5:
                raise ValueError('Child translations exceed numerical FK noise')
            values.extend(Rotation.from_matrix(rotation).as_euler('ZYX', degrees=True))
        lines.append(' '.join(f'{v:.9f}' for v in values))
    Path(path).write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main():
    from ardy.skeleton import CoreSkeleton27
    parser = argparse.ArgumentParser()
    parser.add_argument('motion', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    data = np.load(args.motion, allow_pickle=False)
    skeleton = CoreSkeleton27()
    skin = np.load(Path(skeleton.folder) / 'skin_standard.npz', allow_pickle=False)
    names = ['root', 'pelvis', *skeleton.bone_order_names[1:]]
    parents = [-1, *[int(p) + 1 for p in skeleton.joint_parents]]
    bind_hips = skin['bind_rig_transform'][0, :3, 3]
    rest = np.concatenate([np.zeros((1, 3)), skeleton.neutral_joints.numpy() + bind_hips])
    positions = data['posed_joints'].astype(float)
    rotations = data['global_rot_mats'].astype(float)
    root_translation = positions[:, 0].copy()
    root_translation[:, 1] = 0
    heading = np.unwrap(np.arctan2(data['global_root_heading'][:, 1], data['global_root_heading'][:, 0]))
    root_rotation = Rotation.from_euler('Y', heading[:, None]).as_matrix()
    world_positions = np.concatenate([root_translation[:, None], positions], axis=1)
    world_rotations = np.concatenate([root_rotation[:, None], rotations], axis=1)
    write_bvh(args.out / 'ARDY_Walk_Core27.bvh', names[1:], skeleton.joint_parents.tolist(),
              skeleton.neutral_joints.numpy(), positions, rotations, float(data['fps']), root_translation_only=True)
    np.savez(args.out / 'source_reference.npz', positions=world_positions, rotations=world_rotations,
             names=np.array(names), parents=np.array(parents), rest=rest, fps=data['fps'],
             **{key: skin[key] for key in skin.files})
    report = {'source_sha256': hashlib.sha256(args.motion.read_bytes()).hexdigest(),
              'frames': len(positions), 'fps': float(data['fps']), 'source_joints': 27, 'export_bones': 28,
              'changes': 'Added root for planar translation/yaw; renamed Hips to pelvis; original world joint positions/rotations preserved',
              'bvh_joints': 27, 'bvh_root': 'pelvis', 'bvh_units': 'centimeters', 'source_up': '+Y', 'blender_up': '+Z',
              'root_displacement_m': float(np.linalg.norm(root_translation[-1] - root_translation[0])),
              'names': names, 'parents': parents}
    (args.out / 'conversion-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
