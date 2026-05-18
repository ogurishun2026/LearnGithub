# Unreal_mcp 研究总结

> 仓库地址：https://github.com/ChiR24/Unreal_mcp
> 研究日期：2026-05-18

## 一、仓库概述

Unreal_mcp 是一个全面的 Model Context Protocol (MCP) 服务器，让 AI 助手（如 Claude、Cursor）能够通过 MCP 协议直接控制 Unreal Engine 5（5.0–5.7）。由 TypeScript MCP 服务端 + 原生 C++ UE 插件组成，实现了 AI 驱动的虚幻引擎全流程自动化。623 Stars，MIT 许可证。

## 二、核心内容

### 架构设计

项目采用双端架构：

1. **TypeScript MCP 服务端**（`src/`）：标准 MCP 协议服务端，连接 AI 客户端
2. **C++ UE 原生插件**（`plugins/McpAutomationBridge/`）：运行在 UE 编辑器内，通过 WebSocket 与 MCP 服务端通信

通信流程：`AI 客户端 → MCP 协议 → TypeScript 服务端 → WebSocket → C++ UE 插件 → UE 编辑器操作`

### 36 个 MCP 工具（按类别）

#### 核心工具 (core)
| 工具 | 功能 |
|------|------|
| `manage_pipeline` | 构建自动化，UnrealBuildTool 编译控制 |
| `manage_tools` | 运行时动态启用/禁用工具和工具类别 |
| `manage_asset` | 资产管理：创建、导入、复制、重命名、删除、材质编辑 |
| `manage_blueprint` | 蓝图创建、编辑、图节点操作 |

#### 世界操作 (world)
| 工具 | 功能 |
|------|------|
| `control_actor` | Actor 生成/删除/变换/物理/标签/组件 |
| `control_editor` | PIE 会话控制、相机、视口、截图、书签 |
| `manage_level` | 关卡加载/保存、流式加载、World Partition、Data Layers |
| `build_environment` | 环境构建：地形、植被、体积、大气 |

#### 创作 (authoring)
| 工具 | 功能 |
|------|------|
| `animation_physics` | 动画蓝图、状态机、布娃娃物理、载具、约束 |
| `manage_sequence` | Sequencer：过场动画、时间轴、摄像机动画、关键帧 |
| `manage_material_authoring` | 材质图节点编辑：添加/连接/删除节点 |
| `manage_effect` | Niagara 粒子系统、GPU 模拟、程序化特效 |
| `manage_audio` | 音频：Sound Cue、混音、环境音、MetaSound |
| `manage_texture` | 纹理导入、处理、导出 |
| `manage_skeleton` | 骨骼、骨骼网格体操作 |
| `manage_geometry` | 几何体脚本（GeometryScripting） |
| `manage_widget_authoring` | UMG Widget 创作 |

#### 游戏玩法 (gameplay)
| 工具 | 功能 |
|------|------|
| `manage_behavior_tree` | 行为树图编辑 |
| `manage_ai` | AI/EQS/StateTree 操作 |
| `manage_character` | 角色系统 |
| `manage_combat` | 战斗系统 |
| `manage_gas` | Gameplay Ability System |
| `manage_inventory` | 物品栏系统 |
| `manage_interaction` | 交互系统 |
| `manage_game_framework` | 游戏框架（GameMode/PlayerState 等） |
| `manage_input` | Enhanced Input 系统 |

#### 工具类 (utility)
| 工具 | 功能 |
|------|------|
| `system_control` | 控制台命令、CVars、项目设置、日志 |
| `inspect` | 调试检查、性能分析 |
| `manage_lighting` | 光照系统控制 |
| `manage_performance` | 性能分析优化 |
| `manage_networking` | 网络会话、在线子系统 |
| `manage_sessions` | 游戏会话管理 |
| `manage_level_structure` | 子关卡、关卡流式结构 |
| `manage_volumes` | 体积（触发器、物理体积等） |
| `manage_navigation` | 导航网格、NavMesh |
| `manage_splines` | 样条曲线 |

