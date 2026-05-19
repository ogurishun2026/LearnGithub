# unity-mcp 研究总结

> 仓库地址：https://github.com/CoplayDev/unity-mcp
> 研究日期：2026-05-19

## 一、仓库概述

**MCP for Unity**（原名 unity-mcp）是一个开源的桥接工具，通过 Model Context Protocol（MCP）让 AI 助手（Claude、Cursor、VS Code Copilot 等）直接控制 Unity Editor。它为 LLM 提供了一套完整的工具集，可以管理资源、控制场景、编辑脚本、自动化任务等。

| 基础信息 | 值 |
|---------|-----|
| Stars | 9,753 |
| 主要语言 | C# + Python |
| 最新版本 | v9.6.3 (beta) |
| License | MIT |
| 赞助商 | Aura (AI assistant for Unreal & Unity) |

## 二、核心内容

### 2.1 功能定位

MCP for Unity 填补了 AI 助手与 Unity Editor 之间的鸿沟，让 LLM 能够：
- **创建和修改游戏对象**（GameObjects、Prefabs、Materials）
- **管理场景**（加载、保存、切换场景）
- **编辑脚本**（创建、修改 C# 脚本）
- **运行测试**（Unity Test Framework 集成）
- **控制编辑器**（执行菜单项、读取控制台）
- **自动化工作流**（批处理、批量执行）

### 2.2 支持的 AI 客户端

| 客户端 | 支持情况 |
|--------|---------|
| Claude Desktop | ✅ HTTP |
| Claude Code | ✅ HTTP |
| Cursor | ✅ HTTP |
| VS Code Copilot | ✅ HTTP |
| Windsurf | ✅ HTTP |
| OpenClaw | ✅ stdio + HTTP |
| GitHub Copilot CLI | ✅ HTTP |

### 2.3 可用工具（39个）

**核心工具组（core）：**
- `manage_asset` - 资源管理（创建/删除/查询）
- `manage_gameobject` - GameObject 操作
- `manage_material` - 材质管理
- `manage_prefabs` - Prefab 管理
- `manage_scene` - 场景管理（加载/保存/多场景）
- `manage_script` - 脚本编辑（创建/修改/验证）
- `manage_texture` - 纹理资源管理
- `batch_execute` - 批量执行（性能提升 10-100x）

**编辑器工具组：**
- `manage_editor` - 编辑器操作（Undo/Redo）
- `manage_camera` - 相机管理（含 Cinemachine 支持）
- `manage_components` - 组件管理
- `manage_ui` - UI 系统管理

**图形与特效：**
- `manage_graphics` - 图形设置（Volume/Post-processing/Light baking/URP）
- `manage_vfx` - VFX 粒子系统
- `manage_animation` - 动画系统

**物理系统：**
- `manage_physics` - 物理引擎（21个动作：碰撞矩阵、物理材质、关节、射线检测等）

**构建与部署：**
- `manage_build` - 播放器构建（多平台批量构建）

**包管理：**
- `manage_packages` - Unity Package Manager（安装/移除/搜索包）

**调试与性能：**
- `manage_profiler` - Profiler 会话控制、帧计时、内存快照
- `read_console` - 读取控制台日志

**其他：**
- `execute_menu_item` - 执行任意编辑器菜单项
- `find_gameobjects` - 按名称/标签/层级查找对象
- `find_in_file` - 文件内搜索
- `run_tests` / `get_test_job` - 测试运行
- `refresh_unity` - 刷新 Unity（相当于点击 Play）

### 2.4 可用资源（26个）

`project_info` / `project_layers` / `project_tags` / `gameobject` / `gameobject_api` / `gameobject_component` / `gameobject_components` / `prefab_info` / `prefab_hierarchy` / `prefab_api` / `cameras` / `volumes` / `renderer_features` / `rendering_stats` / `editor_selection` / `editor_state` / `editor_windows` / `editor_active_tool` / `editor_prefab_stage` / `menu_items` / `tool_groups` / `unity_instances` / `custom_tools` / `get_tests` / `get_tests_for_mode`

## 三、技术架构

### 3.1 双端架构

```
AI Assistant (Claude/Cursor)
         ↓ MCP Protocol (stdio/HTTP)
Python Server (Server/src/)
         ↓ WebSocket + HTTP
Unity Editor Plugin (MCPForUnity/)
         ↓ Unity Editor API
Scene, Assets, Scripts
```

**Python Server (`Server/`):**
- 框架：FastMCP
- 传输模式：Stdio（单客户端）或 HTTP（多客户端）
- 工具层：39个 MCP 工具，使用 `@mcp_for_unity_tool` 装饰器

**Unity C# Package (`MCPForUnity/`):**
- Editor 工具：对应 Python 工具的实现
- 资源层：提供只读状态给 AI
- 命令注册：通过反射自动发现 `[McpForUnityTool]` 特性

### 3.2 目录结构

