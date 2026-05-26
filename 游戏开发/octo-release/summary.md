# octo-release 研究总结

> 仓库地址：https://github.com/DouglasDwyer/octo-release
> 研究日期：2026-05-26

## 一、仓库概述

Octo 是一个 Rust 编写的体素（voxel）游戏引擎，使用 ray marching（光线步进）和 compute shaders 实现大规模体素渲染，支持 Windows 原生和 Web（WebGPU/WASM）运行。目标是成为一个在线多人创作平台，用户可以创建、交互并通过 mods/plugins 扩展。

## 二、核心能力

### 2.1 技术架构

- **渲染**：基于 ray marching + LOD（多级细节）+ greedy meshing 的体素渲染
- **光照**：实时路径追踪光照（ambient occlusion、shadow、emissive voxels）
- **物理**：刚体物理模拟（connected component detection、collision detection/response）
- **网络**：TCP 网络多人游戏（桌面版）
- **Modding**：WASM 运行时 mod 加载系统（GUI 和用户输入 API）
- **语言**：Rust，运行在 Windows 原生和 Web（通过 WASM + WebGPU）

### 2.2 已实现功能

- 大规模体素 ray marching + LOD 渲染
- 实时路径追踪光照（ambient occlusion、emissive voxels）
- 完全可编辑的体素地形
- 刚体物理模拟
- 任意缩放比例导入体素模型
- TCP 网络多人游戏
- WASM 运行时 modding 系统

### 2.3 即将恢复的功能

- 半透明体素对象
- Octree 加速的 Perlin 噪声地形生成
- P2P 网络多人游戏（web 和 desktop）

### 2.4 未来计划

- 更沉浸的角色和相机控制
- 3D 空间音频
- 材质系统（纹理/音效/物理数据）

## 三、技术规格

### 3.1 支持的平台

- **原生**：Windows
- **Web**：Windows 或 Mac（Chrome/Edge/Opera 或任何启用 WebGPU 的浏览器）

### 3.2 控制方式

| 输入 | 动作 |
|---|---|
| 鼠标 | 环顾四周 |
| WASD | 水平移动 |
| Space/Shift | 垂直移动 |
| T | 锁定/解锁光标 |
| G | 切换材质 |
| F | 生成物理对象 |
| 左键 | 破坏体素 |
| 右键 | 构建/拖动对象 |
| Escape | 暂停游戏 |

## 四、版本历史

| 版本 | 主要内容 |
|---|---|
| 0.1.x | 基础 ray marching + LOD |
| 0.3.x | 刚体物理系统 + 多人游戏 |
| 0.5.x | 重写为新的体素数据结构 |
| 0.7.x | 路径追踪光照 |
| 0.8.x | 真实感刚体物理 |
| 0.9.x | WASM modding 系统 |

## 五、项目信息

- **Stars**：383
- **语言**：Rust（核心）+ JavaScript（Web 平台适配层）
- **许可证**：无明确开源许可证
- **创建时间**：2022-08-27
- **仓库类型**：游戏引擎 / 体素渲染引擎
- **仓库大小**：221MB（较大，包含编译后的 WASM 和 exe）