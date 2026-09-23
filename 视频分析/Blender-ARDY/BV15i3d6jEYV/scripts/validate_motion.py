"""Validate the saved Core27 demo independently of the generation process."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("motion", type=Path)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    with np.load(args.motion, allow_pickle=False) as data:
        positions = data["posed_joints"]
        frames = positions.shape[0]
        if frames < 2 or positions.shape != (frames, 27, 3):
            raise ValueError("Expected at least two frames of Core27 joint positions")
        for key in ("local_rot_mats", "global_rot_mats"):
            if data[key].shape != (frames, 27, 3, 3):
                raise ValueError(f"Invalid shape for {key}")
        if data["root_positions"].shape != (frames, 3) or float(data["fps"]) != 20:
            raise ValueError("Expected root translations and 20 FPS")
        for key in data.files:
            if np.issubdtype(data[key].dtype, np.number) and not np.isfinite(data[key]).all():
                raise ValueError(f"Nonfinite values in {key}")
        movement = float(np.abs(np.diff(positions, axis=0)).max())
        rotations = data["global_rot_mats"]
        orthogonality = float(np.abs(rotations @ rotations.swapaxes(-1, -2) - np.eye(3)).max())
        det_error = float(np.abs(np.linalg.det(rotations) - 1).max())
        if movement <= 1e-6 or orthogonality > 1e-3 or det_error > 1e-3:
            raise ValueError("Static sequence or invalid rotations")
        report = {"artifact": args.motion.name, "bytes": args.motion.stat().st_size,
                  "sha256": hashlib.sha256(args.motion.read_bytes()).hexdigest(),
                  "frames": frames, "joints": 27, "fps": 20, "duration_seconds": frames / 20,
                  "prompt": str(data["text"]), "all_numeric_arrays_finite": True,
                  "max_adjacent_joint_position_change_m": movement,
                  "max_rotation_orthogonality_error": orthogonality,
                  "max_rotation_determinant_error": det_error, "numeric_status": "pass",
                  "visual_status": "separate browser inspection required"}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
