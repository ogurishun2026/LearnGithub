# Generating with ARDY

## Tested baseline

- Official source: https://github.com/nv-tlabs/ardy at `693f74d13b3d04a0a22ce127ee79c929dd89756b`.
- Core model: `nvidia/ARDY-Core-RP-20FPS-Horizon8`, 27 joints, 20 FPS. Inspect upstream instructions before changing revisions/model families.
- Windows 11, Python 3.12.4, PyTorch 2.5.1+cu121, RTX 4060 Laptop 8 GB; Blender 5.2.2 LTS. These are observed versions, not a claim that other versions fail.
- Quantized text conditioning: `Aero-Ex/KIMODO-Meta3_llm2vec_NF4`, revision `207f0c64a7325f6045d15c68c5ea9e961c18fafd`. This is an experimental substitute for the default upstream encoder. Record it as such.
- No TensorRT required for the demonstrated eager PyTorch route. The original Windows environment reused an existing library environment; do not call it a verified clean-machine installation.

## Discover before downloading

Locate the user's ARDY checkout, interpreter, checkpoint directory and encoder directory. Check CUDA availability and currently free VRAM. Keep models/cache reusable but write candidates into the current project. The bundled `download_checkpoint.py` pins/checks every expected checkpoint file, including statistics and hashes. Large weights and environments stay out of Git.

When installing from scratch, use an isolated Python 3.12 environment, a CUDA-compatible PyTorch build and the pinned upstream `ardy[demo]` installation. Check upstream compiler/CMake requirements for the motion-correction extension. The tested NF4 package was bitsandbytes 0.50.1. Models and quantized/base encoders have separate upstream license/access requirements; the code license does not replace them.

## Encoding strategy

Use the existing cached prompt only for its **exact original text**. Unknown text fails explicitly. Put each new prompt batch in a new embedding directory because the encoder script writes a new manifest.

For NF4 encoding, prefer CUDA when measured free VRAM has headroom for the encoder; release the encoder process before loading the motion model. An observed run with about 6 GB free on an 8 GB card encoded two longer prompts in under a second of encode time after model loading. This excludes startup/load time and is not a hardware guarantee. CPU fallback worked for a short prompt but was prohibitively slow for longer prompts. Do not force CPU just because the card has 8 GB. If memory is insufficient, use CPU or reduce other authorized workload; do not terminate unrelated GPU processes.

Set these variables to discovered absolute paths. `$SkillRoot` is the installed skill folder, `$RunDir` is a new directory inside the active project; `$ArdySource` must be the matching checkout.

```powershell
$Prompt = 'A person stands still in a fighting guard, hands up, knees slightly bent, with small weight shifts and no steps.'
& $ArdyPython "$SkillRoot/scripts/encode_prompts.py" --model $EncoderDir --output "$RunDir/embeddings" --device cuda $Prompt
# Wait for the encoder process to finish before this command.
& $ArdyPython "$SkillRoot/scripts/generate_cached.py" --ardy-root $ArdySource --embeddings "$RunDir/embeddings" --report "$RunDir/generation.json" $Prompt --model core8 --duration 6 --num_samples 3 --seed 42 --output "$RunDir/candidates/guard" --checkpoints_dir $CheckpointDir --no-postprocess
```

Duration/sample count/seed are examples; choose them for the request. `--no-postprocess` preserves the raw generation for later explicit processing. Upstream post-processing may instead be appropriate, but record and validate it separately. Keep raw NPZ files even after trimming or fixing contact.

The cached adapter records model load, cached conditioning, generation, decoding and saving; it excludes process/import startup and prior text encoding. Never present that measurement as full text-to-animation latency.

Inspect source shape, FPS, finite values, actual motion, hand/head/foot placement, direction and displacement. Retain the prompt, seed, source revision, encoder manifest and selected sample hash. Reject “connected viewer” or an empty axis grid as evidence. Candidate count does not guarantee style compliance.
