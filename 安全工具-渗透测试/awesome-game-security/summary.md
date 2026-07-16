# awesome-game-security 研究总结

> 仓库地址：https://github.com/gmh5225/awesome-game-security
> 研究日期：2026-07-16

## 一、仓库概述

**awesome-game-security** 是一个 3.1K+ Stars 的游戏安全资源大全，涵盖游戏逆向工程、反作弊研究、内核安全、移动平台安全等多个领域。该仓库提供了 **AI Agent Skills 系统**，可直接集成到 Claude Code、Cursor、Codex CLI 等 AI 编码助手，提供专业游戏安全知识。

仓库特点：
- **4500+ 行 README**，内容极其丰富
- **AI Skills 集成**：9 个专业技能包可供安装
- **跨平台覆盖**：Windows / Linux / Android / iOS / 主机平台
- **攻防双向**：同时包含 Cheat 技术和 Anti-Cheat 研究

---

## 二、核心内容

### 1. AI Agent Skills（创新特性）

仓库提供 9 个专业 Skills，可直接安装到 AI 编码助手：

| Skill | 描述 |
|-------|------|
| `anti-cheat-systems` | 现代 AC 架构、检测权衡、EAC/BE/Vanguard/FACEIT 研究等 |
| `dma-attack-techniques` | PCIe DMA 威胁建模、FPGA 内存访问、IOMMU 约束等 |
| `game-engine-resources` | Unreal/Unity/Source/Godot 引擎内部、源码、插件等 |
| `game-hacking-techniques` | 作弊实现威胁模型：用户态/内核态/虚拟机/DMA/覆盖层等 |
| `graphics-api-hooking` | DirectX/OpenGL/Vulkan 拦截、覆盖渲染、Swap-Chain 分析等 |
| `mobile-security` | Android/iOS 逆向、Frida/Zygisk/Magisk、越狱/Root 绕过等 |
| `reverse-engineering-tools` | 逆向工程工具：用户态/内核态调试器、Dump 分析等 |
| `windows-kernel-security` | Windows 内核安全：回调、MMVAD、IOCTL、DSE、PatchGuard 等 |
| `awesome-game-security-overview` | 仓库分类映射、贡献指南、导航 |

**安装方式**：
```bash
npx skills add https://github.com/gmh5225/awesome-game-security --skill <skill-name>
```

### 2. 游戏引擎资源（Game Engine）

- **指南资源**：Game-Programmer-Study-Notes、custom_game_engines、awesome-game-engine-dev 等
- **源码仓库**：
  - Unreal Engine、Unity C# Reference、Cocos2d-x
  - Source Engine（2003/2007/OrangeBox）、GoldSource Rebuild
  - Godot、Bevy (Rust)、Fyrox (Rust)、Ambient (Rust)
  - Half-Life SDK、Quake3、OpenArena 等
- **引擎插件**：
  - Unreal：Rider 集成、FlowGraph、ImGui 集成、.NET 6 集成等
  - Unity：ChatGPT 集成、Cursor 编辑器集成、CLI 控制 (UniCli)
  - Godot：沙盒化 Modding 支持

### 3. 逆向工程工具（RE Tools）

**调试器**：
- Cheat Engine（含 DMA/Android/iOS 版本）
- x64dbg、WinDbg、IDA Pro、Ghidra、Binary Ninja、Radare2
- HyperDbg、HyperHide（虚拟机调试）
- LLDB/eBPF 调试器（Android/Linux）

**反编译器**：
- IDA Pro + 大量插件（MCP 集成、AI 集成、签名生成等）
- Ghidra + 插件（MCP 集成、Yara、去混淆）
- Binary Ninja + 插件（MCP 集成、符号执行）
- Recaf、Jadx、dnSpy（.NET/Java）

**IDA Pro 插件精选**：
- IDA-MCP（AI Agent 集成）
- NtRays（Windows 内核增强）
- FindFunc（模式识别）
- GhidraDec（Ghidra 反编译集成）
- Gepetto/DAILA（ChatGPT 集成）

### 4. 游戏作弊技术（Cheat）

**教程与指南**：
- dsasmblr/game-hacking
- guided-hacking.com
- unknowncheats.me
- gamehacking.academy
- secret.club / back.engineering / triplefault.io

**调试技术**：
- VEH Hook、硬件断点
- 虚拟机调试绕过（TitanHide、HyperHide）
- Intel PT / AMD IBS 追踪
- eBPF 调试器（Android/Linux）

**注入技术**：
- Manual Map 注入器（btbd/smap、kdmapper）
- 内核 DLL 注入（APC、PTE.User、线程劫持）
- EFI 注入（umap、sumap）
- Android 注入（Zygote、Ptrace、LD_Preload）

**Hook 框架**：
- MinHook、Detours、PolyHook
- 内核 Hook（Dobby、LightHook）
- ARM64 Hook（And64InlineHook、BWSR）
- eBPF Hook（abyss）

### 5. 反作弊系统（Anti-Cheat）

**研究资源**：
- areweanticheatyet.com（AC 兼容性列表）
- 各 AC 系统研究（EAC、BE、Vanguard、FACEIT）

