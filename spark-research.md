---
name: spark-research
description: Spark 深度研究 —— World Labs 开源的 Web 端 3D Gaussian Splatting 渲染器
metadata: 
  node_type: memory
  type: reference
  originSessionId: 6aafdfcd-c3e4-495d-a2d3-5636278c31ab
---

**Spark** 是一个基于 **THREE.js** 的高级 **3D Gaussian Splatting（3DGS）渲染器**，由 **World Labs**（李飞飞创办的公司）开发并开源。

仓库地址：`https://github.com/sparkjsdev/spark`

## 为什么重要（Why）

开发自动化 Agent 时，如果工作流涉及 **AI 生成 3D 内容**、**计算机视觉结果的 3D 可视化**、或者**生成包含 3D 场景的 Web 应用**，Spark 是目前开源社区最成熟的 Web 端渲染方案。它展示了如何在浏览器中高效渲染大规模 3D Gaussian Splat，以及 TypeScript + Rust/WASM 混合架构的最佳实践。

## 技术栈

| 维度 | 详情 |
|------|------|
| 前端 | TypeScript（54 个 `.ts`）+ GLSL（8 个 shader） |
| 高性能计算 | Rust（28 个 `.rs`）编译为 WebAssembly |
| 渲染底座 | THREE.js（peer dependency ≥ 0.180.0） |
| 构建 | Vite 6 + `vite-plugin-glsl` |
| 版本 | 2.1.0 |
| 许可证 | MIT |

## 核心架构

### 主类层次

```
SparkRenderer          → 主渲染器，继承 THREE.Object3D，接入 THREE.js 管线
  └─ SplatGeometry     → 基于 InstancedBufferGeometry，每个 splat 画一个 quad
  └─ SplatMesh         → 核心 splat 网格，支持加载/动画/编辑/皮肤
       ├─ PackedSplats → 紧凑打包的 splat 数据（纹理存储）
       ├─ ExtSplats    → 扩展 splat 数据
       ├─ SplatSkinning → 骨骼动画（双四元数 / 线性混合）
       ├─ SplatEdit    → 基于 SDF 的实时空间编辑
       └─ SplatGenerator → 程序化生成/变换 splat
```

### Rust/WASM 层（`rust/`）

| 模块 | 职责 |
|------|------|
| `sort.rs` | Splat 深度排序（CPU 端，基于 readback 深度） |
| `raycast.rs` | 射线检测（点击拾取 splat） |
| `decoder.rs` | 多格式 splat 解码 |
| `lod_tree.rs` | LOD（细节层次）树构建 |

### 渲染管线

1. **数据存储**：Splat 数据存储在 `DataTexture` / `DataArrayTexture` 中
2. **排序**：每帧从 GPU readback 深度，WASM 中深度排序，生成 `ordering` 纹理
3. **Vertex Shader**：通过 `gl_InstanceID` 查 `ordering` 纹理获取 splat 索引，计算椭圆投影
4. **Fragment Shader**：在 quad 上根据高斯分布计算透明度，混合颜色

## 主要功能特性

| 特性 | 说明 |
|------|------|
| **多格式支持** | `.PLY`、`.SPZ`、`.SPLAT`、`.KSPLAT`、`.SOG` |
| **Dyno Shader Graph** | 运行时动态构建 GLSL 程序，在 GPU 上程序化创建/编辑 splat |
| **SplatEdit（SDF 编辑）** | 基于有向距离场的实时空间编辑（平面/球体/盒/椭球/圆柱/胶囊/锥），支持 RGBA+XYZ 位移 |
| **SplatSkinning** | 骨骼动画，双四元数模式（默认，避免关节塌陷），最多 256 根骨骼 |
| **WebXR** | VR/AR 模式、手部追踪、控制器、固定注视点渲染 |
| **LOD** | 多层级细节、流式 LOD、Rust 端构建 LOD 树 |
| **多 splat 排序** | 多个 SplatMesh 在一起时仍保持正确深度排序 |
| **多视角渲染** | 支持多个相机/视口同时渲染 |
| **射线检测** | 点击拾取 splat |
| **粒子动画/模拟** | 程序化粒子系统 |
| **传送门效果** | `SparkPortals` |

## 如何应用（How to apply）

1. **AI 3D 资产生成管线**：如果 Agent 需要处理/展示 AI 生成的 3D Gaussian Splat（从视频/图像重建），Spark 是 Web 端最佳渲染方案
2. **3D 场景理解 Agent**：结合多模态 LLM，Agent 可以在 Spark 渲染的 3D 场景中进行交互式分析、标注、编辑
3. **Web 应用生成**：Agent 生成包含 3DGS 的网页应用时，Spark 提供完整成熟的渲染层
4. **学习 WebGL 渲染架构**：Spark 的排序管线、LOD 设计、Shader Graph 实现、TypeScript+Rust/WASM 混合架构都是高质量参考实现

## 相关记忆

- [[ai-game-studio-deep-dive]] — 序列帧动画生成工具，与 Spark 同属 AI 生成 3D/视觉内容方向
- [[ai-workflow-discussion]] — AI 全自动化工作流探索
