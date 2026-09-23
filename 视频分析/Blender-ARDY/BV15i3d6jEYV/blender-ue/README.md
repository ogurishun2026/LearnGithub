# ARDY 动作导入 Blender，再应用到 Unreal Engine

这一份交付针对当前 `A person walks forward.` 的 40 帧短动作。已完成 BVH → Blender 实际导入、Blender 工程保存/重新打开，以及 FBX 导出/重新导入比对。**UE 导入和角色重定向尚未实测。**

## 文件怎么用

| 文件（均在 artifacts 下） | 用途 |
|---|---|
| `ARDY_Walk_Core28.blend` | 推荐直接用 Blender 打开，已有蓝色参考人体和动画 |
| `ARDY_Walk_Core27.bvh` | 在其他 Blender 工程中导入原始骨骼动作，不含人物网格 |
| `SK_ARDY_Core28.fbx` | 在 UE 中首次建立 ARDY 源 Skeletal Mesh 和 Skeleton，参考姿势无动画 |
| `AN_ARDY_Walk_RootMotion.fbx` | 在 UE 中导入走路动画，选择上一步建立的 Skeleton |

BVH 保留 27 个关节，根关节名为 `pelvis`。Blender/FBX 在它上面增加独立的 `root`，总计 28 根骨骼；原 ARDY `Hips` 改名为 `pelvis`。所有原始关节的世界位置与旋转保留，水平位移和朝向转移到 `root`，骨盆保留上下起伏。动画 FBX 也携带参考网格以固定绑定姿势；第二步只导入动画即可。

## 在 Blender 看、编辑或换角色

最简单：文件 → 打开 `ARDY_Walk_Core28.blend`，按空格播放。时间轴为 1–40 帧，20 FPS；场景为厘米单位（Unit Scale 0.01）。蓝色人体是 ARDY 官方参考网格，不是你的游戏角色。

若要导入现有的米制 Blender 场景：文件 → 导入 → Motion Capture / BioVision BVH，选 `ARDY_Walk_Core27.bvh`，Scale 设 **0.01**，Forward **-Z**，Up **Y**，FPS 设 **20**，不要启用改变时间长度的 FPS Scale；确认 1–40 帧。如果场景与附带工程一样用厘米坐标，导入 Scale 设 **1**。找不到 BVH 菜单时启用/安装 Blender 的 BioVision Motion Capture 导入扩展。

BVH 只有骨架和动作，不会自动驱动另一套骨架的人物。要在 Blender 换成已有角色，须用重定向工具（例如兼容当前 Blender 版本的 Rokoko 插件）设置源 `pelvis/Spine/...` 与目标骨骼对应，统一参考姿势和比例，然后烘焙为目标角色的新 Action。不能仅因为骨骼名称类似就直接共享 Action。此步未在本次交付中执行；若最终用途是 UE，推荐直接在 UE 对源动画重定向，减少一次转移。

## 在 UE5 建立源骨架和动画

1. 在内容浏览器新建 `/Game/ARDY/Demo_v1/Source`。导入 `SK_ARDY_Core28.fbx`：启用 Skeletal Mesh，Skeleton 选择 **None**，关闭 Import Animations。得到 ARDY 的新网格与 Skeleton；不要选 Manny 或旧角色的 Skeleton。
2. 导入 `AN_ARDY_Walk_RootMotion.fbx`：选择刚创建的 **ARDY Skeleton**，启用 Import Animations，关闭 Import Mesh，不要更新已有 Skeleton 的参考姿势。采用文件采样率，或指定 20 FPS（若有默认 30 FPS 选项则关闭）。UE 各版本的 FBX/Interchange 面板名称略有不同。
3. 打开生成的 Animation Sequence。核对 28 根骨骼、`root → pelvis`、人物约 190.5 cm、整体比例正确、动作确实迈步。40 个采样点的首尾时间跨度为 **1.95 秒**；按 20 FPS 播放 40 帧是约 2 秒。不要因 UE 显示 1.95 秒而补帧或拉伸速度。

若只想看这次蓝色参考人体的动作，到这里就可以直接预览 Animation Sequence，不必先做角色重定向。想让 Manny 或自己的角色执行同一动作，再继续下面的步骤。

## 应用到 Manny / Quinn（目标为自己的角色时替换目标 IK Rig）

1. 给 ARDY 参考网格建立 `IK_ARDY_Core28`；给 Manny/Quinn 使用其已有 IK Rig 或新建目标 IK Rig。两边 **Retarget Root 都设为 pelvis**。
2. 建立以下对应链。链名可以相同便于自动匹配，但关节不能按“同名 Skeleton”强行合并。

