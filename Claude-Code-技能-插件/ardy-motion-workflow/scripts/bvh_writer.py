"""BVH writer using centimeter units; only root translation is Blender-safe."""
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
