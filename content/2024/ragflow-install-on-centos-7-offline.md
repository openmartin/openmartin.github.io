Title: 在 redhat/centos 7.9 上离线安装 raglow
Status: published
Date: 2024-08-21 18:00
Modified: 2024-08-21 18:00
Category: Linux
Tags: llm, ai
Slug: ragflow-install-on-centos-7-offline
Authors: Martin
Summary: 源码安装非常复杂，尽量用 docker 安装


众所周知还有很多企业用户被锁死在 redhat 7.9 上，一直没法升级，glibc 2.17，gcc 4，python 2，导致安装新一点软件的都是噩梦，所以尽量用 docker，减少因为系统环境浪费的时间。

需要有一台同样版本的 redhat/centos 7.9 而且可以联网的服务器，也可以去云上开一台，联网把依赖的包都下载下来，然后复制到离线的那台机器上去，基本的思路就是这样。

这里以 ragflow v0.9.0 的版本为例子


## 如何用 docker 安装

思路就是在联网的那台机器上拉取镜像，然后再导入离线的服务器上。可以自己搭建 docker 镜像代理，加速大陆地区的访问。

参考 docker/docker-compose-base.yml 和 docker/.env 文件，手动 pull 镜像

```bash
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.11.3
docker pull mysql:5.7.18
docker pull quay.io/minio/minio:RELEASE.2023-12-20T01-00-02Z
docker pull redis:7.2.4
docker pull ragflow:0.9.0

docker save -o es.tar docker.elastic.co/elasticsearch/elasticsearch:8.11.3
docker save -o mysql.tar mysql:5.7.18
docker save -o minio.tar quay.io/minio/minio:RELEASE.2023-12-20T01-00-02Z
docker save -o redis.tar redis:7.2.4
docker save -o ragflow.tar infiniflow/ragflow:v0.9.0
```

把上面那些tar文件传输到离线的服务器上，然后在离线的服务器上导入

```
docker load -i es.tar
docker load -i mysql.tar
docker load -i minio.tar
docker load -i redis.tar
docker load -i ragflow.tar
```

然后就可已启动了， `docker compose -f docker/docker-compose-gpu.yml up -d`

```bash
# 查看日志
docker logs -f ragflow-server
# 进入容器的 shell
docker exec -it ragflow-server sh
```


## 如何使用源码安装

### 升级 gcc

centos/redhat 7.9 默认带的 gcc 4.8.5 版本太旧，第一步就需要升级，不然很多需要源码编译安装的就过不去

先先找一个可以连外网的 centos 下载 rpm 包

```bash
sudo yum -y install centos-release-scl
sudo yum -y install devtoolset-11 --downloadonly --downloaddir /home/centos/rpms/devtoolset-11
```

把 rpm 包传输到离线的服务器上，然后安装，切换到 gcc 11

```bash
sudo rpm -ivh *.rpm --force --nodeps
scl enable devtoolset-11 bash
```

### 升级 python 3.11，openssl，sqlite3

centos/redhat 7.9 默认带的 openssl, sqlite3 版本太低，会影响 python 3.11 的编译安装，需要升级

openssl 的安装过程如下，为了简洁，不在详细解释了

```
wget https://github.com/openssl/openssl/releases/download/OpenSSL_1_1_1w/openssl-1.1.1w.tar.gz
tar -zxvf openssl-1.1.1w.tar.gz
cd openssl-1.1.1w
./config --prefix=/usr/local/openssl --openssldir=/usr/local/openssl
make
sudo make install

# 替换旧版本
sudo mv /usr/bin/openssl /usr/bin/openssl.bak
sudo mv /usr/include/openssl /usr/include/openssl.bak

sudo ln -s /usr/local/openssl/bin/openssl /usr/bin/openssl
sudo ln -s /usr/local/openssl/include/openssl /usr/include/openssl
sudo echo "/usr/local/openssl/lib" >> /etc/ld.so.conf.d/openssl.conf
sudo ldconfig

# 查看 openssl 版本
openssl version
```


sqlite3 的如下

```
wget  https://www.sqlite.org/2024/sqlite-autoconf-3460100.tar.gz
tar -zxvf sqlite-autoconf-3460100.tar.gz
cd sqlite-3460100
./configure --prefix=/usr/local/sqlite3
make
sudo make install


sudo mv /usr/bin/sqlite3  /usr/bin/sqlite3_old
sudo ln -s /usr/local/sqlite3/bin/sqlite3   /usr/bin/sqlite3
sudo echo "/usr/local/sqlite3/lib" >> /etc/ld.so.conf.d/sqlite3.conf
sudo ldconfig

# 查看 sqlite3 的版本
sqlite3
```

安装 python 3.11

```shell
sudo yum install wget make cmake gcc bzip2-devel libffi-devel zlib-devel
# 编译 Python
export makeLDFLAGS="${LDFLAGS} -Wl,-rpath=/usr/local/openssl/lib:/usr/local/sqlite3/lib"
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/openssl/lib:/usr/local/sqlite3/lib
./configure --prefix=/home/learnai/localpython --with-openssl=/usr/local/openssl --enable-optimizations


make
make install
```


### pip 安装依赖

#### pytorch

因为 centos/redhat 7.9 仅支持 cuda 11，所以安装 pytorch 需要指定 cuda 11

手工下载安装

