# Codex-X 研究总结

> 仓库地址：https://github.com/yynxxxxx/Codex-X
> 研究日期：2026-07-16

## 一、仓库概述

**Codex-X** 是一个 1.15K Stars 的跨平台桌面工具，用于管理 **OpenAI Codex Desktop / Codex CLI**。它将提示词模板管理、API/Provider 切换、会话组织、Skills/MCP 管理整合到一个界面中，避免反复手动编辑配置文件。

仓库特点：
- **跨平台支持**：macOS / Windows / Linux 全覆盖
- **技术栈**：Tauri 2 + React 18 + TypeScript + Rust + SQLite
- **内置提示词库**：5 套"破甲"模板，支持 GitHub 同步
- **Provider 管理**：支持第三方 API 切换，cc-switch 导入
- **会话管理**：搜索、修复、永久删除本地会话

---

## 二、核心功能

### 1. 提示词模板中心

内置 5 套提示词模板，支持离线使用 + GitHub 自动同步：

| 模板 | 用途 | 特点 |
|------|------|------|
| `gpt5.5-unrestricted.md` | 日常编码与技术工作 | 紧凑通用型 |
| `gpt5.4-unrestricted.md` | GPT-5.4 / Codex CLI 工作流 | CTF 与安全研究导向 |
| `gpt5.5-jeli.md` | 工程与逆向工程工作流 | 完整流程，自然语言版 |
| `gpt-5.6-sol-unrestricted.md` | GPT-5.6 SOL 提示词 | 直接执行 + 双语任务 |
| `海鸥3.0破甲.md` | 中文技术操作员 | 编码/CTF/逆向/记忆/协议路由 |

**两种启用模式**：
- **保留原有提示词**：追加管理内容，禁用时移除，不影响用户原有配置
- **替换原有提示词**：将选定模板设为主入口，完全切换

### 2. Provider 切换与管理

- **多 Provider 保存**：始终可见当前激活的配置
- **连接测试**：切换前可测试 API 端点（使用 `/v1/models`）
- **cc-switch 导入**：支持从 cc-switch 导入配置，自动合并重复项
- **无需重启**：切换后新建或重新打开会话即可生效
- **配置编辑**：同一页面编辑 Base URL / API Key / Model / Wire API / 完整 TOML

### 3. 官方 Auth 管理

- 自动读取 Codex 官方 `auth.json`
- 查看 / 编辑 ChatGPT 登录状态
- 区分官方 Auth 与第三方 API Key
- 统一 UI 管理官方 Auth 和第三方 Provider

### 4. 可视化 TOML 编辑

- 查看当前 Codex `config.toml`
- 深色代码预览 + 语法高亮
- 从 Provider 编辑器直接编辑完整 TOML
- 保存变更到 Codex 配置目录

### 5. 会话管理

| 功能 | 说明 |
|------|------|
| **查找与组织** | 按标题或项目路径搜索，按项目分组；内部子会话默认不显示 |
| **检查与修复** | 检查本地会话是否匹配当前 Provider，手动或启动时自动修复 |
| **永久删除** | 单选/多选/项目级选择，确认后从 Codex 存储中硬删除（不可恢复） |

### 6. Skills / MCP 管理

- **Skills**：查看当前 Skills、导入现有内容、从 ZIP 安装、单独启用/禁用、检查更新
- **MCP**：导入前预览 MCP 服务器、选择 Codex-X 管理的项目、启用/禁用时维护 Codex 配置

### 7. 逆向 Skills 导航

在线指南网站：https://yynxxxxx.github.io/Codex-X/

提供：
- GPT-5.5 / unrestricted jeli 工作流
- Android APK 逆向 Skills
- Windows EXE / DLL 逆向 Skills
- Web / API / 协议逆向 Skills
- 一键复制安装命令

---

## 三、技术架构

### 技术栈

| 类别 | 技术 |
|------|------|
| 桌面框架 | Tauri 2 |
| 前端 | React 18 / TypeScript / Vite |
| 后端 | Rust |
| 本地数据 | SQLite / rusqlite |
| 配置编辑 | TOML / JSON |
| 发布 | GitHub Actions / GitHub Releases |

