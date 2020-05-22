Title: 在 centos 7 上安装 redis 6
Date: 2020-05-22 17:00
Modified: 2020-05-22 17:00
Category: Linux
Tags: centos, redis
Slug: redis-6-on-centos-7-setup
Authors: Martin
Summary: 在 centos 7 上安装 最新的 redis 6 的步骤

## 遇到的问题

在 centos  7 的 yum 源中 redis 的版本为 3.2.12-2.el7，想要安装最新版的 redis 6，只能通过源代码安装，但是默认的环境会遇到编译问题，如下：

```
In file included from server.c:30:0:
server.h:1022:5: error: expected specifier-qualifier-list before '_Atomic'
     _Atomic unsigned int lruclock; /* Clock for LRU eviction */
     ^
```

是因为默认的 gcc 版本(gcc version 4.8.5)太低导致，不支持新特性

## 解决办法

解决办法就是升级 gcc 版本

升级到 gcc 7.3
```
sudo yum -y install centos-release-scl
sudo yum -y install devtoolset-7-gcc devtoolset-7-gcc-c++ devtoolset-7-binutils
sudo scl enable devtoolset-7 bash
```

还可以选择升级到其他版本

```
devtoolset-8: gcc 8.3
devtoolset-9: gcc 9.1
```

升级完成之后并不会覆盖系统默认的gcc，需要使用脚本来切换，x为要启用的版本

```sh
scl enable devtoolset-x bash 
```

## 安装和配置

后续就可以按照常规安装步骤来执行，就不再赘述了

```sh
$ wget http://download.redis.io/releases/redis-6.0.3.tar.gz
$ tar xzf redis-6.0.3.tar.gz
$ cd redis-6.0.3
$ make
```

修改配置文件

```
bind 192.168.1.100 127.0.0.1 ::1 
daemonize yes
appendonly yes
```

打开 appendonly yes 后，会启用 RDB-AOF 混合持久化



