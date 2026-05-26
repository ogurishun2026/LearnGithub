# codedb-mcp 研究总结

> 仓库地址：https://github.com/killop/codedb-mcp
> 研究日期：2026-05-26

## 一、仓库概述

`codedb-mcp`（原名 `codebase-mcp`）是一个 Rust 实现的本地 MCP Server，专注于为大型代码库提供超高速的代码搜索、符号分析、依赖图分析和本地 DeepWiki 生成能力。通过 MCP（Model Context Protocol）协议暴露 `codedb_*` 工具接口，其核心优势在于**预索引 + 混合搜索**架构——索引构建稍慢，但查询极快（毫秒级），且支持语义搜索、LSP 级别的引用查找和代码图分析。

## 二、核心能力

### 2.1 MCP 工具集

| 工具 | 用途 |
|---|---|
| `codedb_search` | 混合搜索（BM25 + 向量）或 regex 行搜索；支持 batch |
| `codedb_callers` | LSP 级别引用查找，支持 definition path/line 锚定，支持 batch |
| `codedb_deps` | 文件依赖和反向依赖；支持 transitive |
| `codedb_outline` | 返回预计算符号大纲，不在请求时重新 parse |
| `codedb_symbol` | 按符号名找定义 |
| `codedb_word` | 精确 identifier 倒排索引查询 |
| `codedb_find` | 模糊文件名/路径查找 |
| `codedb_query` | find/search/filter/limit/outline 小型 pipeline |
| `codedb_bundle` | 一次 MCP 请求里执行最多 100 个工具调用 |
| `codedb_graph` | 图摘要或导出 |
| `codedb_communities` | 懒计算 Louvain community/subcommunity |
| `codedb_analyze` | 图统计、top nodes、关系计数、建议问题 |
| `codedb_hot` | 最近修改的索引文件 |
| `codedb_status` | 索引健康状态和统计 |

### 2.2 性能数据

在 Unity C# 项目（18,975 indexed files, 129,165 chunks）上的实测表现：

- **精确 regex 搜索**：`PoolManager` 搜索耗时 **0.2234s**（rg 对比 1.7201s），命中数完全一致
- **混合语义搜索**：`Joystick` 相关 chunk 搜索 **0.0666s**，rg 无等价能力
- **引用查找**：`PoolManager.cs:26` 引用 **7 个结果仅 0.0045s**
- **依赖分析**：`GameObjectPoolMgr.cs` 依赖 **7 个文件 0.0002s**
- **批量 bundle**：`codedb_bundle` 一次请求 100 个操作 **0.0913s**（p95）

### 2.3 vs rg 对比结论

`rg` 适合临时扫任意文件；`codedb-mcp` 适合在配置好的源码语料上做反复、低延迟、代码感知的查询，特别是语义搜索和引用分析。

## 三、技术架构

### 3.1 多层架构

```
显式配置层(.codedb-mcp/codedb-mcp.toml)
    ↓
本地存储层(.codedb-mcp/ 索引文件)
    ↓
扫描层(基于配置遍历代码库，gitignore/include_paths)
    ↓
语言解析层(tree-sitter grammars，统一 FileEntry/Symbol)
    ↓
代码语义增强层(C#/Java namespace/别名/静态using/注解/属性)
    ↓
搜索索引层(chunks/BM25/Model2Vec embeddings/HNSW向量)
    ↓
依赖与图层(文件/namespace/symbol/dependency/reference 节点边)
    ↓
MCP 工具层(rmcp SDK stdio server)
```

### 3.2 核心依赖

- **语言解析**：tree-sitter（支持 C#、Java、Python、JS/TS、C、C++）
- **向量模型**：`model2vec-rs` + `minishlab/potion-code-16M`（本地文件级向量）
- **向量索引**：Vicinity HNSW
- **文本搜索**：BM25 + 精确 identifier 倒排索引
- **代码图**：graphify 风格 + Louvain community
- **MCP 协议**：Rust `rmcp` SDK
- **文件监听**：`notify` crate，debounce 后台重建索引

