# text-to-cad 研究总结

> 仓库地址：https://github.com/earthtojake/text-to-cad
> 研究日期：2026-05-26

## 一、仓库概述

`text-to-cad` 是一个 AI 驱动的 CAD（计算机辅助设计）/ 机器人描述文件生成工具集，通过自然语言描述让编码 Agent（Codex、Claude Code 等）生成受版本控制的 CAD 模型。支持 STEP、STL、3MF、DXF、GLB 等常见 CAD 格式导出，以及 URDF、SRDF、SDF 等机器人描述文件。

## 二、核心能力

### 2.1 Skills 列表

| Skill | 功能 |
|---|---|
| **CAD** | 生成 CAD 模型（STEP/STL/3MF/DXF/GLB）、拓扑数据、渲染图片、`@cad[...]` 几何引用 |
| **Render** | 启动 CAD Explorer 查看器，返回视觉审查链接和快照 |
| **step.parts** | 从 step.parts 查找、评估、下载标准件（螺丝螺母轴承电机等） |
| **URDF** | 生成机器人 URDF 描述（连杆/关节/限制/验证/可视化） |
| **SRDF** | MoveIt2 SRDF 语义、IK 求解、路径规划 |
| **SDF** | 生成 SDFormat/SDF 仿真模型/世界文件 |
| **SendCutSend** | SendCutSend.com DXF/STEP 上传预处理（材料/SKU/服务/二次操作） |

### 2.2 工作流程

```
描述 → 编辑源码 → 再生目标文件 → 检查 CAD 模型 → 引用几何 → 提交
```

1. **Describe** - 告诉 Agent 想要的零件/装配/机器人/机构
2. **Edit** - 让编码 Agent 更新本地 CAD 源码文件
3. **Regenerate** - 生成明确的 STEP/STL/3MF/DXF/GLB/URDF/SRDF/SDF 目标
4. **Inspect** - 打开 CAD Explorer 审查生成模型
5. **Reference** - 复制 `@cad[...]` 句柄进行几何感知的后续编辑
6. **Commit** - 将源码和生成产物一起保存

### 2.3 性能基准

仓库内置 10 个 CAD 基准测试，涵盖：

| # | 目标 | 难度 |
|---|---|---|
| 1 | 带四孔的矩形校准块 | 基础 |
| 2 | 带螺栓孔模式的圆形法兰 | 基础 |
| 3 | 带加强筋和两方向孔的 L 支架 | 中等 |
| 4 | 带键槽的阶梯轴 | 中等 |
| 5 | 带支座的开放顶电子外壳 | 中等 |
| 6 | 带减重切口的航空航天索具支架 | 复杂 |
| 7 | 带冷却片的径向发动机气缸 | 复杂 |
| 8 | 带后弯叶片的离心叶轮 | 复杂 |
| 9 | 带螺旋扶手的螺旋楼梯 | 复杂 |
| 10 | 简化行星齿轮级 | 复杂 |

## 三、技术架构

### 3.1 技术栈

- **CAD 内核**：build123d（基于 OpenCascade 的 Python CAD 库）+ OCP（OpenCascade Python binding）
- **Web 查看器**：Three.js + WebGL（CAD Explorer）
- **Agent 接口**：Claude Code / Codex 兼容 Skill 系统
- **安装方式**：`npx skills add earthtojake/text-to-cad`
- **本地化**：所有文件本地生成，无后端依赖

### 3.2 目录结构

```
skills/
  cad/          # CAD 核心 skill（build123d + OCP）
  render/       # CAD Explorer WebGL 查看器
  step-parts/   # 标准件库查找
  urdf/         # 机器人描述生成
  srdf/         # MoveIt2 语义
  sdf/          # 仿真格式
  sendcutsend/  # SendCutSend 板材加工预处理
harness/        # AGENTS.md / CLAUDE.md（CAD 项目级指令）
benchmarks/     # 10 个基准测试（含 GIF 渲染结果）
docs/           # 文档
assets/         # 演示 GIF
```

### 3.3 CAD 核心依赖

- `build123d`：Python 几何建模内核
- `OCP`（OpenCascade）：工业级 CAD 格式（STEP/STP/IGES）读写
- `numpy-stl`：STL 文件处理
- `trimesh`：网格处理和 GLB 导出

### 3.4 关键设计

1. **源码受控**：CAD 源码（Python build123d 脚本）受 Git 版本控制，而非 CAD 二进制文件
2. **显式目标**：生成明确的 STEP/STL/3MF/DXF/GLB 目标文件，不依赖自动推导
3. **harness 机制**：`harness/AGENTS.md` 和 `harness/CLAUDE.md` 可复用到其他 CAD 项目
4. **本地查看器**：CAD Explorer 为纯前端 WebGL，无须后端服务

## 四、实际应用场景

1. **AI 生成机械零件**：自然语言描述 → 程序员 Agent 生成 build123d Python 脚本 → 导出 STEP/STL
2. **机器人描述生成**：描述机器人结构 → 生成 URDF/SRDF/SDF → MoveIt2 运动规划
3. **标准件复用**：通过 step.parts 搜索螺栓/轴承/电机等标准件并集成
4. **钣金加工**：SendCutSend skill 直接输出可直接加工的 DXF 文件
5. **CAD 协作**：通过 `@cad[...]` 引用机制让 AI 进行精确的几何感知编辑

## 五、项目信息

- **Stars**：4850（非常高）
- **Forks**：553
- **语言**：JavaScript（Skills/渲染）+ Python（CAD 生成）
- **许可证**：MIT
- **主页**：https://www.cadskills.xyz
- **创建时间**：2026-04-22
- **Topics**：text-to-cad、cad、robotics、build123d、opencascade、step/stl/dxf/3mf/urdf/srdf/sdf 格式

## 六、与 codedb-mcp 的潜在结合

两个项目同属重点关注（⭐），可以在以下方向结合：
- `codedb-mcp` 为 `text-to-cad` 的 build123d Python 源码提供毫秒级代码搜索和引用查找
- AI 生成 CAD 脚本时，`codedb-mcp` 可以快速定位相关几何 API 的用法
- 两个项目都支持 skills 机制，可整合为统一的 AI 硬件设计工作台