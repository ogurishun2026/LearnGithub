# ppf-contact-solver 研究总结

> 仓库地址：https://github.com/st-tech/ppf-contact-solver
> 研究日期：2026-05-26

## 一、仓库概述

ZOZO's Contact Solver 是日本最大时尚电商 ZOZO, Inc. 开源的物理仿真引擎，专门处理服装（shells）、固体（solids）和杆件（rods）之间的碰撞接触。核心算法已发表在 ACM Transactions on Graphics (TOG) 期刊。支持 Blender 编辑器插件，可在 Blender 内直接运行大规模物理仿真。

## 二、核心能力

### 2.1 技术亮点

| 特性 | 说明 |
|---|---|
| **无穿透碰撞** | 碰撞解析完全无穿透、无缠绕 |
| **超大规模** | 支持超过 1.8 亿次碰撞接触 |
| **单精度 GPU** | 全 GPU 运行，仅用单精度浮点 |
| **三角形有界延伸** | 三角形延伸严格不超过上限（如 1%） |
| **FEM 弹性** | 使用有限元法处理可变形体和符号力雅可比矩阵 |
| **MCP 支持** | 支持 LLM 通过自然语言控制仿真 |

### 2.2 支持的仿真类型

- **服装（Shells）**：布料、衣物仿真
- **固体（Solids）**：刚体/柔体
- **杆件（Rods）**：绳索、链条

### 2.3 部署方式

| 方式 | 说明 |
|---|---|
| **Windows 原生** | 解压即用，无安装向导 |
| **Docker** | 约 1GB 镜像，包含 JupyterLab |
| **Blender 插件** | 通过 Blender 编辑器远程仿真 |
| **云平台** | 支持 vast.ai、Scaleway、AWS、GCE |

### 2.4 仿真规模参考

| 示例 | 接触数量 | 说明 |
|---|---|---|
| five-twist | >180M | 超大规模布料扭曲 |
| large-five-twist | >180M | 大规模五重扭曲 |
| large-woven | 大规模 | 编织物仿真 |

## 三、技术架构

### 3.1 技术栈

- **语言**：C++/Python
- **GPU**：CUDA（单精度）
- **前端**：Blender Add-on（Python）
- **后端**：JupyterLab（Python API）
- **论文**：ACM TOG Vol.43, No.6

### 3.2 目录结构

```
ppf-contact-solver/
├── asset/               # 资源文件
├── articles/            # 技术文章（开发文档、bug修复等）
├── examples/            # JupyterLab 示例notebook
├── solver/              # 核心求解器
├── blender_addon/       # Blender插件
├── .github/workflows/   # GitHub Actions（压力测试等）
└── README.md
```

### 3.3 核心算法

基于"具有弹性包容动态刚度的三次屏障函数"（A Cubic Barrier with Elasticity-Inclusive Dynamic Stiffness），在 ACVD（ Accelerated Contact Vertex Dynamics）框架内实现。

## 四、项目信息

- **Stars**：未公开
- **语言**：C++/Python
- **许可证**：Apache 2.0（可商用、可闭源）
- **维护者**：Ryoichi Ando（ZOZO, Inc.）
- **论文**：ACM TOG 2024

## 五、应用场景

1. **游戏开发**：布料仿真、碰撞检测
2. **影视特效**：服装/布料动画
3. **虚拟试穿**：电商服装可视化
4. **学术研究**：物理仿真算法研究
5. **AI 控制**：通过 MCP 用自然语言控制仿真