### 3.3 源码结构

| 文件 | 职责 |
|---|---|
| `main.rs` | CLI 入口，MCP 模式和 CLI 模式 |
| `mcp.rs` | MCP 服务器协议实现 |
| `tools.rs` | MCP 工具定义（最大，57KB） |
| `indexer.rs` | 索引构建核心（53KB） |
| `graph.rs` | 代码依赖图和 Louvain（87KB，最大） |
| `search.rs` | BM25 + 向量混合搜索 |
| `config.rs` | `.codedb-mcp.toml` 配置解析 |
| `tree_sitter_lang.rs` | 多语言 tree-sitter 解析封装 |
| `embedding.rs` | Model2Vec embedding 生成 |
| `vector_store.rs` | Vicinity HNSW 向量存储 |
| `bm25.rs` | BM25 索引和搜索 |
| `cache.rs` | 索引缓存管理 |
| `watcher.rs` | 文件系统监听 |
| `source.rs` | 源码文本管理 |
| `tokens.rs` | 分词 |
| `types.rs` | 基础类型定义 |
| `language.rs` | 语言检测 |

### 3.4 数据流

1. **索引构建**：扫描文件 → tree-sitter 声明解析 → 语义增强 → chunks/embeddings → BM25/HNSW → graph → cache
2. **查询流程**：MCP 请求 → warm in-process index → 按类型路由（search/callers/deps/outline）→ 合并结果
3. **文件监听**：检测改动 → debounce → 后台重建受影响部分 → 更新 runtime index

## 四、部署方式

### 4.1 Skill-First 部署（推荐）

```powershell
# 1. 把 skills/codedb-mcp 复制到 agent skills 目录
# 2. 在目标项目里，让 agent 使用 codedb-mcp skill
# 3. skill 运行 setup 脚本
powershell -ExecutionPolicy Bypass -File <skill-root>\scripts\setup.ps1 -ProjectRoot <repo-root>
# 4. skill 打印 MCP 注册命令，agent 显式注册
# 5. 重启 agent session
```

### 4.2 项目本地化

所有数据写入目标项目的 `.codedb-mcp/` 目录（索引、manifest、Louvain 缓存），不依赖全局数据库。删除该目录即可清理。

### 4.3 构建

```powershell
cargo build --release
target/release/codebase-mcp.exe --config <repo-root>/.codedb-mcp/codedb-mcp.toml mcp <repo-root>
```

## 五、配套 Skills

### 5.1 `skills/codedb-mcp`

打包了 `codebase-mcp.exe`、setup 脚本、配置模板、MCP 安装说明。复制目录即可使用，不修改全局 MCP 配置。

### 5.2 `skills/deepwiki`

利用 `codedb_*` 工具和 agent 推理能力生成 DeepWiki-style 文档，强调业务模块边界，按 community 分组而非按文件夹。

## 六、实际应用场景

1. **大型 Unity/C# 项目**：19K 文件量级，毫秒级搜索和引用查找，远超 `rg`
2. **跨语言代码库**：统一接口搜索 C#/Java/Python/C++，混合语义搜索
3. **代码图分析**：Louvain community 发现、文件依赖可视化、top nodes 分析
4. **DeepWiki 生成**：基于图结构生成业务模块文档
5. **Agent 辅助编码**：MCP 协议直连 Claude Code，为 AI agent 提供代码索引能力

## 七、项目信息

- **Stars**：34
- **语言**：Rust
- **创建时间**：2026-05-22（非常新）
- **主要依赖**：tree-sitter 系列、model2vec-rs、rmcp、Vicinity HNSW
- **配置**：`.codedb-mcp/codedb-mcp.toml`，支持扩展名/gitignore/include_paths/skip_dirs/embedding 模型/存储路径