### 目录结构

```
Codex-X/
├── apps/desktop/          # Tauri 桌面应用
├── services/              # Cloudflare Worker 服务
│   └── star-history-worker/
├── examples/              # 提示词模板（5 套）
├── docs/                  # 文档与截图
├── scripts/               # 构建脚本
├── codex-instruct.py      # Python 辅助脚本
└── package.json           # pnpm monorepo 配置
```

### 配置路径

**Codex 配置目录**：
```text
~/.codex/config.toml
~/.codex/auth.json
```

**环境变量支持**：
```text
CODEX_HOME=/path/to/.codex
CODEXX_HOME=/path/to/codex-x-data
CC_SWITCH_HOME=/path/to/.cc-switch
```

**Codex-X 数据库**：
```text
~/.codexx/codexx.db
```

---

## 四、平台支持

| 平台 | 格式 |
|------|------|
| macOS Apple Silicon | `.dmg` |
| macOS Intel | `.dmg` |
| Windows | `.msi` |
| Windows Portable | `.zip` |
| Linux | `.deb` / `.rpm` / `.AppImage` |

**更新机制**：
- 安装版：应用内下载、验证、安装更新
- Windows Portable：手动下载更新

---

## 五、版本历史

### v0.3.0 (2026-07-16)

- 全面升级桌面界面，统一布局与深浅色模式
- 新增应用内更新功能
- 完善供应商管理与提示词管理
- 优化会话管理，简化 Skills/MCP 导入

### v0.2.35 (2026-07-13)

- 新增 `gpt-5.6-sol-unrestricted.md` 模板
- 优化第三方供应商切换
- 修复重复供应商显示问题

### v0.2.34 (2026-07-13)

- 新增会话永久删除功能
- 重做会话列表为表格式布局
- 修复会话总数重复统计问题

### v0.2.33 (2026-07-11)

- 重做指令提示词页面布局
- GitHub 提示词目录改为权威同步
- 新增 `海鸥3.0破甲.md` 模板

---

## 六、实际应用场景

### 1. Codex Desktop/CLI 用户

- **提示词管理**：一键切换不同风格模板，无需手动编辑配置
- **API 切换**：快速切换官方 API 与第三方中转，测试连接
- **会话清理**：查找、修复、删除不需要的历史会话

### 2. 安全研究者

- **逆向 Skills**：通过在线指南获取 Android / Windows / Web 逆向工具
- **破甲提示词**：使用 `gpt5.4-unrestricted.md` 等 CTF 导向模板
- **SQL 注入 / NSFW 测试**：内置安全测试场景示例

### 3. 多环境开发者

- **跨平台**：macOS / Windows / Linux 统一体验
- **配置备份**：重要写入自动备份，可恢复
- **会话同步**：检查并修复 Provider 不匹配问题

### 4. Skills/MCP 开发者

- **Skills 管理**：查看、导入、启用/禁用、检查更新
- **MCP 管理**：预览服务器、选择性导入、配置维护

---

## 七、亮点总结

| 维度 | 特点 |
|------|------|
| **定位** | Codex Desktop/CLI 一站式管理工具 |
| **规模** | 1.15K Stars，活跃开发中 |
| **技术** | Tauri 2 + React + Rust，现代化架构 |
| **模板** | 5 套"破甲"提示词，GitHub 自动同步 |
| **功能** | 提示词 / Provider / 会话 / Skills/MCP 全覆盖 |
| **平台** | macOS / Windows / Linux 全平台支持 |
| **更新** | 应用内自动更新（安装版） |

---

## 八、推荐使用方式

1. **日常 Codex 用户**：管理提示词和 API 切换，避免手动改配置
2. **安全研究者**：使用逆向 Skills 导航 + CTF 导向提示词
3. **多 Provider 用户**：统一管理多个第三方 API 配置
4. **会话整理需求**：批量查找、修复、删除历史会话