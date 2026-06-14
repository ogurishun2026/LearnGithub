# heretic 研究总结

> 仓库地址：https://github.com/p-e-w/heretic
> 研究日期：2026-06-14

## 一、仓库概述

**AGPL-3.0 开源协议 · Python · v1.4.0**

Heretic 是一个**全自动语言模型审查（censorship）移除工具**。它将"审查移除"（aka "abliteration"）与基于 Optuna 的 TPE 参数优化器结合，自动找到高质量的 abliteration 参数，最小化拒绝率的同时保持 KL 散度最小。

## 二、核心定位

### 2.1 解决的问题

语言模型通常经过"安全对齐"（safety alignment），导致对某些合法问题拒绝回答。Heretic 可以在**无需昂贵的后训练**的情况下移除这种审查。

### 2.2 核心优势

| 对比项 | 原始模型 | 人工 abliteration | Heretic 自动生成 |
|--------|----------|-------------------|------------------|
| gemma-3-12b-it 拒绝率 | 97/100 | 3/100 | **3/100** |
| KL 散度 | 0 | 0.45~1.04 | **0.16** |

Heretic 生成的模型达到了与其他人工创建的 abliteration 相同的拒绝抑制水平，但 KL 散度低得多，说明对原模型能力的损害更小。

## 三、技术原理

### 3.1 Directional Ablation（方向性消融）

Heretic 实现了一种参数化变体的方向性消融。对于每个支持的 transformer 组件（注意力输出投影和 MLP 下投影）：

1. 识别每个 transformer 层中的相关矩阵
2. 相对于相关的"拒绝方向"对它们进行正交化
3. 抑制该方向在矩阵乘法结果中的表达

### 3.2 拒绝方向计算

拒绝方向 = "有害"提示词与"无害"提示词首 token 残差的均值差

### 3.3 可优化参数

| 参数 | 说明 |
|------|------|
| `direction_index` | 拒绝方向索引，支持 `per layer` 插值 |
| `max_weight` | 消融权重最大值 |
| `max_weight_position` | 最大权重位置 |
| `min_weight` | 消融权重最小值 |
| `min_weight_distance` | 最小权重距离 |

### 3.4 Heretic 的创新点

1. **灵活的消融权重核形状**：结合自动参数优化，可改善合规性/质量权衡
2. **浮点拒绝方向索引**：支持插值，解锁大量额外方向
3. **组件级参数选择**：MLP 和 Attention 使用不同权重

## 四、支持架构

- ✅ **大多数 dense 模型**
- ✅ **多模态模型**
- ✅ **多种 MoE 架构**
- ✅ **混合模型（如 Qwen3.5）**
- ⚠️ **纯状态空间模型** 暂不支持
- ⚠️ **部分研究架构** 暂不支持

## 五、使用方式

### 5.1 快速开始

```bash
pip install -U heretic-llm
heretic Qwen/Qwen3-4B-Instruct-2507
```

### 5.2 使用 uv（推荐）

```bash
git clone https://github.com/p-e-w/heretic.git
cd heretic
uv run heretic Qwen/Qwen3-4B-Instruct-2507
```

### 5.3 带研究功能安装

```bash
pip install -U heretic-llm[research]
```

### 5.4 硬件需求

- Python 3.10+
- PyTorch 2.2+
- 量化模式支持 bitsandbytes（可大幅降低 VRAM 需求）

### 5.5 默认配置

在 RTX 3090 上，使用默认配置 decensoring Qwen3-4B-Instruct-2507 约需 **20-30 分钟**。

## 六、研究功能（research extra）

### 6.1 `--plot-residuals`

生成残差向量可视化：
1. 计算每个 transformer 层首 token 的残差向量
2. PaCMAP 投影到 2D
3. 左右对齐有害/无害残差投影
4. 生成 PNG 散点图 + GIF 动画

### 6.2 `--print-residual-geometry`

打印残差几何定量分析表，包含：
- 各层余弦相似度
- L2 范数
- Mean silhouette 系数

## 七、评估数据

社区已使用 Heretic 创建并发布了 **4000+ 个模型**。

用户反馈（社区评价）：
> "GPT-OSS 20B Heretic 是我见过的最好的 uncensored 模型..."
> "Heretic GPT 20b 似乎是我尝试过的最好的 uncensored 模型..."
> "Qwen3-4B-Instruct-2507-heretic 是在 16GB VRAM 上运行的最佳未量化 abliterated 模型..."

## 八、与竞争产品对比

| 项目 | Heretic | AutoAbliterator | abliterator.py | ErisForge |
|------|---------|-----------------|----------------|-----------|
| **自动化程度** | 全自动 | 半自动 | 手动 | 手动 |
| **参数优化** | Optuna TPE | 无 | 无 | 无 |
| **灵活消融权重** | ✅ | ❌ | ❌ | ❌ |
| **浮点方向插值** | ✅ | ❌ | ❌ | ❌ |
| **多组件分别优化** | ✅ | ❌ | ❌ | ❌ |

## 九、技术栈

| 层级 | 技术 |
|------|------|
| **核心框架** | Transformers + PyTorch |
| **参数优化** | Optuna |
| **量化** | bitsandbytes |
| **加速** | accelerate |
| **UI** | Rich + questionary |
| **评估** | lm-eval |
| **研究可视化** | Matplotlib + PaCMAP + scikit-learn |

## 十、总结

Heretic 是一个**全自动的语言模型审查移除工具**，无需人工干预即可生成高质量的 decensored 模型：

- ✅ **完全自动化**：无需理解 transformer 内部结构
- ✅ **更低 KL 散度**：比人工 abliteration 更好地保留原模型能力
- ✅ **支持多种架构**：Dense、MoE、多模态、混合模型
- ✅ **量化支持**：bitsandbytes 降低 VRAM 需求
- ✅ **研究功能**：残差几何分析和可视化
- ⚠️ **AGPL 协议**：修改需开源
- ⚠️ **硬件要求**：需要足够的 GPU 资源
- ⚠️ **仅支持 Python 3.10+**

适合场景：
- 需要移除模型审查的研究人员
- 希望在本地运行"开放"语言模型的用户
- AI 可解释性研究（残差分析）