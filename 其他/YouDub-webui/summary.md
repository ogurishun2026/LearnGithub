# YouDub-webui 研究总结

> 仓库地址：https://github.com/liuzhao1225/YouDub-webui
> 研究日期：2026-05-18

## 一、仓库概述

YouDub-webui 是一个**开源视频本地化/配音工具**，能将 YouTube 或 Bilibili 视频自动转换为另一种语言的配音版。核心成熟场景是 YouTube 英文→中文配音，也支持 B站中文→英文配音。作者用这个工具运营着一个 80万+ 粉丝的 B 站频道，是经过真实生产验证的项目。

- Stars: 4,616 | Forks: 489 | License: 未标注
- 主语言：Python（后端流水线），TypeScript（前端 WebUI）
- 定位：个人创作者/小团队的本地视频翻译配音流水线

## 二、核心内容

### 2.1 完整工作流（8步流水线）

```
YouTube/Bilibili URL
  → yt-dlp 下载视频
  → Demucs 分离人声与背景音
  → Whisper 语音识别（词级时间戳）
  → 句子与时间范围整理
  → OpenAI API 预处理全文 + 逐句并发翻译
  → 按句切分原始人声（参考音频）
  → VoxCPM2 生成目标语言配音
  → 对齐配音时长 → 与背景音混音 → FFmpeg 压制字幕 → 输出 mp4
```

### 2.2 功能亮点

| 功能 | 说明 |
|------|------|
| **端到端自动化** | 从 URL 到最终配音视频，无需手动拆分 |
| **双来源** | YouTube + Bilibili |
| **本地优先** | 所有数据（Cookie、日志、产物）保存在本机 |
| **任务管理** | 历史记录、阶段状态、耗时、运行日志均可查看 |
| **失败恢复** | 失败任务从失败阶段继续，已成功阶段复用缓存 |
| **在线预览** | 页面内播放最终视频 + 下载 mp4 |
| **UI 配置** | Cookie、代理、API Key 等全部在 Settings 中维护 |

### 2.3 技术栈

| 层 | 技术 |
|----|------|
| 前端 | Next.js App Router, shadcn/ui, Tailwind CSS |
| 后端 | FastAPI, SQLite, 后台 Worker |
| 视频下载 | yt-dlp |
| 音源分离 | Demucs（子模块引入） |
| 语音识别 | OpenAI Whisper（默认 large-v3-turbo） |
| 翻译 | OpenAI 兼容 Chat Completions API（可换模型） |
| 语音合成 | VoxCPM2 |
| 音视频处理 | FFmpeg, pydub, librosa, audiostretchy |

## 三、技术架构

### 3.1 项目结构

```
YouDub-webui/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI 入口
│   │   ├── config.py         # 环境变量配置
│   │   ├── database.py       # SQLite 数据库
│   │   ├── pipeline.py       # 流水线编排
│   │   ├── stages.py         # 各阶段定义
│   │   ├── worker.py         # 后台任务 Worker
│   │   ├── sources.py        # 视频源适配
│   │   ├── youtube.py        # YouTube 相关
│   │   ├── sanitize.py       # 输入清理
│   │   └── adapters/         # 核心适配器层
│   │       ├── ytdlp.py      # yt-dlp 下载
│   │       ├── demucs.py     # 音源分离
│   │       ├── whisper_asr.py # 语音识别
│   │       ├── openai_translate.py # 翻译
│   │       ├── voxcpm.py     # 语音合成
│   │       ├── audio.py      # 音频处理
│   │       ├── ffmpeg.py     # 视频压制
│   │       └── asr_sentence_fixer.py # ASR 句子修正
│   ├── tests/                # 后端测试
│   └── requirements.txt
├── apps/web/                 # Next.js WebUI
│   ├── src/
│   └── package.json
├── scripts/
│   └── run_pipeline.py       # 独立流水线脚本
└── submodule/demucs/         # Demucs 源码子模块
```

### 3.2 架构设计

- **适配器模式**：`adapters/` 目录下每个文件对应流水线的一个环节，模块边界清晰，方便替换 ASR/TTS/翻译后端
- **流水线编排**：`pipeline.py` + `stages.py` 串行编排各阶段，每个阶段独立、可恢复
- **后台 Worker**：`worker.py` 在进程内运行后台任务，前端通过 API 查询进度
- **SQLite 存储**：轻量级本地存储，零配置

## 四、实际应用场景

### 4.1 视频翻译配音

- 将英文 YouTube 视频（科技、科普、游戏等）自动翻译为中文配音，发布到 B 站
- 将 B 站中文视频翻译为英文配音，覆盖海外受众
- 适合个人创作者、自媒体、小团队做跨语言内容

### 4.2 开发者参考

- **AI 视频处理流水线**：完整的 8 阶段流水线设计，每个阶段可独立替换
- **适配器模式实践**：如何设计可替换的 AI 服务层（ASR/TTS/翻译）
- **FastAPI + Next.js 全栈项目**：前后端分离的本地工具架构
- **任务管理设计**：失败恢复、进度追踪、缓存复用的实现方式

### 4.3 运行要求

- Python 3.12 + Node.js 20+
- CUDA GPU 推荐（CPU 可跑但极慢）
- 需要 OpenAI 兼容 API 的 Key
- 需要 YouTube 代理 + Cookie
- 首次运行需下载较大的 ASR/TTS 模型
