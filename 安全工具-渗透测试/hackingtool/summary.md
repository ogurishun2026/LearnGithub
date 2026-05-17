# hackingtool 研究总结

> 仓库地址：https://github.com/Z4nzu/hackingtool
> 研究日期：2026-05-17

## 一、仓库概述

hackingtool 是一个**一站式安全测试 / 渗透测试工具集**，用 Python 3.10+ 编写，将 185+ 个主流黑客/安全工具按 20 个类别整合到统一的 TUI（终端 UI）菜单中。面向安全研究人员和渗透测试人员，仅限授权安全测试使用。

- Stars: 75,061 | Forks: 8,470 | License: MIT
- 主语言：Python（100%）
- 支持平台：Linux / Kali / Parrot / macOS

## 二、核心内容

### 2.1 功能定位

不是自己实现攻击工具，而是做一个**统一的安装/启动/管理界面**，把分散在 GitHub 上的 185+ 个安全工具归类整合：

- 一键安装：每个工具有独立的安装命令（git clone / pip install / go install）
- 一键运行：安装后直接从菜单启动
- 批量安装：任意分类下输入 `97` 可批量安装该分类所有工具
- 搜索推荐：`/` 关键词搜索、`r` 智能推荐、`t` 标签过滤

### 2.2 20 个工具分类

| # | 分类 | 工具数 | 典型工具 |
|---|------|--------|----------|
| 1 | 匿名隐藏 | 2 | Anonsurf, Multitor |
| 2 | 信息收集 | 26 | Nmap, Amass, Masscan, RustScan, SpiderFoot, TruffleHog |
| 3 | 字典生成 | 7 | Hashcat, John the Ripper, Cupp |
| 4 | 无线攻击 | 13 | WiFi-Pumpkin, Fluxion, Bettercap, Airgeddon |
| 5 | SQL 注入 | 7 | Sqlmap, NoSqlMap, Leviathan |
| 6 | 钓鱼攻击 | 17 | Setoolkit, Evilginx3, SocialFish, HiddenEye |
| 7 | Web 攻击 | 20 | Nuclei, ffuf, Nikto, OWASP ZAP, mitmproxy, Caido |
| 8 | 后渗透 | 10 | Sliver, Havoc, LinPEAS/WinPEAS, Ligolo-ng, Mythic |
| 9 | 数字取证 | 8 | Wireshark, Volatility 3, Binwalk |
| 10 | 载荷生成 | 8 | TheFatRat, MSFvenom, Venom |
| 11 | 漏洞利用框架 | 4 | RouterSploit, Commix |
| 12 | 逆向工程 | 5 | Ghidra, Radare2, JadX |
| 13 | DDoS 攻击 | 5 | SlowLoris, UFOnet, GoldenEye |
| 14 | 远程管理 (RAT) | 1 | Pyshell |
| 15 | XSS 攻击 | 9 | DalFox, XSStrike, XSpear |
| 16 | 隐写术 | 4 | StegoCracker |
| 17 | Active Directory | 6 | BloodHound, Impacket, Responder, Certipy |
| 18 | 云安全 | 4 | Prowler, ScoutSuite, Pacu, Trivy |
| 19 | 移动安全 | 3 | MobSF, Frida, Objection |
| 20 | 其他工具 | 24 | Sherlock（社交账号查找）, Hash Buster 等 |

### 2.3 v2.0.0 新特性

- Python 3.10+ 全面升级，移除所有 Python 2 代码
- OS 感知菜单：macOS 自动隐藏仅限 Linux 的工具
- 安装状态检测：每个工具旁显示 ✔/✘ 标记
- 智能更新：自动识别 git pull / pip upgrade / go install
- Docker 支持：本地构建，无外部未验证镜像
- 一行命令安装：`curl -sSL .../install.sh | sudo bash`

## 三、技术架构

### 3.1 项目结构

```
hackingtool/
├── hackingtool.py          # 主入口，注册所有分类菜单
├── core.py                 # 核心框架：HackingTool 基类 + TUI 组件
├── constants.py            # 版本、路径、主题配置
├── config.py               # 用户配置管理（JSON）
├── os_detect.py            # 操作系统检测
├── install.py / install.sh # 安装脚本
├── tools/
│   ├── tool_manager.py     # 工具管理器（搜索、推荐、标签过滤）
│   ├── anonsurf.py         # 每个文件 = 一个分类
│   ├── information_gathering.py
│   ├── web_attack.py
│   ├── phishing_attack.py
│   ├── ...（20 个分类文件）
│   └── others/             # 子分类
├── Dockerfile              # Docker 构建
├── docker-compose.yml      # Docker Compose（含 dev 模式）
└── requirements.txt        # Python 依赖
```

### 3.2 核心设计模式

**基类继承**：`core.py` 定义 `HackingTool` 基类和 `HackingToolsCollection` 容器类
- 每个工具定义 `TITLE`、`DESCRIPTION`、`INSTALL_COMMAND`、`RUN_COMMAND`、`SUPPORTED_OS`
- 每个分类文件继承 `HackingToolsCollection`，注册该分类下的所有工具

**UI 框架**：使用 [Rich](https://github.com/Textualize/rich) 库构建 TUI
- Panel、Table、Prompt 构建层级菜单
- 自定义主题（紫色调 magenta 主题）

**工具管理**：`tool_manager.py` 提供搜索（`/query`）、标签过滤（`t`）、智能推荐（`r`）

### 3.3 依赖

| 依赖 | 用途 |
|------|------|
| Python 3.10+ | 核心运行时 |
| Rich | TUI 终端界面 |
| Go 1.21+ | 部分工具（nuclei, ffuf, amass 等） |
| Ruby | 部分工具（haiti, evil-winrm） |
| Docker | 可选，用于 MobSF、Mythic 等 |

## 四、实际应用场景

### 4.1 安全测试学习

- 新手入门渗透测试的**工具索引**——不了解有哪些工具时，浏览 20 个分类即可建立全局认知
- CTF 比赛工具箱——快速安装比赛所需工具

### 4.2 渗透测试工作流

- 授权渗透测试的统一工具管理界面
- 批量安装/更新工具，避免逐个 git clone
- 按攻击阶段（信息收集 → 漏洞利用 → 后渗透）组织工具

### 4.3 开发者参考价值

- **Python CLI/TUI 项目架构**：Rich 库的实战用法，基类继承模式管理大量子模块
- **工具编排框架设计**：如何设计一个可扩展的插件/工具管理系统
- **跨平台安装脚本**：处理不同 OS 的安装路径和依赖

### 4.4 注意事项

- **仅限授权安全测试**：仓库明确声明仅供授权使用
- 运行环境推荐 Kali Linux / Parrot OS
- 部分工具需要 root 权限
