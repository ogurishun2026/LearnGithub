# 部署与重跑

本机成功路线是 Windows 11 / Python 3.12.4 / RTX 4060 Laptop 8 GB，ARDY 环境复用了既有 CUDA 库。下面提供等价的新环境安装步骤，**未在第二台空机器全量重装验证**。生成、重新编码、NPZ 校验和 Viser 画面已在本机验证；二进制权重、环境与 embedding 不在 Git 中。

## 1. 从 LearnGithub 准备目录

在本目录（有 `summary.md` 的目录）打开 PowerShell。Python 3.12、Git、CMake 和 MSVC C++17 Build Tools 需要事先可用。新建的 runtime 目录被本目录的 `.gitignore` 排除。

```powershell
git clone https://github.com/nv-tlabs/ardy.git runtime/ardy
git -C runtime/ardy checkout 693f74d13b3d04a0a22ce127ee79c929dd89756b
py -3.12 -m venv runtime/venv
runtime/venv/Scripts/python.exe -m pip install --upgrade pip
runtime/venv/Scripts/python.exe -m pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu121
runtime/venv/Scripts/python.exe -m pip install -e 'runtime/ardy[demo]' -c tested-constraints.txt
runtime/venv/Scripts/python.exe -m pip install bitsandbytes==0.50.1
```

`tested-constraints.txt` 是本机关键版本记录，不是完整锁文件。ARDY demo 固定使用 NVIDIA 的 kimodo-viser fork，不能随意替换成 PyPI 的同名包。已有 Kimodo 应继续放在其原环境，避免两个项目不同的 Transformers 固定版本相互覆盖。

## 2. 下载模型并编码

```powershell
runtime/venv/Scripts/python.exe scripts/download_checkpoint.py runtime/checkpoints/ARDY-Core-RP-20FPS-Horizon8
runtime/venv/Scripts/hf.exe download Aero-Ex/KIMODO-Meta3_llm2vec_NF4 --revision 207f0c64a7325f6045d15c68c5ea9e961c18fafd --local-dir runtime/nf4
runtime/venv/Scripts/python.exe scripts/encode_prompts.py --model runtime/nf4 --output runtime/embeddings --device cpu 'A person walks forward.'
```

NF4 来源是第三方量化模型；自行核对模型页/基础模型许可和访问要求。该 revision 来自本地已下载模型的 Hugging Face 缓存元数据。脚本加载本地文件，采用 ARDY 内置 LLM2Vec，无 Kimodo 包依赖。CPU 编码需要较多内存和约一分钟以上；本机测得 83 秒，换硬件可能更慢。

`download_checkpoint.py` 会核对每个文件的大小和哈希。若服务返回 502，重跑相同命令会跳过已校验的完整文件，但未完成的大文件会重新下载；没有实现断点续传。必须等下载器正常结束并生成 `download-report.json`，不能只看 denoiser 存在。

## 3. 真实生成和校验

```powershell
runtime/venv/Scripts/python.exe scripts/generate_cached.py --ardy-root runtime/ardy --embeddings runtime/embeddings --report runtime/generation-report.json 'A person walks forward.' --model core8 --duration 2 --seed 0 --output runtime/outputs/walk --checkpoints_dir runtime/checkpoints --no-postprocess
runtime/venv/Scripts/python.exe scripts/validate_motion.py runtime/outputs/walk.npz --report runtime/validation-report.json
runtime/venv/Scripts/python.exe scripts/test_cached_encoder.py
```

缓存只支持已经编码过的原文；新提示词需要先编码，未知提示词会报错而不是偷偷回退。当前脚本每次重写目标目录的 manifest；建议每组提示词使用新的缓存目录，或在一次调用中把需要的提示词一起传入。

## 4. 浏览器预览

```powershell
runtime/venv/Scripts/python.exe runtime/ardy/scripts/visualize.py runtime/outputs/walk.npz --port 2334
```

打开 <http://localhost:2334>，应显示具体文件名、40 帧、20 FPS 和实际人体。Playing 可播放，暂停后用 Frame 切换；第 0 帧和第 30 帧的姿态/位置应不同。也可把输入换成仓库附带的 `demo-artifacts/walk.npz`，仅查看保存结果，无需重新下载文字编码器和 ARDY 权重。

如出现 `No client build found` 且 Node 自动安装失败，可用已安装的 Node（本机 24.13.0）构建公开前端源码：

```powershell
$ViserClient = (& runtime/venv/Scripts/python.exe -c "from pathlib import Path; import viser; print(Path(viser.__file__).parent / 'client')").Trim()
Push-Location $ViserClient
npm ci --legacy-peer-deps
npx vite build --base ./ --outDir build
Pop-Location
```

这是上游自动构建路径使用的 Vite bundling。本机 `npm run build` 的 TypeScript 检查未通过（`keys.left/right/up/down` possibly undefined），不能用 bundling 成功冒充类型检查通过。构建后重新运行预览命令并检查实际人体；出现 WorldAxes 或 Connected 仍不算预览完成。

## 测试边界

本次关闭动作后处理，未验收脚滑、长序列稳定性、6 GB 显卡速度、完整交互控制、BVH 导出、Blender 角色重定向或 TensorRT。所附小样本和画面可用于验证部署链路，不能代表生产动画质量。代码、模型与量化模型许可分别见上游项目页面。