```
torch-2.3.0+cu118-cp311-cp311-linux_x86_64.whl
triton-2.3.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
```

#### onnxruntime

pypi 上下载的 onnxruntime 安装包需要比较新的 glibc 2.27, 所以只能自己从源码编译，需要在可以联网的那台机器上先编译，把编译好的包拷贝到离线的服务器上

```bash
# 1.17.3
pip install numpy==1.26.4
pip install packaging
pip install wheel
./build.sh --config RelWithDebInfo --build_shared_lib --parallel --compile_no_warning_as_error --skip_submodule_sync --cmake_extra_defines onnxruntime_BUILD_UNIT_TESTS=OFF --build_wheel --skip_tests
# 编译之后的结果
onnxruntime-1.17.3/build/Linux/Release/dist/onnxruntime-1.17.3-cp311-cp311-linux_x86_64.whl


# 1.17.1 cuda
wget https://developer.download.nvidia.cn/compute/cudnn/redist/cudnn/linux-x86_64/cudnn-linux-x86_64-8.9.7.29_cuda11-archive.tar.xz
tar Jxvf cudnn-linux-x86_64-8.9.7.29_cuda11-archive.tar.xz
sudo mkdir /usr/local/cudnn-8.9.28_cuda11
sudo cp -r cudnn-linux-x86_64-8.9.7.29_cuda11-archive/ /usr/local/cudnn-8.9.28_cuda11/
sudo ln -s /usr/local/cudnn-8.9.28_cuda11 /usr/local/cudnn

./build.sh --config RelWithDebInfo --build_shared_lib --parallel --compile_no_warning_as_error --skip_submodule_sync --use_cuda --cudnn_home /usr/local/cudnn --cuda_home /usr/local/cuda --cmake_extra_defines onnxruntime_BUILD_UNIT_TESTS=OFF --build_wheel --skip_tests
# 编译之后的结果
onnxruntime-1.17.1/build/Linux/Release/dist/onnxruntime_gpu-1.17.1-cp311-cp311-linux_x86_64.whl
```

#### requirements.txt

先把 `requirements.txt` 中 jina 那一行注释掉，因为依赖冲突，而且一般用不到

先建立一个虚拟环境，然后安装依赖包

```
/home/learnai/localpython/bin/python3 -m venv ragflow_venv
source ragflow_venv/bin/activate
```

```
# 先安装下面的包
onnxruntime-1.17.3
onnxruntime_gpu-1.17.1
fastembed-0.2.6-py3-none-any.whl
torch-2.3.0+cu118-cp311-cp311-linux_x86_64.whl
triton-2.3.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

# 安装其他包
pip intall -r requirements.txt

pip install python-docx
# 因为版本冲突，再安装一遍这个版本
pip install pydantic=2.8.2
```


### 其他基础软件

为了省事，ES、MySQL、minio、redis 可以直接使用 docker 镜像启动

```
docker compose -f docker/docker-compose-base.yml up -d
```

### 前端代码编译

下载 node-v18.19.1-linux-x64-glibc-217.tar.gz https://unofficial-builds.nodejs.org/download/release/v18.19.1/

```bash
tar -zxvf node-v18.19.1-linux-x64-glibc-217.tar.gz
export PATH=$PATH:/home/learnai/node-v18.19.1-linux-x64-glibc-217/bin
cd web
npm install --force --loglevel verbose
vim .umirc.ts
# Update proxy.target to http://127.0.0.1:9380
./node_modules/umi/bin/umi.js build
```

### 后端运行

在 ragflow v0.9.0 源码目录下

```
export PYTHONPATH=`pwd`
```

下载 [cl100k_base.tiktoken](https://openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken) 然后上传到离线的服务器上，指定环境变量

`export TIKTOKEN_CACHE_DIR=/home/learnai/tiktoken_cache`

启动的时候 nltk 会报错，本地下载后上传到离线的服务器上

```
nltk.download("punkt")
nltk.download("wordnet")
```

[deepdoc](https://hf-mirror.com/InfiniFlow/deepdoc) 模型本地下载后放在 /rag/res/deepdoc/ 下

```
# 后台任务
python rag/svr/task_executor.py
# web api
python api/ragflow_server.py
```

### Ollama 离线安装

[https://blog.csdn.net/u010197332/article/details/137604798](https://blog.csdn.net/u010197332/article/details/137604798)

参考这篇离线安装 ollama

因为没有网，所以 model 需要手工上传，然后指定路径 `export OLLAMA_MODEL=xxx`


默认的使用的是联网的大模型，所以需要改成本地 ollama

conf/service_conf.yaml

```
user_default_llm:
  factory: 'Ollama'
  api_key: 'sk-xxxxxxxxxxxxx'
  base_url: 'http://localhost:11434'
```

### 前端运行

参考官方文档，把编译之后的前端文件复制到 nginx 配置指定的目录下

```
sudo mkdir -p /ragflow/web
cp -r dist /ragflow/web
sudo yum install nginx -y
sudo cp ../docker/nginx/proxy.conf /etc/nginx
sudo cp ../docker/nginx/nginx.conf /etc/nginx
sudo cp ../docker/nginx/ragflow.conf /etc/nginx/conf.d
sudo systemctl start nginx
```

如果没问题的话，现在就可以打开前端页面了 `http://ip:80/`, 如果有问题再针对性的查找问题
