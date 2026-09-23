---
name: ardy-motion-workflow
description: Use when NVIDIA ARDY is selected for text-driven humanoid motion such as walking, idle or combat guard (走路、待机、战斗待机), when making an ARDY idle loop, or when converting ARDY Core27 NPZ into Blender, BVH or FBX for Unreal Engine. Not for reconstructing poses from images or transferring arbitrary existing rigs.
---

# ARDY Motion Workflow

Produce an actual generated motion, an inspectable Blender scene, and clearly scoped export evidence. The bundled converter supports **ARDY Core27 + its official reference skin**, adding one independent root for Core28 FBX. It does not produce a Manny-compatible Skeleton by renaming bones.

## Choose the route

| Request | Read and use |
|---|---|
| Generate a new text-driven action / deploy ARDY | [generation.md](references/generation.md); `encode_prompts.py`, `generate_cached.py` |
| Convert an existing Core27 NPZ | [blender-export.md](references/blender-export.md); `prepare_motion.py`, `build_blender.py` |
| Make a stationary combat/idle loop | [idle-loops.md](references/idle-loops.md); optional `make_loop.py` |
| Import or retarget in UE | [unreal-and-validation.md](references/unreal-and-validation.md) |
| Find this user's existing runtime | [local-runtime.md](references/local-runtime.md), only when those paths exist |

Resolve scripts relative to **this skill directory**, never the current project. Pass all input and output paths explicitly. Keep outputs, raw candidates, logs and renders in a versioned directory inside the active project's writable workspace. Use a new empty directory for each export; `prepare_motion.py` refuses an occupied output directory. Preserve existing actions and baseline files.

## Working decisions

1. Infer action style, target duration, in-place versus moving root, and required formats from the current request. Ask only when the missing choice materially changes the result. A generic combat guard can use an explicitly stated unarmed default. Do not silently switch an explicitly selected generator or target rig.
2. Reuse an available ARDY runtime after checking paths, pinned source, GPU capacity and dependencies. The global skill contains scripts and knowledge, **not model weights, an environment, or a running server**. Do not modify another project's environment merely to reuse it.
3. Generate real candidates, inspect their motion and pick one that visibly matches the request. A prompt saying “fists” does not prove closed fingers. Core27 lacks complete finger articulation; use the target character's finger pose later if needed.
4. Select `--root-mode planar` for locomotion: extract horizontal travel and heading into root, retain body bob in pelvis. Select `fixed` for a stationary action: root translation **and rotation** stay fixed. `fixed` alone does not remove travel from an already moving pelvis. Both modes preserve the supplied original joints' world transforms.
5. Use `--loop` only for an input that already contains a verified duplicate endpoint. It validates closure; it does not create it. Do not remove the last frame from non-looping motion. Idle fitting/foot locking is optional processing, never applied automatically to walks, jumps or attacks.
6. Convert, build, reopen the saved blend and reimport both FBXs with the bundled verifier. Then inspect real mesh renders and playback. Numbers cannot excuse reversed limbs, bad palms, sliding, floor penetration, poor timing or a wrong action.
7. Deliver the actual `.blend`, animation FBX, source skeletal FBX when needed, preview and brief usage instructions. Report source generation separately from loop/contact editing, Blender verification separately from UE import, and UE import separately from target retargeting. Git upload requires authorization in the active task; this skill does not grant it.

## Stable export contract

- Input: Core27 joint positions and rotation matrices, Y-up, meters; finite valid rotations and recorded FPS. Reject unsupported skeletons rather than truncating/relabeling them.
- BVH: centimeters, pelvis is the root, **root position channels only**. Blender 5.2's non-root position-channel interpretation caused double offsets; do not reintroduce child translation channels casually.
- Blender/FBX: centimeter scene (`scale_length=.01`), `root → pelvis`, 28 expected deform bones, unit armature scale, maximum four influences. Keep the original joint world transforms when adding root.
- FBX: `-Z` forward, `Y` up, `FBX_SCALE_NONE`, no leaf bones, only selected mesh/armature, only current action, bake each source frame without simplification. A static FBX establishes the bind pose. **The animation FBX also includes skin clusters**; armature-only export lost the original bind pose in the tested route. UE imports this second file with Import Mesh disabled.
- Timing: use source FPS and count. N ordinary samples span `(N-1)/fps` between first and last keys. A loop with N unique frames has N+1 exported samples, last equal to first; Blender previews only the N unique frames. FBX round-trip uses `anim_offset=0`.

## Completion evidence

Run the relevant bundled tests when scripts change. `verify_exports.py` proves Blender/FBX structure, timing, bind pose and joint transforms; `render_preview.py` measures the mesh and renders actual frames. `--contact-mode planted` is only for a clip whose two feet should remain planted, after contact correction. Review front/side and representative frames plus motion/loop boundaries. Record limitations such as open hands or untested target characters.

If a check fails, preserve its evidence and fix the failing stage; do not loosen tolerances or relabel a reference-skin demo as retargeting success. User preferences and current project instructions take precedence over example durations, paths and styles in the references.
