Title: 如何在 CentOS 7 上部署 Qwen3-Coder-30B-A3B
Status: published
Date: 2025-09-20 20:00
Modified: 2025-09-20 20:00
Category: Linux
Tags: linux, llm
Slug: deploy-qwen3-coder-on-centOS-7-with-dual-A40
Authors: Martin
Summary: 服务器上有两张 A40 显卡，安装的是祖传 CentOS 7 系统，如何部署 Qwen3-Coder-30B-A3B？

服务器上有两张 A40 显卡，安装的是祖传 CentOS 7 系统，如何部署 Qwen3-Coder-30B-A3B？

两张 A40 显卡，一张显卡 48G 内存，总共 96 G 内存，模型：Qwen3-Coder-30B-A3B，FP16 下模型权重约 60GB，应该足够运行。

A40 显卡有点老，原生不支持 FP8 数据格式，所以下载模型文件的时候不能用 Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8 的文件，应该选择 [Qwen/Qwen3-Coder-30B-A3B-Instruct](https://www.modelscope.cn/models/Qwen/Qwen3-Coder-30B-A3B-Instruct) 。

一张显卡的显存不够加载整个模型，需要使用两张显卡，vllm 支持并行，自己用的话，不对外提供服务的话也不用比较复杂的设置来优化。

使用 vllm 来部署大模型，主要的依赖包如下：

```
vllm==0.8.5.post1
torch==2.6.0
transformers==4.51.3
```

因为 CentOS 7 的 glibc 被锁死在 2.17 了，所以不支持 PyTorch 2.7 以上，所以 vllm 的版本也被限定在 0.8.5.post1

## 创建虚拟环境和安装依赖包

因为 CentOS 7 自带的 python 版本比较低，所以推荐使用 Anaconda，比自己从源码安装 python 要方便。

先升级 gcc 版本，有些 pip 包可能需要编译安装

```bash
sudo yum install centos-release-scl centos-release-scl-rh
sudo yum install devtoolset-11-gcc-c++ devtoolset-11-gcc

scl enable devtoolset-11 bash
```

创建虚拟环境，我这里用的是 python 3.12

```bash
conda create -n qwen3_coder_venv python=3.12
```

## 安装依赖包

有一个包 pip 安装不成功，可以用 conda 来安装

```
conda install pyzmq
```

```
pip install vllm==0.8.5.post1
```

会自动识别环境，然后安装对应包，我这里的 cuda 的版本安装的是 12.4，也是 CentOS 7 可以安装的最高版本。

## 启动服务

有两个坑：

- 如果要支持 tool call 的话需要修改一下 vllm 的源码，不多，很好改
- Qwen3-Coder 默认的上下文长度是 256K，在两张 A40 的情况下，显存不够，会启动失败，需要把上下文长度改小一点，我这里是改成 200K，可以启动

修改 vllm 0.8.5.post1 源代码，让支持 qwen3_coder 格式的 tool call

```text
从 github 上 vllm 的仓库里复制 vllm/entrypoints/openai/tool_parsers/qwen3coder_tool_parser.py

把 qwen3coder_tool_parser.py 放到对应的本地目录下，比如 site-packages/vllm/entrypoints/openai/tool_parsers/qwen3coder_tool_parser.py

修改 vllm/entrypoints/openai/tool_parsers/__init__.py 
增加 from .qwen3coder_tool_parser import Qwen3CoderToolParser 和 "Qwen3CoderToolParser",
```

启动命令如下：

```
vllm serve ./Qwen3-Coder-30B-A3B-Instruct \
    --served-model-name Qwen3-Coder-30B-A3B \
    --host 0.0.0.0 --port 8000 \
    --gpu-memory-utilization 0.95 \
    --max-model-len 204800 \
    --enable-auto-tool-choice \
    --tool-call-parser qwen3_coder
```

curl http://localhost:8000/v1/models 查看一下服务是否正常

然后就可以在你的电脑上配置 openai 兼容的接口 http://IP:Port/v1 方便各种软件调用了




