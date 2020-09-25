Title: fscrawler for Elasticsearch 文件系统索引
Status: published
Date: 2020-09-20 18:00
Modified: 2020-09-20 19:00
Category: Java
Tags: java, elasticsearch
Slug: fscrawler-for-elasticsearch
Authors: Martin
Summary: fscrawler for Elasticsearch文件系统索引


## fscrawler for Elasticsearch

如果需要搜索本地文件，索引数据放到 Elasticsearch 可以试试
https://github.com/dadoonet/fscrawler

程序可以定时索引本地文件系统，增加新文件，更新已经索引的文件，移除已删除的文件

解析文件的过程调用 [apache tika](https://tika.apache.org/)，把各种格式的文件转换成文本，导入到 Elasticsearch

### config

> 需要 Java 1.8 及以上

新建配置目录

```sh
# 在当前目录下新建配置目录 config\job_name
$ bin/fscrawler --config_dir config job_name
18:28:58,174 WARN  [f.p.e.c.f.FsCrawler] job [job_name] does not exist
18:28:58,177 INFO  [f.p.e.c.f.FsCrawler] Do you want to create it (Y/N)?
y
```

建立配置目录如下

```
config
│
├─job_name
│      _settings.yaml
│
└─_default
    ├─6
    │      _settings.json
    │      _settings_folder.json
    │
    └─7
            _settings.json
            _settings_folder.json
```

最重要的配置文件是 `job_name\_settings.yaml`，配置参考 [Job file specification](https://fscrawler.readthedocs.io/en/latest/admin/fs/index.html)

`_default\6\_settings.json` 对应 es 6.x 版本，`_default\7\_settings.json` 对应 es 7.x 版本，只有一个地方可能需要修改，就是 content 的分词方法，我这里用的是 hanlp_index

```json
"content": {
        "type": "text", "analyzer": "hanlp_index", "search_analyzer": "hanlp_index", "index_options":  "offsets"
      },
```

### run

```
fscrawler-es7-2.7-SNAPSHOT\bin\fscrawler.bat --config_dir config job_name
```

### 其他

记录日志：可以指定一个log4j2.xml

```
set FS_JAVA_OPTS="-Dlog4j.configurationFile=file:///D:/fscrawler/config/log4j2.xml"
```

开启 [REST service](https://fscrawler.readthedocs.io/en/latest/admin/fs/rest.html)

```
fscrawler-es7-2.7-SNAPSHOT\bin\fscrawler.bat --rest --config_dir config job_name
```





