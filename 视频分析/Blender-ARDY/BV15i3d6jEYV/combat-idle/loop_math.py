"""Periodic smoothing on Euclidean coordinates and SO(3), plus two-bone IK."""
import numpy as np
from scipy.spatial.transform import Rotation


def periodic_values(values, frames, harmonics=2):
    values = np.asarray(values, dtype=float)
    if len(values) < 2*harmonics + 1 or frames < 4 or not np.isfinite(values).all():
        raise ValueError('Insufficient or nonfinite samples')

    def design(phase):
        return np.stack([np.ones_like(phase), *[f(k*phase) for k in range(1, harmonics+1)
                        for f in (np.sin, np.cos)]], axis=1)

    source = design(np.arange(len(values)) * 2*np.pi / len(values))
    target = design(np.arange(frames+1) * 2*np.pi / frames)
    coefficients = np.linalg.lstsq(source, values.reshape(len(values), -1), rcond=None)[0]
    result = (target @ coefficients).reshape((frames+1, *values.shape[1:]))
    result[-1] = result[0]
    return result


def periodic_rotations(matrices, frames, harmonics=2):
    rotations = Rotation.from_matrix(np.asarray(matrices))
    center = rotations.mean()
    tangent = (center.inv() * rotations).as_rotvec()
    if np.linalg.norm(tangent, axis=1).max() > np.pi*.8:
        raise ValueError('Clip contains too much rotation for an idle tangent fit')
    result = (center * Rotation.from_rotvec(periodic_values(tangent, frames, harmonics))).as_matrix()
    result[-1] = result[0]
    return result


def solve_knee(hip, ankle, pole, thigh_length, shin_length):
    direction = np.asarray(ankle) - hip
    distance = np.linalg.norm(direction)
    if not abs(thigh_length-shin_length)+1e-6 < distance < thigh_length+shin_length-1e-6:
        raise ValueError('Planted ankle is outside reachable leg length')
    direction /= distance
    bend = np.asarray(pole) - direction*np.dot(pole, direction)
    if np.linalg.norm(bend) < 1e-7:
        raise ValueError('Knee pole is parallel to the leg')
    bend /= np.linalg.norm(bend)
    along = (thigh_length**2 - shin_length**2 + distance**2) / (2*distance)
    height = np.sqrt(max(0., thigh_length**2 - along**2))
    return np.asarray(hip) + direction*along + bend*height


def rotation_between(source, target):
    source = np.asarray(source, dtype=float) / np.linalg.norm(source)
    target = np.asarray(target, dtype=float) / np.linalg.norm(target)
    axis = np.cross(source, target)
    sine, cosine = np.linalg.norm(axis), np.clip(np.dot(source, target), -1, 1)
    if sine < 1e-10:
        if cosine > 0:
            return np.eye(3)
        axis = np.cross(source, np.eye(3)[np.argmin(np.abs(source))])
        axis /= np.linalg.norm(axis)
        return Rotation.from_rotvec(axis*np.pi).as_matrix()
    return Rotation.from_rotvec(axis/sine * np.arctan2(sine, cosine)).as_matrix()
