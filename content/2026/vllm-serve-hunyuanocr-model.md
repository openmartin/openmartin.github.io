Title: 在本地电脑和消费级显卡上运行 HunyuanOCR 1.5
Status: published
Date: 2026-08-08 20:00
Modified: 2026-08-08 20:00
Category: Linux
Tags: llm
Slug: vllm-serve-hunyuanocr-model
Summary: 在本地电脑和消费级显卡上运行 HunyuanOCR 1.5

参考官方文档，同时也有一些自己实际碰到的问题，踩得坑，花了一下午时间。

## 环境

操作系统： Debian 12.15

显卡： RTX 4060 Ti 16G

## 安装依赖

```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
# 虚拟环境
uv venv --python 3.12 && source .venv/bin/activate
# 依赖包
uv pip install vllm==0.25.1
uv pip install "https://github.com/adithyaxx/flash-attention/releases/download/v2.8.3/flash_attn-2.8.3+cu13torch2.11cxx11abiTRUE-cp312-cp312-linux_x86_64.whl"
```

如果是按照官方文档里的 `uv pip install --no-build-isolation --no-cache-dir "flash-attn==2.8.3"` 非常容易编译失败，而且 flash-attn 官方没有跟目前环境一致而且编译好的 wheel 包下载，不过有其他人提供了目前需要的环境对应的 flash-attn 包，直接下载就行，否则编译的问题太难解决了。

## 下载模型

```bash
uv pip install hf
hf download tencent/HunyuanOCR --local-dir ./HunyuanOCR --exclude "v1.0/*"
```

## vllm

直接使用官方的脚本就可以启动

```bash
# —— vLLM AR ——
MODEL_PATH=./HunyuanOCR GPU=0 PORT=8000 bash inference/vLLM/serve.sh

# —— vLLM + DFlash（草稿路径默认为 ${MODEL_PATH}/dflash） ——
MODEL_PATH=./HunyuanOCR GPU=0 PORT=8000 bash inference/DFlash/serve_DFlash.sh

# 就绪检查
curl -sf http://127.0.0.1:8000/v1/models
```

## DFlash

官方说用了 DFlash 速度会块很多，的确是快了，第一次请求会慢，但是后续的请求速度就加快了。

简单用了一个小图片对比用了 DFlash 和 没用 DFlash 的速度，还是有明显提升的，第一次请求往往包含一些初始化操作。

|                | vllm  | vllm + DFlash |
|----------------|-------|---------------|
| 图片第一次     | 0.97s | 2.34s         |
| 同样图片第二次 | 0.71s | 0.47s         |


## 其他说明

下载模型的时候需要设置代理，huggingface.co 没办法直接连上。

安装 python 包的时候最好也设置一下，否者会很慢。

参考资料
1. [HunyuanOCR github](https://github.com/Tencent-Hunyuan/HunyuanOCR/blob/main/docs/inference/inference_zh.md)


