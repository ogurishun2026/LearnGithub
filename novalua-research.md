---
name: novalua-research
description: NovaLua（ZLua）深度研究 —— Unity Il2Cpp 极致优化的原生 Lua 方案
metadata:
  type: reference
---

**ZLua**（原名 NovaLua）是一个针对 **Unity Il2Cpp 极致优化的现代原生 Lua 方案**。核心创新是在 **C++ 层面让 Il2Cpp 和 Lua 虚拟机直接相互操作**，绕开了传统方案中低效的 C# 交互接口。

仓库地址：`https://github.com/focus-creative-games/novalua`

## 为什么重要（Why）

对**游戏开发自动化 Agent**有重要参考价值。ZLua 展示了如何在 Unity 中深度集成脚本系统，让 AI Agent 可以控制游戏逻辑。Il2Cpp C++ 层面的桥接设计是高性能游戏脚本系统的标杆实现，对需要"AI 驱动游戏内容生成"的场景（如 AI 生成关卡、AI 控制 NPC）提供了高效的运行时基础。

## 技术栈

| 维度 | 详情 |
|------|------|
| 语言 | C#（Runtime/Mono + Runtime/Il2Cpp）+ C++（ZLua~/libil2cpp-2022/） |
| 目标平台 | Unity 2021+ LTS（Mono / Il2Cpp），含 WebGL、微信小游戏、鸿蒙、车机 |
| Lua 版本 | 5.1、5.3、5.4、5.5、LuaJIT、Luau |
| DLL 修改 | dnlib（编译后注入 IL） |
| 许可证 | MIT |

## 核心设计目标

类比于 P/Invoke、MonoPInvokeCallback、MarshalAs，ZLua 提出了对应概念：

| C# 互操作概念 | ZLua 对应概念 | 用途 |
|-------------|-------------|------|
| P/Invoke | **L/Invoke**（`[LuaInvoke]`） | C# 调用 Lua 函数 |
| MonoPInvokeCallback | **MonoLuaCallback**（`[LuaCallback]`） | Lua 调用 C# 函数 |
| MarshalAs | **LuaMarshalAs**（`[LuaMarshalAs]`） | 参数/返回值类型编排 |

## 架构

ZLua 实现了**两套代码**，分别对应 Editor 和 Player：

```
Editor / Mono 模式          Player / Il2Cpp 模式
─────────────────────       ─────────────────────────
ZLua.Mono                   ZLua.Il2Cpp（极薄 C# 门面）
  ├─ LuaMonoAppDomain       ├─ LuaIl2CppAppDomain
  ├─ LuaEnv（P/Invoke）     ├─ InitializeInternal [InternalCall]
  ├─ 反射绑定                └─ C++ MethodBridge（直接调用）
  └─ 生成 C# wrapper
```

### C++ 层核心模块

| 模块 | 职责 |
|------|------|
| LuaEnv | Lua 状态管理 |
| LuaInteropManager | 互操作管理 |
| LuaInvokeRuntime | `[LuaInvoke]` 运行时 |
| Marshaling | 类型编列 |
| ObjectRegistry | 托管对象注册（注册到 Il2Cpp GCRoots） |
| MethodBridge | 按签名复用的 C++ 桥接函数 |

## 性能优势（相比 xLua）

| 优化点 | 原理 | 效果 |
|--------|------|------|
| **对象查找** | UserData 中直接包含对象指针，无需 pool index 查找 | **10 倍以上** |
| **字段访问** | C++ 层直接 `obj + 偏移` 访问内存，不经过 C# wrapper | **10 倍以上** |
| **属性访问** | C++ 层直接调用 Property 函数，不经过 C# wrapper | 大幅优化 |
| **函数调用** | C++ 层通过 `methodPointer` 直接调用 Il2Cpp 生成体 | 大幅优化 |
| **引用维护** | C++ 层维护对象列表并注册到 GCRoots | **数倍以上** |
| **桥接大小** | 相同签名的函数共享同一个桥接函数，不生成 C# wrapper | 彻底解决 wrapper 膨胀问题 |

## 使用示例

C# 端（标记 `[LuaInvoke]`）：
```csharp
[LuaInvoke("app", "main")]
private static extern void AppMain();

[LuaInvoke("app", "add")]
private static extern int AppAdd(int a, int b);
```

Lua 端（访问 C# 类）：
```lua
local demo = CSharp['Assembly-CSharp'].Demo()
demo:SetX(10)
print(demo.x)  -- 10
demo:Run(20)   -- 调用成员函数
```

## 当前状态

- 早期 MVP 阶段，仅在 Unity 2022.3.62f3 + Lua 5.4 上测试通过
- 基础交互已可用，功能远未完善
- **预计 2026 年 8 月发布正式版**

## 如何应用（How to apply）

1. **游戏脚本系统**：为 Unity 游戏提供高性能 Lua 脚本支持，让 AI Agent 可以控制游戏逻辑
2. **AI 驱动内容生成**：AI 生成关卡、AI 控制 NPC 等场景的高性能运行时基础
3. **Il2Cpp 桥接设计参考**：C++ 层直接桥接 Il2Cpp ↔ Lua 的设计是高性能绑定方案的标杆

## 相关记忆

- [[spark-research]] — 3D 渲染器，可与 ZLua 组合用于游戏开发（ZLua 提供脚本，Spark 提供渲染）
- [[ai-game-studio-deep-dive]] — 序列帧动画生成工具，同属游戏开发方向