| 链 | ARDY 起点 → 终点 | Manny 起点 → 终点 |
|---|---|---|
| Root | root → root | root → root |
| Spine | Spine → Spine3 | spine_01 → spine_05 |
| Head | Neck → Head | neck_01 → head |
| LeftArm | LeftShoulder → LeftHand | clavicle_l → hand_l |
| RightArm | RightShoulder → RightHand | clavicle_r → hand_r |
| LeftLeg | LeftUpLeg → LeftToeBase | thigh_l → ball_l |
| RightLeg | RightUpLeg → RightToeBase | thigh_r → ball_r |

3. 创建 IK Retargeter，Source 选 ARDY，Target 选目标角色。统一 Retarget Pose 的肩臂/腿朝向（本源模型是 T Pose，Manny 通常是 A Pose）；先检查站立、迈步与左右方向。
4. 保留独立 root 的位移。如果版本使用 Root Motion 操作，目标 root 设为 `root`，目标骨盆设为 `pelvis`；Root 链不能从 root 连到 pelvis。其他版本在相应的根平移/链设置中保留根运动。
5. 预览这条走路动画，检查脚底、膝肘、手掌、缩放和约 1.47 米的根位移，再 Export Retargeted Animation 到 `/Game/ARDY/Demo_v1/Retargeted`。生成的动画现在才属于目标角色的 Skeleton。

## 在场景/游戏中播放

- **先看效果：**把目标角色加入 Sequencer，添加 Animation Track，选择重定向后的 Animation Sequence。先播放一遍。
- **让游戏角色实际前进：**在动画资源启用 Root Motion，并通过角色的 Anim Blueprint / Montage 使用一致的 Root Motion 模式（常见为 Montage + Root Motion from Montages Only）。让动画位移驱动胶囊体；不要再用另一条逻辑重复施加同一段位移。
- **由 Character Movement 控制速度：**需要另做去除 root 位移的 In-place 动画，再放进状态机/Blend Space。本交付是带 Root Motion 的版本，没有附带 In-place 版本。

这条短样本从站立进入走路，首尾并非无缝循环；不要直接把它当循环 Walk。当前骨架没有完整手指链，不能提供精细手指动画。

## 验证与边界

- Blender 5.2.2 LTS，全新进程重新打开 `.blend`。
- BVH 全 40 帧最大关节位置误差约 0.000047 cm。
- `.blend` 全 40 帧最大关节位置误差约 0.000104 cm。
- 动画 FBX 重新导入最大关节位置误差约 0.000119 cm，最大旋转矩阵分量误差约 0.0000012；骨架对象 scale=(1,1,1)。
- 参考网格 9,084 顶点。18 个原有五权重顶点裁剪/归一化为四权重，抽样与官方网格最大差异约 2.64 mm；未发现明显塌缩，但这不是完整穿模/脚滑验收。
- 已查看第 1、11、21、31、40 帧的 Blender 渲染，见 `artifacts/preview-contact-sheet.jpg`。
- 无 UE 目标角色实测结果；上述 UE 步骤是待执行操作说明，不能称已完成 Manny/MetaHuman 重定向。

## 重新生成

直接使用附带的 Blender/FBX 文件无需安装 ARDY 或下载模型。只有重新生成转换文件才需要前一阶段的 ARDY Python 环境，以及带 BVH 导入器的 Blender。这几个脚本只针对本次 40 帧 Core27 样本，未做通用插件。

```powershell
# 在本项目根目录，使用已有环境
verification/ardy/demo_v1/venv/Scripts/python.exe verification/ardy/blender_ue_v1/convert_bvh.py verification/ardy/demo_v1/outputs/walk.npz --out verification/ardy/blender_ue_v1/artifacts
```

从 LearnGithub 克隆后，先按前一阶段部署说明准备 `runtime/venv` 和 `runtime/ardy`。在包含 `summary.md` 的目录运行以下命令；只转换仓库中的样本，不必下载生成模型。将 Blender 路径改为本机安装位置，重建输出放在独立 runtime 目录中：

```powershell
$ardyBlender = 'F:/Program Files (x86)/Steam/steamapps/common/Blender/blender.exe'
runtime/venv/Scripts/python.exe blender-ue/test_bvh_conversion.py
runtime/venv/Scripts/python.exe blender-ue/convert_bvh.py demo-artifacts/walk.npz --out runtime/blender-ue-rebuild
& $ardyBlender --background --factory-startup --python-exit-code 1 --python blender-ue/build_blender.py -- --artifacts runtime/blender-ue-rebuild
& $ardyBlender --background --factory-startup --python-exit-code 1 --python blender-ue/verify_saved_exports.py -- --artifacts runtime/blender-ue-rebuild
```

源码/参考网格：[NVIDIA nv-tlabs/ardy](https://github.com/nv-tlabs/ardy/tree/693f74d13b3d04a0a22ce127ee79c929dd89756b)，上游版权与 Apache-2.0 文本见 [LICENSE-ARDY.txt](LICENSE-ARDY.txt)，修改和来源见 [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md)。生成动作使用的 ARDY checkpoint 及 NF4 文字条件来源见前一阶段研究总结。本地原有角色、Blender v4 和旧 Action 没有修改。
