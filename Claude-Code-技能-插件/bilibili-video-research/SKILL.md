---
name: bilibili-video-research
description: Use when researching a Bilibili video to reproduce a software, AI, Blender, or deployment workflow and the video may have incomplete subtitles, login-gated captions, or platform access limits.
---

# Bilibili Video Research

Use this skill to turn a B 站 tutorial into a traceable, runnable result. Keep three evidence classes separate throughout the work:

- **Video evidence:** what is visibly or audibly shown in the supplied video.
- **Reference evidence:** facts checked against the official project, repository, release notes, or an identified secondary article.
- **Experiment evidence:** commands, versions, hardware, timings, logs, and artifacts actually produced on the current machine.

## Workflow

1. Record the URL, BV id, title, duration, access date, and the intended output. Check whether the page exposes official subtitles without login. If captions are unavailable, do not invent a transcript.
2. Use an allowed public audio track and local ASR only as a research aid when needed. Label the transcript as approximate, keep timestamps, and record obvious recognition errors. Never upload the full audio or transcript unless the user explicitly asks and redistribution is allowed.
3. Identify the project from the video, then verify it from the official project page and repository. Pin a commit or release before installing. Treat creator scripts, forks, model quantization, and custom launchers as deviations until verified.
4. Inspect the machine before deployment: OS, Python, GPU, VRAM, CUDA/PyTorch, compiler, network restrictions, and required model access. Use a new versioned directory and isolated environment. Preserve existing Blender baselines and actions.
5. Run the smallest useful end-to-end test. Importing a package, starting an empty web page, or downloading a checkpoint is not a demo. For generation, require a non-empty artifact, expected schema/joint count/FPS, finite values, and measurable motion. In the viewer, inspect the generated character/geometry in at least two frames and during playback. A connected page, controls, grid, or WorldAxes alone do not count. Reject visible collapse, jitter-only motion, or an unrelated action even if numbers pass.
6. Record deviations such as CPU or NF4 conditioning, reduced duration, eager PyTorch, missing TensorRT, or a different OS. Do not call an experimental low-memory path “the official setup.”
7. Validate any export or Blender handoff separately. A valid `.npz` or BVH does not prove a character is correctly bound, retargeted, oriented, or free of mesh/contact failures.
8. Write a concise report with sources, evidence boundaries, exact commands, artifact paths, measurements, failures and limitations. Distinguish fresh-install recipes from environments that reused existing packages. Include only redistributable scripts and small demo artifacts. When the user requests Git upload, inspect the actual staged files, push to the authorized destination, and verify the remote commit before claiming upload completion.

## Acceptance checklist

- [ ] Source URL, BV id, access limits, and evidence classes are recorded.
- [ ] Official repository/model and a pinned version are identified.
- [ ] Dependencies run in an isolated, versioned environment.
- [ ] One fixed-input, fixed-seed end-to-end artifact exists and is independently checked.
- [ ] Output shape, frame rate, finite values, and non-zero motion are checked where applicable.
- [ ] Generated geometry is visible and playback changes it plausibly; controls or WorldAxes alone are not accepted.
- [ ] Hardware, VRAM, timings, and deviations are reported.
- [ ] Cookies, tokens, private configuration, full video/audio, model weights, virtual environments, and large caches are excluded from Git.

## Stop conditions

Stop and report a blocker when the official source cannot be identified, required model access is unavailable, the artifact fails schema/finite/motion checks, or the only evidence is an empty UI. Preserve the failing log and the exact command so another person can reproduce the issue.
