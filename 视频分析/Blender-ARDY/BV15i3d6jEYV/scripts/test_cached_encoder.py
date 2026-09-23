import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
import torch

from cached_encoder import CachedPromptEncoder


class CachedPromptEncoderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.directory = Path(self.tmp.name)
        np.save(self.directory / "walk.npy", np.full((1, 4096), 0.25, dtype=np.float32))
        (self.directory / "manifest.json").write_text(json.dumps({"entries": [
            {"text": "A person walks forward.", "file": "walk.npy"}]}))

    def tearDown(self):
        self.tmp.cleanup()

    def test_repeated_prompt_produces_correct_batch_and_dtype(self):
        encoder = CachedPromptEncoder(self.directory).to(dtype=torch.float64)
        result, lengths = encoder(["A person walks forward."] * 2)
        self.assertEqual(tuple(result.shape), (2, 1, 4096))
        self.assertEqual(lengths, [1, 1])
        self.assertEqual(result.dtype, torch.float64)
        self.assertTrue(torch.all(result == 0.25))

    def test_unknown_text_is_not_silently_replaced(self):
        with self.assertRaisesRegex(ValueError, "not cached"):
            CachedPromptEncoder(self.directory)(["A person jumps."])

    def test_invalid_embedding_is_rejected(self):
        np.save(self.directory / "walk.npy", np.zeros((1, 20)))
        with self.assertRaisesRegex(ValueError, "4096"):
            CachedPromptEncoder(self.directory)(["A person walks forward."])


if __name__ == "__main__":
    unittest.main()
