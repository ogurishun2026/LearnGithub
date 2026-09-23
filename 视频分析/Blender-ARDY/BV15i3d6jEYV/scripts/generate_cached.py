"""Run upstream ARDY generation using cached NF4 text embeddings."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys
import time

import torch
from cached_encoder import CachedPromptEncoder


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--ardy-root", type=Path, required=True)
    parser.add_argument("--embeddings", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    options, forwarded = parser.parse_known_args()
    source = options.ardy_root.resolve() / "scripts" / "generate.py"
    sys.path.insert(0, str(options.ardy_root.resolve()))
    spec = importlib.util.spec_from_file_location("upstream_generate", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    original_loader = module.load_model
    encoder = CachedPromptEncoder(options.embeddings)
    timings = {}

    def load_with_cache(*args, **kwargs):
        started = time.perf_counter()
        model = original_loader(*args, **kwargs, text_encoder=encoder)
        if torch.cuda.is_available():
            torch.cuda.synchronize()
        timings["model_load_seconds"] = time.perf_counter() - started
        return model

    module.load_model = load_with_cache
    sys.argv = [str(source), *forwarded]
    torch.set_num_threads(8)
    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()
    started = time.perf_counter()
    module.main()
    if torch.cuda.is_available():
        torch.cuda.synchronize()
    timings.update(total_seconds=time.perf_counter() - started,
                   cuda=torch.cuda.is_available(), torch=torch.__version__,
                   peak_allocated_mib=torch.cuda.max_memory_allocated() / 2**20 if torch.cuda.is_available() else 0,
                   peak_reserved_mib=torch.cuda.max_memory_reserved() / 2**20 if torch.cuda.is_available() else 0,
                   text_encoder="cached NF4 LLM2Vec (experimental quantized conditioning)",
                   acceleration="PyTorch eager; no TensorRT",
                   timing_scope="Upstream main: model load, cached conditioning, generation, decoding and saving; excludes process/import startup and prior text encoding")
    options.report.parent.mkdir(parents=True, exist_ok=True)
    options.report.write_text(json.dumps(timings, indent=2), encoding="utf-8")
    print(json.dumps(timings, indent=2), flush=True)


if __name__ == "__main__":
    main()