```
unity-mcp/
├── Server/                      # Python MCP 服务器
│   └── src/
│       ├── services/
│       │   ├── tools/           # 39个 MCP 工具实现
│       │   └── resources/       # 资源提供器
│       └── cli/commands/        # CLI 命令（独立实现）
├── MCPForUnity/                  # Unity Editor Package
│   ├── Editor/
│   │   └── Tools/               # C# 工具实现
│   └── Runtime/Helpers/          # Unity API 兼容层
├── CustomTools/                  # 自定义工具模板
├── TestProjects/                # 测试项目
├── docs/                        # 文档
└── unity-mcp-skill/             # Claude Code Skill
```

### 3.3 关键技术点

**1. 多实例支持**
- 支持同时连接多个 Unity Editor 实例
- 通过 `set_active_instance` 切换目标实例
- 通过 `unity_instances` 资源查看所有实例

**2. 工具分组机制**
- 工具按组分类：`core`(默认启用)、`vfx`、`animation`、`ui`、`scripting_ext`、`testing`、`probuilder`、`profiling`、`docs`
- 通过 `manage_tools` 动态启用/禁用工具组

**3. Roslyn 脚本验证**
- 可选安装 Roslyn 编译器
- 支持严格的 C# 代码验证（检测未定义的命名空间、类型、方法）
- 提供一键安装器

**4. 性能优化**
- `batch_execute` 批量执行，比单独调用快 10-100x
- 分页机制处理大型层级数据

## 四、实际应用场景

### 4.1 游戏原型快速开发

**场景：** 想快速验证一个游戏机制原型

**AI 对话示例：**
```
用户: 创建一个红色的立方体作为玩家角色，再创建几个蓝色的球作为敌人
AI → MCP工具: manage_gameobject(create), manage_material(create)
用户: 给玩家添加跳跃能力和左右移动
AI → MCP工具: manage_script(create), manage_script(validate)
用户: 创建一个简单的AI，让敌人向玩家移动
AI → MCP工具: manage_script(create), manage_components(add)
```

### 4.2 自动化测试流水线

**场景：** 每次 PR 都需要跑一套冒烟测试

```bash
# AI 自动执行
1. manage_scene(load_scene, path="Assets/Tests/PlayMode/GameplayTests.unity")
2. run_tests(test_filter="GameplayTests.*")
3. read_console() → 检查是否有错误
4. manage_build(build_target=iOS) → 验证构建
```

### 4.3 批量资源处理

**场景：** 需要为 100 个角色创建不同的材质变体

```python
# batch_execute 一次性处理
batch_execute(commands=[
    {"tool": "manage_material", "params": {"action": "create", "name": "Hero_Red_Mat"}},
    {"tool": "manage_material", "params": {"action": "create", "name": "Hero_Blue_Mat"}},
    # ... 100个
])
```

### 4.4 多平台构建验证

**场景：** 游戏需要同时发布 iOS、Android、PC 版本

```bash
manage_build(
    action="batch_build",
    platforms=["iOS", "Android", "Windows"],
    build_profiles=["Release", "Debug"]
)
```

## 五、安装与配置

### 5.1 快速安装

**Step 1: Unity Package**
```
Window > Package Manager > + > Add package from git URL...
https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#main
```

**Step 2: 启动服务器**
```
Window > MCP for Unity > Start Server
```

**Step 3: 配置 AI 客户端**

HTTP 模式（Claude Desktop / Cursor / VS Code）:
```json
{
  "mcpServers": {
    "unityMCP": {
      "url": "http://localhost:8080/mcp"
    }
  }
}
```

### 5.2 前置要求

- Unity 2021.3 LTS+
- Python 3.10+ 和 uv 包管理器
- MCP 客户端（Claude Desktop / Claude Code / Cursor 等）

## 六、与 Unreal_mcp 的对比

| 维度 | unity-mcp | Unreal_mcp |
|------|-----------|------------|
| 目标引擎 | Unity | Unreal Engine 5 |
| 工具数量 | 39个 | 36个 |
| Stars | 9,753 | 较小 |
| 架构 | Python+C# 双端 | C++插件+TS服务端 |
| 语言方向 | C# 脚本 | C++/Blueprint |

## 七、总结与建议

**价值定位：**
MCP for Unity 是目前最成熟的 Unity AI 集成方案，9.7K+ Stars 已证明其社区认可度。它让 AI 从"只能给建议"升级到"能直接操控编辑器"，是游戏开发自动化的重要里程碑。

**对你的游戏开发的价值：**
1. **加速原型验证** — 用自然语言快速创建游戏对象和基础逻辑
2. **降低重复劳动** — 批量处理资源、批量构建、多平台发布
3. **AI 驱动开发** — Claude Code 可以直接操 Unity，无需手动复制粘贴代码
4. **工作流集成** — 可与现有 CI/CD 流水线结合

**推荐用法：**
- 实验性项目用 AI 生成代码框架
- 确定性代码保持手写（性能关键部分）
- 将 AI 视为"能执行 Unity API 的助手"而非"全权代理"

---

> 更多信息请参考：
> - [官方文档](https://github.com/CoplayDev/unity-mcp)
> - [Discord 社区](https://discord.gg/y4p8KfzrN4)
> - [Aura - Unity AI 助手](https://www.tryaura.dev/)