### C++ UE 插件能力

C++ 插件按功能域拆分为 60+ Handler 文件，覆盖：
- 资产查询/工作流、蓝图创建/图编辑/列表
- 动画、音频创作、行为树
- 角色、战斗、GAS、物品栏、交互
- 控制台命令、调试、环境、植被、地形
- 几何体、输入、光照、日志、材质图
- 网络、Niagara 图、性能、渲染
- Sequencer、会话、骨架、样条线
- 纹理、UI、体积、World Partition
- 属性反射、WebSocket 通信、连接管理

### 关键设计特点

1. **优雅降级**：即使没有 UE 连接，服务端也能启动
2. **按需连接**：指数退避重试自动化握手
3. **命令安全**：基于模式验证阻止危险控制台命令
4. **资产缓存**：10 秒 TTL 提升性能
5. **速率限制**：Prometheus 端点按 IP 限制（60 req/min）
6. **动态类型发现**：运行时反射获取灯光、调试形状、Sequencer 轨道类型
7. **运行时工具管理**：`manage_tools` 可动态启用/禁用工具和类别
8. **Docker 支持**：提供 Dockerfile 和部署配置

## 三、技术架构

### 目录结构

```
Unreal_mcp/
├── src/                          # TypeScript MCP 服务端
│   ├── cli.ts                    # CLI 入口
│   ├── server/                   # MCP 服务端
│   ├── tools/                    # 工具定义与处理
│   │   ├── consolidated-tool-definitions.ts   # 36 个工具定义
│   │   ├── consolidated-tool-handlers.ts      # 统一处理器
│   │   ├── dynamic-tool-manager.ts            # 运行时工具管理
│   │   ├── schemas/                           # JSON Schema
│   │   └── handlers/                          # 按功能域的处理函数
│   ├── automation/               # UE 自动化桥接
│   ├── config/                   # 配置
│   ├── services/                 # 服务层
│   ├── resources/                # MCP Resources
│   └── types/                    # TypeScript 类型
├── plugins/
│   └── McpAutomationBridge/      # C++ UE 原生插件
│       └── Source/McpAutomationBridge/
│           ├── Private/          # 60+ Handler 实现
│           │   ├── MCP/          # MCP 协议层
│           │   └── Mcp*Handlers.cpp  # 按域拆分的处理器
│           └── Public/           # 公共头文件
├── docs/                         # 文档
├── tests/                        # Vitest 测试
└── Public/                       # 安装视频和图标
```

### 技术栈

| 维度 | 技术 |
|------|------|
| MCP 服务端 | TypeScript + MCP SDK |
| UE 插件 | C++ (UE 5.0–5.7) |
| 通信协议 | WebSocket（服务端 ↔ UE 插件） |
| 运行时 | Node.js 18+ |
| 测试 | Vitest |
| 构建 | npm / npx |
| 容器化 | Docker |
| 许可证 | MIT |

### 安装方式

1. **NPX 即用**（推荐）：`npx unreal-engine-mcp-server`
2. **克隆构建**：`npm install && npm run build && node dist/cli.js`
3. **UE 插件**：复制 `plugins/McpAutomationBridge/` 到项目 Plugins 目录

## 四、实际应用场景

1. **AI 驱动的游戏开发**：用 Claude/Cursor 等通过自然语言操控 UE，自动化场景搭建、资产导入、蓝图编写
2. **自动化测试流水线**：通过 `manage_pipeline` 触发构建，`system_control` 运行测试命令
3. **快速原型验证**：AI 助手直接在 UE 中创建关卡、放置 Actor、配置材质和光照
4. **教学内容生成**：AI 读取场景信息、生成教程文档
5. **批量资产处理**：通过 `manage_asset` 批量重命名、导入、整理资产
6. **过场动画制作**：通过 `manage_sequence` 用自然语言描述来编排摄像机动画
