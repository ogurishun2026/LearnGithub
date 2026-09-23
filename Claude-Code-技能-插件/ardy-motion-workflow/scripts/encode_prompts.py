"""Cache real NF4 LLM2Vec conditioning, in a separate process from ARDY."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import time

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

import numpy as np
import torch
from ardy.model.llm2vec.llm2vec import LLM2Vec


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--device", default="cpu", choices=["cpu", "cuda"])
    parser.add_argument("prompts", nargs="+")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    start = time.perf_counter()
    torch.set_num_threads(min(8, os.cpu_count() or 4))
    model = LLM2Vec.from_pretrained(str(args.model.resolve()), peft_model_name_or_path=None,
                                   torch_dtype=torch.float16, device_map=args.device)
    model.eval()
    load_seconds = time.perf_counter() - start
    entries = []
    for prompt in args.prompts:
        started = time.perf_counter()
        with torch.inference_mode():
            value = model.encode([prompt], batch_size=1, show_progress_bar=False, device=args.device)
        value = np.asarray(value, dtype=np.float32).reshape(1, 4096)
        if not np.isfinite(value).all() or not np.any(value):
            raise ValueError("Encoder produced invalid conditioning")
        name = hashlib.sha256(prompt.encode()).hexdigest() + ".npy"
        np.save(args.output / name, value, allow_pickle=False)
        entry = {"text": prompt, "file": name, "shape": list(value.shape),
                 "seconds": time.perf_counter() - started,
                 "sha256": hashlib.sha256((args.output / name).read_bytes()).hexdigest()}
        entries.append(entry)
        print(json.dumps(entry), flush=True)
    manifest = {"encoder": "Aero-Ex/KIMODO-Meta3_llm2vec_NF4", "quantization": "NF4",
                "conditioning_status": "experimental_quantized_llm2vec",
                "device": args.device, "load_seconds": load_seconds,
                "model_config_sha256": hashlib.sha256((args.model / "config.json").read_bytes()).hexdigest(),
                "entries": entries}
    (args.output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
