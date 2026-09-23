import tempfile
import unittest
from pathlib import Path

import numpy as np
from scipy.spatial.transform import Rotation
from ardy.skeleton.bvh import Bvh

from convert_bvh import write_bvh


class BvhConversionTests(unittest.TestCase):
    def test_rotated_parent_and_pelvis_offset_roundtrip(self):
        names = ['root', 'pelvis', 'hand']
        parents = [-1, 0, 1]
        rest = np.array([[0., 0, 0], [0, 1, 0], [1, 1, 0]])
        yaw = Rotation.from_euler('Y', 60, degrees=True).as_matrix()
        hand_rotation = yaw @ Rotation.from_euler('X', 25, degrees=True).as_matrix()
        rotations = np.array([[np.eye(3)] * 3, [yaw, yaw, hand_rotation]])
        positions = np.array([rest, [[2, 0, 3], [2, 1.2, 3], np.array([2, 1.2, 3]) + yaw @ [1, 0, 0]]])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'test.bvh'
            write_bvh(path, names, parents, rest, positions, rotations, 20)
            parsed = Bvh(path.read_text(), backend='np')
            self.assertEqual(parsed.get_joints_names(), names)
            self.assertAlmostEqual(parsed.frame_time, 0.05)
            for frame in range(2):
                world = []
                for index, name in enumerate(names):
                    channels = parsed.joint_channels(name)
                    vals = [float(parsed.frame_joint_channel(frame, name, ch)) for ch in channels]
                    local = np.eye(4)
                    local[:3, 3] = np.array(parsed.joint_offset(name)) / 100
                    for axis, channel in enumerate(['Xposition', 'Yposition', 'Zposition']):
                        if channel in channels:
                            local[axis, 3] += vals[channels.index(channel)] / 100
                    rotation_channels = [ch for ch in channels if ch.endswith('rotation')]
                    local[:3, :3] = Rotation.from_euler(''.join(ch[0] for ch in rotation_channels), [vals[channels.index(ch)] for ch in rotation_channels], degrees=True).as_matrix()
                    world.append(local if index == 0 else world[parents[index]] @ local)
                    np.testing.assert_allclose(world[index][:3, 3], positions[frame, index], atol=1e-7)
                    np.testing.assert_allclose(world[index][:3, :3], rotations[frame, index], atol=1e-7)


if __name__ == '__main__':
    unittest.main()
