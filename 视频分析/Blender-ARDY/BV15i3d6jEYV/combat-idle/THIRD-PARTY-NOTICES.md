# 来源与修改

参考人体与 Core27 骨架来自 `nv-tlabs/ardy`，commit `693f74d13b3d04a0a22ce127ee79c929dd89756b`，资源 `ardy/assets/skeletons/cskel27/skin_standard.npz`。

Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.

上游 Apache License 2.0 全文随附于 [LICENSE-ARDY.txt](LICENSE-ARDY.txt)。模型与量化文字编码器许可分别见上一阶段研究总结列出的上游模型页；本包不包含其权重。

本次修改：截取 ARDY 生成的候选片段，平滑为 4 秒循环，通过双骨腿 IK 固定足部并按参考网格校正脚底接地；Hips 改名为 pelvis，Blender/FBX 新增固定 root；转换坐标系与厘米单位；18 个五权重顶点裁剪为四权重；添加蓝色预览材质和地面。新脚本与报告记录实际处理步骤。原始生成和最终处理后动作分别保存。
