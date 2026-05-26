# ripgrep 研究总结

> 仓库地址：https://github.com/burntsushi/ripgrep
> 研究日期：2026-05-26

## 一、仓库概述

ripgrep（简称 rg）是一个基于行的搜索工具，递归搜索目录中的正则表达式模式。默认情况下会尊重 gitignore 规则，自动跳过隐藏文件和二进制文件。是 grep、ack、silver Searcher 等工具的最佳替代品，跨平台支持 Windows、macOS 和 Linux。

## 二、核心能力

### 2.1 功能特点

| 特性 | 说明 |
|---|---|
| 速度极快 | 比同类工具快数倍，支持多线程搜索 |
| 智能过滤 | 自动尊重 .gitignore，自动跳过隐藏文件/二进制 |
| 正则表达式 | 支持多种正则引擎，默认启用自动转发 |
| 彩色输出 | 默认启用颜色，方便阅读结果 |
| 跨平台 | 支持 Windows、macOS、Linux |

### 2.2 主要选项

| 选项 | 说明 |
|---|---|
| `-u, --no-ignore` | 禁用所有自动过滤 |
| `-g, --glob` | 通过 glob 模式包含文件 |
| `-F, --fixed-strings` | 固定字符串模式（禁用正则） |
| `-l, --files-with-matches` | 只显示文件名 |
| `-n, --line-number` | 显示行号 |
| `-A, --after-context` | 匹配后显示行数 |
| `-B, --before-context` | 匹配前显示行数 |

### 2.3 性能对比

在大型代码库（如 Linux 内核）中，ripgrep 的搜索速度显著优于传统 grep 和 ack。

## 三、技术架构

### 3.1 技术栈

- **语言**：Rust
- **许可证**：Unlicense（公有领域）
- **依赖**：使用 Rust 的正则表达式库和并行处理能力

### 3.2 架构设计

```
用户输入 → 正则解析 → 并行搜索 → 结果聚合 → 彩色输出
```

核心利用 Rust 的轻量级线程实现高效并行搜索。

## 四、项目信息

- **Stars**：64,213（非常高 🔥）
- **Forks**：3,044
- **语言**：Rust
- **许可证**：Unlicense（公有领域）
- **创建时间**：2016-03-19
- **平台**：Windows/macOS/Linux
- **Topics**：grep, search, command-line, rust

## 五、实际应用场景

1. **代码搜索**：`rg "function_name" --type rust` 快速查找 Rust 代码中的函数
2. **日志分析**：`rg "ERROR" /var/logs` 在日志文件中查找错误
3. **代码审查**：`rg "TODO" -C 3` 显示上下文辅助审查
4. **替代 grep**：`alias rg="ripgrep"` 永久替代 grep

## 六、与 grep 的对比

| 维度 | ripgrep | grep |
|---|---|---|
| 速度 | 极快，多线程 | 较慢 |
| 智能忽略 | 自动跳过二进制/隐藏 | 手动处理 |
| 输出格式 | 彩色默认 | 需加 --color |
| 正则支持 | 默认支持 | 支持但语法不同 |
| 许可证 | Unlicense | GPL |