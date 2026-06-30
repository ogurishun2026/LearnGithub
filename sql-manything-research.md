---
name: sql-manything-research
description: SQL-ManyThing 深度研究 —— 让 AI Agent 拥有代码库搜索记忆的 SQLite 索引基础设施
metadata: 
  node_type: memory
  type: reference
  originSessionId: 6aafdfcd-c3e4-495d-a2d3-5636278c31ab
---

**SQL-ManyThing** 是一个**方法论仓库 + 工具脚本集合**，核心目标是将任何源代码树索引为可查询的 SQLite 数据库，让 AI Agent 在不读取每个文件的情况下回答关于陌生代码库的问题。

仓库地址：`https://github.com/IOchair/SQL-ManyThing`

## 为什么重要（Why）

开发自动化 Agent 时，一个核心痛点是**如何让 Agent 高效探索大规模代码库**。传统方式是把整文件丢给 LLM（token 爆炸、上下文污染），或者用黑盒 RAG（不可审计、依赖云服务）。SQL-ManyThing 用极简技术栈（Python 标准库 + SQLite）提供了一个**完全离线、可审计、有界提取、查询记忆**的代码搜索基础设施。这对任何需要处理大型代码库的自动化 Agent 都极具价值。

## 技术栈

| 维度 | 详情 |
|------|------|
| 语言 | Python 3.9+（Phase 1–2 仅需标准库，零 pip install） |
| 数据库 | SQLite 3.35+（FTS5 trigram 分词器） |
| 脚本数量 | 约 15 个 Python 脚本 + shell/bat 包装器 |
| 参考文档 | 20+ 篇 markdown |
| 许可证 | MIT |

## 三阶段架构

### Phase 1 — 创建索引
- 遍历目标项目所有文本文件（`os.walk` 或 `git ls-files`）
- 文件路径 + 完整内容写入 SQLite
- 创建 **FTS5 trigram 全文索引**，支持 CJK、CamelCase、snake_case
- 内置 Unreal Engine 专用 profile
- **输出**：`.srcidx/source.db`（单个 SQLite 文件）
- **性能**：UE 5.8 完整索引 —— 89,203 文件，~3GB，约 85 分钟

### Phase 2 — 结构富化
| 脚本 | 功能 |
|------|------|
| `enrich_depth_segments.py` | 按深度/缩进层级分段代码（花括号语言跟踪 `{}` 深度，缩进语言跟踪缩进级别） |
| `enrich_file_refs.py` | 解析 import/require/include/use，支持 Python/JS/TS/Java/Go/Rust/C/C++/Scala |
| `flatten_file_deps.py` | 展开传递依赖树（上游/下游） |
| `create_enriched_view.py` | 创建 `v_enriched` 统一视图，支持按 depth_level 提取代码块 |

### Phase 3 — 查询追踪
- 安装 `sqlite3` 包装器到 `~/.local/bin/`
- 拦截 `/manything/<project>/source.db` 查询，解析为实际路径
- 每次查询记录到 `pending.jsonl`，再批量导入全局 `query_log.db`
- 提供 `:trace` 虚拟数据库查询历史
- **核心表**：`query_trace`（查询记录）、`query_notes`（标注/tag）

## 核心设计思想

### 1. A* 搜索框架
将代码探索建模为 A* 搜索：状态=文件/行/符号/图节点/追踪历史，操作符=SQL 查询 或 有界 `substr()` 提取，目标=用最少必要源码获得证据充分的答案。

### 2. 四条规范化查询模板
```
DISCOVER → [TRACE_DEPS] → EXTRACT → EXTRACT_BLOCK
```
- **DISCOVER**：FTS5 MATCH 找到候选文件
- **TRACE_DEPS**：依赖追踪消歧
- **EXTRACT**：按 depth_level 探查文件结构
- **EXTRACT_BLOCK**：精确提取代码块

### 3. 有界提取（Bounded Extraction）
永不读取整个文件。用 `substr()` 只提取匹配区域：
```sql
SELECT substr(content, max(1, ? - 30), ? + 60) FROM files WHERE rowid = ?
```

### 4. 虚拟路径 + 别名
`/manything/<project>/source.db` 不是真实路径，由包装器通过 `MANYTHING_<project>` 环境变量解析。项目移动后路径仍然稳定。

## 数据库表结构

| 表 | 内容 |
|---|---|
| `files` | 文件元数据 + 完整文本内容 |
| `files_fts` | FTS5 trigram 索引 |
| `v_enriched` | 统一视图：深度分段块，含 `block_content_full` |
| `enrich_depth_segments` | 原始深度分段数据 |
| `enrich_file_deps` | 已解析的 import/include 依赖图 |
| `enrich_file_refs` | 原始 import/include 字符串及行号 |

## 如何应用（How to apply）

1. **Agent 代码搜索后端**：替代"碰运气"的文件读取，让 Agent 拥有整个代码库的结构化搜索记忆
2. **有界上下文提取**：只提取证据片段，大幅降低 LLM token 消耗
3. **查询模式复用**：同一项目查多了，Agent 自动收敛到最高效的 SQL 模式
4. **离线自托管**：无需向量数据库、云 RAG、嵌入模型。一个 SQLite 文件，scp 到任何地方
5. **完全可审计**：每条结果都可追溯到一条 SELECT，无黑盒检索
6. **多 Agent 协作**：多个 Agent 共享同一索引和追踪数据库，集体学习

## 相关记忆

- [[narutocode-research]] — 终端 Agent 编程助手，SQL-ManyThing 可作为其代码搜索后端
- [[cliproxyapi-research]] — AI 代理网关，提供多模型 API 接入
- [[ai-workflow-discussion]] — AI 全自动化工作流探索
- [[spark-research]] — 3D 渲染器，SQL-ManyThing 的索引理念可扩展到 Shader/资产元数据搜索
