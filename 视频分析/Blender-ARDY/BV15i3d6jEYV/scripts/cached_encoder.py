"""Strict adapter for real, precomputed LLM2Vec embeddings."""
import json
from pathlib import Path

import numpy as np
import torch


class CachedPromptEncoder:
    def __init__(self, directory):
        self.directory = Path(directory).resolve()
        manifest = json.loads((self.directory / "manifest.json").read_text(encoding="utf-8"))
        self.entries = {item["text"]: item["file"] for item in manifest["entries"]}
        self.device = torch.device("cpu")
        self.dtype = torch.float32

    def to(self, device=None, dtype=None):
        if device is not None:
            self.device = torch.device(device)
        if dtype is not None:
            self.dtype = dtype
        return self

    def __call__(self, texts):
        if isinstance(texts, str):
            texts = [texts]
        if not texts:
            raise ValueError("At least one prompt is required")
        values = []
        for text in texts:
            if text not in self.entries:
                raise ValueError(f"Prompt not cached: {text!r}. Run encode_prompts.py first.")
            path = (self.directory / self.entries[text]).resolve()
            if not path.is_relative_to(self.directory):
                raise ValueError("Embedding path is outside the cache")
            value = np.load(path, allow_pickle=False)
            if value.shape != (1, 4096) or not np.isfinite(value).all() or not np.any(value):
                raise ValueError("Expected a finite, nonzero [1, 4096] LLM2Vec embedding")
            values.append(value)
        return torch.as_tensor(np.stack(values), device=self.device, dtype=self.dtype), [1] * len(values)
