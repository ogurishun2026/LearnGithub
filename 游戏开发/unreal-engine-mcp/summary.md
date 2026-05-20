# unreal-engine-mcp 研究总结

> 仓库地址：https://github.com/flopperam/unreal-engine-mcp
> 研究日期：2026-05-20

## 一、仓库概述

通过自然语言控制 Unreal Engine 5.5+ 的 MCP 服务器。使用 AI 构建令人惊叹的 3D 世界和建筑杰作——创建整个城镇、中世纪城堡、现代豪宅、挑战性迷宫和复杂结构。

**核心定位**：将 AI Agent（如 Cursor、Claude Code）接入 Unreal Engine 编辑器，通过自然语言命令操控游戏引擎，无需手动操作界面。

## 二、核心内容

### 2.1 支持的功能领域

| 领域 | 工具数 | 功能说明 |
|------|--------|----------|
| **Scene & Level** | 8 | 场景查询、Actor操作、资产搜索、项目上下文 |
| **Blueprint 读取** | 3 | BP概览、检查、导出 |
| **Blueprint 创作** | 12 | 创建Actor/Pawn/Character、变量/组件/节点/连线CRUD |
| **Materials & Shading** | 2 | 材质检查与编辑 |
| **VFX** | 3 | Niagara粒子、VFX编辑、Chaos破碎 |
| **Animation** | 5 | 动画检查、编辑、IK绑骨、重定向 |
| **UMG / Widgets** | 2 | UI组件树检查与编辑 |
| **AI & Ability System** | 3 | 行为树、Gas编辑、标签注册 |
| **Landscape & Foliage** | 4 | 地形塑造、植被编辑 |
| **Cinematics & Audio** | 3 | 序列编辑器、音频编辑 |
| **Procedural (PCG)** | 1 | 程序化内容生成 |
| **Data Assets** | 1 | 数据资产工厂 |
| **Editor & Diagnostics** | 5 | 编辑器操作、日志、性能审计、截图 |
| **Runtime Verification** | 2 | PIE测试 |
| **Execution** | 3 | Python执行、API查询、Skill加载 |

**总计：50+ 工具**

### 2.2 核心工作流

```
1. Orient    → bp_brief / scene_brief / search_assets / project_context
2. Execute   → 使用对应领域的工具
3. Verify    → 重新检查 + PIE测试
```

### 2.3 效率规则

- **批量操作**：所有接受数组的工具都设计为单次调用多项
- **并行调用**：独立工具可并行调用
- **使用过滤器**：inspect类工具支持compact模式+过滤器
- **延迟编译**：窄范围bp_*写操作延迟编译，批量后统一`bp_commit`

## 三、技术架构

### 3.1 项目结构

```
unreal-engine-mcp/
├── .cursor-plugin/
│   └── plugin.json           # Cursor插件配置
├── .cursor/
│   └── rules/
│       └── unreal-mcp-shapes-guide.mdc  # Cursor规则
├── skills/                   # AI Skill文档
│   ├── blueprint-authoring/  # Blueprint创作技能
│   ├── material-vfx/         # 材质与VFX技能
│   ├── scene-building/       # 场景构建技能
│   └── unreal-mcp-overview/  # 总览与工作流
├── assets/                   # 演示图片
├── DEBUGGING.md             # 调试文档
└── README.md
```

### 3.2 技术特点

| 特性 | 说明 |
|------|------|
| **通信方式** | WebSocket 连接运行中的 Unreal Editor |
| **Editor 版本** | Unreal Engine 5.5+ |
| **插件架构** | Cursor 官方插件格式 (.cursor-plugin) |
| **Skill 系统** | Markdown 格式 Skill 文档 |
| **付费分层** | 部分高级功能（Blueprint创作、Python执行）需要付费 |

### 3.3 认证层级

| 功能 | Tier |
|------|------|
| 场景查询、资产搜索、项目上下文 | 免费 |
| Blueprint 读取 (brief/inspect/export) | 免费 |
| Blueprint Authoring (创建/变量/组件/节点) | **付费** |
| PIE Test (Blueprint) | **付费** |
| Python Execution | **付费** |
| Unreal API (15000+ 签名查询) | **付费** |

## 四、与 unity-mcp 的对比

| 维度 | unreal-engine-mcp | unity-mcp |
|------|-------------------|-----------|
| **游戏引擎** | Unreal Engine 5.5+ | Unity |
| **Stars** | 948 | 9,700 |
| **架构** | WebSocket (编辑器内运行) | MCP 服务器 |
| **工具数** | 50+ | 39 |
| **AI 绑定** | Cursor 插件 | 通用 MCP |
| **付费模式** | 部分功能付费 | 免费 |

## 五、Star 历史与社区

- **Stars**: 948 (截至 2026-05-20)
- **语言**: C++ (Unreal Engine 插件)
- **许可**: MIT
- **定位**: 商业产品 (flopperam.com)
- **更新时间**: 2026-05-20

## 六、总结

unreal-engine-mcp 是 Unreal Engine 的 AI 控制桥梁，通过 MCP 协议将 AI Agent 接入编辑器。相比 unity-mcp (9.7K Stars)，它还处于早期阶段但功能覆盖面广。

**亮点**：
- 50+ 工具覆盖 UE 开发的各个方面
- Cursor 官方插件支持
- 分层付费模式（免费功能足够入门）
- WebSocket 实时连接编辑器

**注意**：这是一个商业项目的开源部分，核心高级功能需要付费。

**适用场景**：
- 使用 Cursor 的 UE 开发者
-希望通过自然语言操控 UE 场景和资产
- 需要批量处理 Blueprint 资产的自动化工作流
