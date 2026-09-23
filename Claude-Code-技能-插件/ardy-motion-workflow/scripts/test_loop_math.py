"""Check periodic timing, rotation wraparound, and planted-leg geometry."""
import unittest
import numpy as np
from scipy.spatial.transform import Rotation
from loop_math import periodic_values, periodic_rotations, solve_knee


class LoopMathTests(unittest.TestCase):
    def test_keeps_known_periodic_signal_and_duplicate_endpoint(self):
        phase = np.arange(80) * 2 * np.pi / 80
        source = np.stack([2 + .1*np.sin(phase), 1 + .03*np.cos(phase)], axis=1)
        output = periodic_values(source, 80)
        self.assertEqual(output.shape, (81, 2))
        np.testing.assert_allclose(output[:-1], source, atol=1e-8)
        np.testing.assert_allclose(output[0], output[-1], atol=1e-12)

    def test_rotation_crosses_180_without_spinning(self):
        phase = np.arange(80) * 2 * np.pi / 80
        source = Rotation.from_euler('Y', (180 + 7*np.sin(phase))[:, None], degrees=True).as_matrix()
        output = periodic_rotations(source, 80)
        delta = Rotation.from_matrix(output[:-1]).inv() * Rotation.from_matrix(source)
        self.assertLess(float(delta.magnitude().max()), 1e-7)
        np.testing.assert_allclose(output[0], output[-1], atol=1e-12)
        np.testing.assert_allclose(np.linalg.det(output), 1, atol=1e-10)

    def test_knee_preserves_lengths_and_forward_bend(self):
        hip = np.array([.15, .95, 0.])
        ankle = np.array([.20, .10, .15])
        pole = np.array([0., 0., 1.])
        knee = solve_knee(hip, ankle, pole, .46, .47)
        self.assertAlmostEqual(np.linalg.norm(knee-hip), .46, places=10)
        self.assertAlmostEqual(np.linalg.norm(ankle-knee), .47, places=10)
        self.assertGreater(knee[2], ankle[2])


if __name__ == '__main__':
    unittest.main()
