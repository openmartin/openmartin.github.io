Title: 修复 virtualenv 环境
Date: 2020-05-25 12:00
Modified: 2020-05-25 12:00
Category: Python
Tags: python, virtualenv
Slug: fix-python-virtualenv
Authors: Martin
Summary: 很多时候升级 python 之后，virtualenv 中的软链接会失效，这时候就需要修复了

## 问题

升级 python 之后，很多时候就会发现 virtualenv 失效了，因为 virtualenv 使用软链接链接到系统的 python, 系统的 python path 变化导致 virtualenv 失效


### 简单的修复

```
find . -type l -delete
cd ..
virtualenv -p python3 v_env
```

已经安装的 package 不需要重新安装

### 复杂的修复

有时候如果 python 版本有比较大的变动，系统的 site-packages 有很多更新，这个时候需要重新生成 virtualenv

```
# 保存已经安装的 package
pip freeze > requirements.txt
# 根据需要看看 package 是否需要更新版本
# 重新生成 virtualenv
virtualenv -p python3 new_env
# 安装 package
pip install -r requirements.txt
```