**绕过技术**：
- 内核回调移除（CheekyBlinder、DCMB）
- PatchGuard 绕过
- DSE 绕过（DSE-Patcher、BootBypass）
- HVCI 绕过

### 6. Windows 内核安全

**核心概念**：
- 内核回调（Process/Thread/Image/Registry）
- MMVAD / VAD 树
- IOCTL 路径
- PatchGuard 机制
- DSE（驱动签名强制）
- PiDDBCache

**工具**：
- OpenArk、WinArk（系统分析）
- KDU（Kernel Driver Utility）
- Process Hacker / System Informer
- InfinityHook（ETW Hook）

### 7. 移动平台安全（Android/iOS）

**Android**：
- Magisk / KernelSU / APatch（Root 框架）
- Zygisk（进程注入框架）
- Frida（动态插桩）
- eBPF 调试器
- 内核驱动开发模板
- DMA 设备支持

**iOS**：
- 越狱工具（Dopamine、palera1n、TrollStore）
- Frida 注入
- 内核 Hook（xnuspy）
- Objective-C Runtime 分析

### 8. DMA（直接内存访问）

**硬件**：
- PCILeech-FPGA（Squirrel、Captain、Enigma）
- DMA 固件（QuantumStealth、Fullstealth）

**软件**：
- MemProcFS
- Cheat Engine DMA 插件
- ReClass DMA
- DMA 库（DMALib、Spuckwaffel/DMALib）

**绕过技术**：
- MSI-X 中断绕过
- VMD 伪装
- Intel I226-V 仿真

### 9. MCP（Model Context Protocol）集成

**逆向工程 MCP**：
- ida-pro-mcp、ida-mcp-server（IDA Pro）
- GhidraMCP、GhidrAssistMCP（Ghidra）
- binary_ninja_mcp（Binary Ninja）
- x64DbgMCPServer（x64dbg）
- Cheat Engine MCP 插件

**游戏引擎 MCP**：
- unreal-mcp、UE5-MCP
- unity-mcp、mcpup
- vibe-blocks-mcp（Roblox）

**分析工具 MCP**：
- MemMCP（类 CE 的 MCP 工具）
- ProcessHacker MCP
- GDB MCP、WinDBG MCP

---

## 三、技术架构

### 目录结构

```
awesome-game-security/
├── README.md           # 主文档（4500+ 行）
├── .claude/            # Claude Code 配置
├── .github/            # GitHub Actions
├── archive/            # 归档资源
├── description/        # 分类描述
├── scripts/            # 辅助脚本
├── wiki/               # AI Agent 知识库
│   └── AGENTS.md       # Agent 导航指南
└── awesome-image.webp  # NFT 图片
```

### 关键依赖

- **主要语言**：Python（自动化脚本）
- **协议**：MIT License
- **官方网站**：https://gs.awesome.rip

### 设计特点

1. **分类细致**：50+ 分类，涵盖游戏开发到逆向工程全流程
2. **AI First**：原生支持 AI Agent，提供结构化 Skills
3. **社区驱动**：欢迎 PR，持续更新（最近更新：2026-07-16）
4. **跨平台**：Windows / Linux / Android / iOS / 主机全覆盖

---

## 四、实际应用场景

### 1. 游戏安全研究

- **学习路径**：从游戏引擎 → 逆向工程 → 作弊实现 → 反作弊研究
- **工具获取**：一站式获取各类逆向/调试工具

### 2. AI Agent 集成

- **技能安装**：通过 `npx skills add` 安装专业技能包
- **MCP 集成**：让 AI Agent 直接操作 IDA/Ghidra/Binary Ninja

### 3. 内核安全研究

- **Windows 内核**：回调、PatchGuard、DSE、驱动通信
- **Linux 内核**：eBPF、Rootkit 检测
- **Android 内核**：GKI 驱动开发、KernelSU

### 4. 移动游戏逆向

- **Android**：Magisk/Zygisk 模块、Frida 脚本、内核驱动
- **iOS**：越狱、Runtime 分析、Hook 框架

### 5. DMA 硬件研究

- **硬件选购**：FPGA 板卡推荐
- **固件定制**：绕过各种 AC 检测
- **软件集成**：CE、ReClass、MemProcFS

---

## 五、亮点总结

| 维度 | 特点 |
|------|------|
| **规模** | 4500+ 行 README，涵盖 50+ 分类 |
| **AI 集成** | 9 个专业 Skills，支持 Claude Code/Cursor/Codex |
| **MCP 支持** | IDA/Ghidra/Binja/CE/x64dbg 全覆盖 |
| **平台覆盖** | Windows/Linux/Android/iOS/主机全覆盖 |
| **攻防双向** | Cheat 技术和 Anti-Cheat 研究并存 |
| **社区活跃** | 3.1K Stars，持续更新 |

---

## 六、推荐使用方式

1. **AI Agent 用户**：直接安装 Skills，获取专业知识
2. **安全研究员**：作为工具索引，快速定位所需资源
3. **游戏开发者**：了解攻击手段，设计更好的防御
4. **学习者**：按分类循序渐进学习游戏安全知识