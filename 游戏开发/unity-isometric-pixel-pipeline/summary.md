# unity-isometric-pixel-pipeline 研究总结

> 仓库地址：https://github.com/bababuyyy/unity-isometric-pixel-pipeline
> 研究日期：2026-05-20

## 一、仓库概述

**Unity 6 URP 的像素艺术等距渲染管线** — 提供 Toon shading、GPU 实例化草丛、自适应轮廓和像素完美的清晰 upscale。

专为等距 3D 游戏设计，目标是手绘像素艺术美学，灵感来自 [t3ssel8r](https://www.youtube.com/@t3ssel8r)。

## 二、核心内容

### 2.1 核心技术概念

**像素艺术 3D 渲染的核心思想**：
1. 以极低内部分辨率（640×360）渲染 3D 场景
2. 在该分辨率应用 1 像素轮廓着色器
3. 使用锐利滤镜 upscale 到屏幕

因为轮廓在内部分辨率计算，每个边缘保证恰好 1 像素——这就是它读起来像像素艺术的原因。

### 2.2 5-Pass 渲染管线

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐     ┌───────────┐     ┌──────────────┐
│ Scene        │────▶│ Downsample   │────▶│ Outline 1px  │────▶│ Composite │────▶│ Sharp        │
│ (full res)   │     │ (640×360)    │     │ (640×360)    │     │ (640×360) │     │ Upscale      │
└─────────────┘     └──────────────┘     └──────────────┘     └───────────┘     └──────────────┘
```

| Pass | 说明 |
|------|------|
| **Pass 0** | CopyColor - 拷贝全分辨率相机输出到安全缓冲区 |
| **Pass 1** | Downsample Color - 从全分辨率下采样到 640×360 |
| **Pass 2** | Outline at Internal Resolution - 最重要！在 640×360 检测轮廓 |
| **Pass 3** | Composite - 将轮廓遮罩混合到低分辨率场景颜色 |
| **Pass 4** | Sharp Upscale - 锐利 upscale 到屏幕分辨率 |

### 2.3 核心着色器

| 着色器 | 功能 |
|--------|------|
| **ToonLit** | 标准不透明材质着色器，带 Toon 分级 |
| **GrassBlade** | Billboard 草丛，GPU Instancing (~35k 实例) |
| **OutlineShader** | 屏幕空间边缘检测（轮廓检测） |
| **CompositeShader** | 轮廓遮罩与场景颜色的 alpha 混合 |
| **SharpUpscale** | 锐利 upscale + 像素完美平移补偿 |

### 2.4 ToonLit 特性

- **Toon Stepping** — 将漫反射光照量化为离散级别（`_Cuts` 参数）
- **Cloud Shadows** — 全局滚动噪声纹理调制光照
- **Bayer Dithering** — 可选 4×4 有序抖动
- **Patch System** — 世界空间噪声驱动颜色变化
- **Palette System** — 允许艺术控制的阴影/高光色调

### 2.5 GrassBlade 特性

- **GPU Instancing** — ~35k 实例
- **Color Inheritance** — 颜色来自与地形相同的 patch 系统
- **Wind** — 双层噪声驱动摇摆
- **Accent Sprites** — 随机替换花朵/装饰精灵
- **Fake Perspective** — 基于风和相机方向的 UV 扭曲

### 2.6 像素完美平移

解决 3D 场景中低分辨率移动导致的像素蠕动（pixel creep）问题：

1. **Snap** — 将相机位置捕捉到最近的 texel 大小网格点
2. **Compensate** — 将捕捉误差作为 UV 偏移应用到 upscale 着色器

### 2.7 昼夜循环

| 组件 | 职责 |
|------|------|
| **DayNightCycleManager** | 时间单一数据源，控制太阳/月亮轨道、强度和颜色 |
| **CloudShadowManager** | 云视觉参数（缩放、对比度、阈值、滚动方向） |

## 三、技术架构

### 3.1 项目结构

```
Assets/
├── Materials/
│   ├── Pipeline/          # 渲染管线材质 (Outline, Composite, SharpU)
│   ├── Toon/             # ToonLit 材质示例
│   └── Grass/           # GrassBlade 材质
├── Rendering/
│   ├── PC_Renderer.asset # URP Renderer Data
│   └── RenderFeatures/
│       ├── PixelRendererFeature.cs  # 5-pass 渲染管线
│       └── OutlineRendererFeature.cs
├── Scripts/Systems/
│   ├── DayNightCycleManager.cs
│   ├── CloudShadowManager.cs
│   ├── GrassSpawner.cs
│   ├── IsometricCameraController.cs
│   └── PlayerPlaceholder.cs
├── Shaders/
│   ├── ToonLighting/    # ToonLit.shader, GrassBlade.shader
│   └── PostProcess/     # Outline, Composite, SharpUpscale
└── Scenes/DemoScene.unity
```

### 3.2 技术要求

| 要求 | 说明 |
|------|------|
| Unity 版本 | Unity 6 (6000.x) |
| 渲染管线 | Universal Render Pipeline (URP) |
| SSAO | **必须禁用**（会导致 GPU 实例化草丛的伪影） |

### 3.3 轮廓检测原理

**Silhouette Detection**：
- 采样 3×3 网格的 8 个邻居
- 检测深度不连续性
- 使用自适应阈值（基于表面角度）
- 使用最近邻居颜色变暗（`_LineDarken`）

**Crease Detection**：
- 使用 4 个主要邻居的**方向对比度**方法
- 避免在弯曲面上错误触发
- 增亮中心像素颜色（`_CreaseBrighten`）

### 3.4 为什么不用 PBR？

管线专为**平面 Toon shading 和离散颜色级别**设计：
- PBR 纹理（粗糙度、金属度、法线图）产生的平滑渐变与 toon 分级冲突
- 在 640×360，PBR 渐变成为离散级别之间的视觉噪声
- 没有同时满足 PBR 和像素艺术的分辨率甜蜜点

## 四、与 unity-mcp 的关系

| 维度 | unity-isometric-pixel-pipeline | unity-mcp |
|------|-------------------------------|-----------|
| **功能** | 像素艺术渲染管线 | Unity Editor AI 控制 |
| **关注点** | 视觉效果 | 编辑器自动化 |
| **语言** | HLSL/GLSL (Shader) + C# | C# + TypeScript |
| **定位** | 游戏美术/渲染 | AI Agent 集成 |

两者互补：一个提供像素艺术渲染能力，一个让 AI 控制 Unity 编辑器。

## 五、Star 历史与社区

- **Stars**: 未获取到（API 限流）
- **语言**: C# + HLSL
- **许可**: MIT (推测)
- **更新**: 2026-05-20

## 六、总结

unity-isometric-pixel-pipeline 是一个**专业的像素艺术 3D 渲染管线**，解决了在 Unity 中创建等距像素艺术游戏的核心技术挑战。

**核心价值**：
- 5-pass 渲染管线确保 1px 轮廓在任意分辨率下都成立
- Toon shading + 离散颜色级别实现真正的像素艺术美学
- GPU Instancing 草丛（~35k 实例）性能友好
- 像素完美平移消除摄像机移动时的像素蠕动
- 昼夜循环系统提供沉浸式光照变化

**技术亮点**：
- Unity 6 Render Graph API
- 自定义轮廓检测（深度 + 法线双通道）
- 锐利 upscale 算法（fwidth + smoothstep）
- 云影和风噪声系统

**适用场景**：
- 等距像素艺术 3D 游戏开发
- 需要手绘像素美学但想用 3D 场景的开发者
- 研究现代 Unity 渲染管线的学习资源