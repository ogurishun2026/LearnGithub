# Existing runtime on the current Windows machine

These are optional discovery hints, not required paths and not output destinations. Verify existence before use. All newly generated work belongs to the active project, even when the runtime is reused read-only from here.

| Item | Previously working path |
|---|---|
| ARDY interpreter | `E:/3D建模动画研究/verification/ardy/demo_v1/venv/Scripts/python.exe` |
| ARDY source | `E:/3D建模动画研究/third_party/ardy` |
| Checkpoint parent | `E:/3D建模动画研究/verification/ardy/demo_v1/checkpoints` |
| NF4 encoder | `E:/3D建模动画研究/verification/kimodo/runtime/kimodo-venv/llm2vec-model` |
| Blender | `F:/Program Files (x86)/Steam/steamapps/common/Blender/blender.exe` |

The interpreter reused libraries from the existing Kimodo environment. Do not upgrade that shared environment without a separate need and authorization; choose a fresh environment for incompatible versions. Relative paths from an old project are not valid from a new project's current working directory.

Verified example sources and outputs are published at https://github.com/ogurishun2026/LearnGithub/tree/main/视频分析/Blender-ARDY/BV15i3d6jEYV . This is an example repository, not an automatic publishing destination. Follow the active task's Git instructions.
