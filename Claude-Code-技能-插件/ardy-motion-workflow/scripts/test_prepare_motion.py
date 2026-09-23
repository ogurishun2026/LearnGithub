import unittest
import numpy as np
from prepare_motion import validate_motion, motion_root


class PrepareMotionTests(unittest.TestCase):
    def data(self):
        return dict(posed_joints=np.zeros((6,27,3)), global_rot_mats=np.tile(np.eye(3),(6,27,1,1)),
                    global_root_heading=np.tile([1.,0.],(6,1)), fps=np.array(20.))

    def test_rejects_other_skeletons_and_unclosed_loop(self):
        data = self.data()
        data['posed_joints'] = np.zeros((6,30,3))
        with self.assertRaises(ValueError):
            validate_motion(data, loop=False)
        data = self.data()
        data['posed_joints'][-1,0,0] = 1
        with self.assertRaises(ValueError):
            validate_motion(data, loop=True)

    def test_fixed_root_ignores_heading_but_planar_preserves_it(self):
        data = self.data()
        data['posed_joints'][:,0] = [2,1,3]
        data['global_root_heading'][:] = [0,1]
        positions, rotations = motion_root(data,'fixed')
        np.testing.assert_array_equal(positions,0)
        np.testing.assert_allclose(rotations,np.tile(np.eye(3),(6,1,1)))
        positions, rotations = motion_root(data,'planar')
        np.testing.assert_allclose(positions,np.tile([2,0,3],(6,1)))
        np.testing.assert_allclose(rotations[0]@[0,0,1],[1,0,0],atol=1e-10)

    def test_rejects_nan_and_nonrotation_matrix(self):
        data = self.data()
        data['fps'] = np.array(float('nan'))
        with self.assertRaises(ValueError):
            validate_motion(data,loop=False)
        data = self.data()
        data['global_rot_mats'][0,0,0,0] = 2
        with self.assertRaises(ValueError):
            validate_motion(data,loop=False)


if __name__ == '__main__':
    unittest.main()
