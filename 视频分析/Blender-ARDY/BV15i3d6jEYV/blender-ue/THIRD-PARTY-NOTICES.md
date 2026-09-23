# 来源与修改说明

此目录的 `.blend` 和两个 `.fbx` 包含来自 NVIDIA ARDY 的参考人体网格及骨架。来源：[`nv-tlabs/ardy`](https://github.com/nv-tlabs/ardy/tree/693f74d13b3d04a0a22ce127ee79c929dd89756b)，commit `693f74d13b3d04a0a22ce127ee79c929dd89756b`，资源路径 `ardy/assets/skeletons/cskel27/skin_standard.npz`。

Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.

上游 Apache License 2.0 原文及版权声明随附于 [LICENSE-ARDY.txt](LICENSE-ARDY.txt)。本包不包含 ARDY 模型权重或 NF4 文字编码器权重；模型和文字条件来源在上一阶段研究总结中分别记录，不能用代码许可代替模型许可。

本次转换修改：Y-up 米制数据转换为 Blender Z-up 厘米坐标；`Hips` 改名为 `pelvis`；Blender/FBX 增加独立 `root` 并烘焙水平位移/朝向；18 个五权重顶点保留最大的四项并归一化；添加蓝色预览材质、灯光环境和地面。原始骨架关节的世界位置/旋转逐帧比对，修改后的网格有抽样偏差报告。BVH 保留 27 关节，Blender/FBX 为 28 骨。

转换脚本为本次复现新增，未安装视频作者的第三方 BVH 导出扩展。生成样本为 `A person walks forward.`，40 帧，20 FPS，使用 ARDY Core8、seed 0、关闭后处理。UE 导入和目标角色重定向尚未实测。
