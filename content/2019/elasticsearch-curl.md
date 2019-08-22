Title: Elasticsearch 常用 curl 命令
Date: 2019-08-22 11:11
Modified: 2019-08-22 11:11
Category: Java
Tags: java, elasticsearch
Slug: elasticsearch-java-client
Authors: Martin
Summary: 虽然可以通过各种语言的 client 来操作 Elasticsearch，但是 curl 还是最方便和最常用的。

## Elasticsearch 常用 curl 命令

虽然可以通过各种语言的 client 来操作 Elasticsearch，但是 curl 还是最方便和最常用的。

### 查看 Elasticsearch 版本

```sh
curl -XGET 'localhost:9200'
```

```json
{
  "name" : "node-1",
  "cluster_name" : "rs-application",
  "cluster_uuid" : "ouChgr_bTKmGm4MicVEt6g",
  "version" : {
    "number" : "7.3.0",
    "build_flavor" : "default",
    "build_type" : "rpm",
    "build_hash" : "de777fa",
    "build_date" : "2019-07-24T18:30:11.767338Z",
    "build_snapshot" : false,
    "lucene_version" : "8.1.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
```

### 查看索引状态

```sh
curl -XGET 'localhost:9200/_cat/indices?v&pretty'
```

```sh
health status index                   uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   .kibana_task_manager    EYi69PoYQASniv_dTpvkdA   1   0          2            0     30.8kb         30.8kb
green  open   kibana_sample_data_logs L0oSKJgnRmOxCp3zSHZojw   1   0      14075            0     11.5mb         11.5mb
green  open   .kibana_1               SaISvKYHQ6Su72LVtLpv9A   1   0         44            1    127.7kb        127.7kb
```

### 新建 index mapping

```sh
curl -X PUT "localhost:9200/netdisk-document-v1" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "docId": {"type": "long"},
      "title":   {"type": "text", "analyzer": "hanlp_index", "search_analyzer": "hanlp_nlp", "index_options" : "offsets"}, 
      "content": {"type": "text" , "analyzer": "hanlp_index", "search_analyzer": "hanlp_nlp", "index_options" : "offsets"}, 
      "uploadDate": {"type": "date"}
    }
  }
}
'
```

### 查看 index mapping

```sh
curl -XGET 'localhost:9200/netdisk-document-v1/_mapping/?pretty'
```

### 删除 index

```sh
curl -X DELETE 'localhost:9200/netdisk-document-v1?pretty'
```

### 设置 index 别名 alias

```sh
curl -X PUT "localhost:9200/netdisk-document-v1/_alias/netdisk-document?pretty"
```

### 删除 index 别名 alias

```sh
curl -X DELETE "localhost:9200/netdisk-document-v1/_alias/netdisk-document?pretty"
```

### alias 和 index 互查

```sh
curl -X GET "localhost:9200/*/_alias/netdisk-document?pretty"
```

```sh
curl -X GET "localhost:9200/netdisk-document-v1/_alias/*?pretty"
```

返回的结果都是

```json
{
  "netdisk-document-v1" : {
    "aliases" : {
      "netdisk-document-cn" : { }
    }
  }
}
```

### 重建索引 reindex

因为 index 的 mapping 只能新增字段，不能修改现有的字段，只能通过重建索引可以完成

```sh
curl -X POST "localhost:9200/_reindex?pretty" -H 'Content-Type: application/json' -d'
{
  "source": {
    "index": "netdisk-document-v1"
  },
  "dest": {
    "index": "netdisk-document-v2"
  }
}
'
```

### 查看 Elasticsearch 后台任务

可以查看重建索引目前的进度

```
curl -X GET "localhost:9200/_tasks?detailed=true&actions=*reindex&pretty"
```

### 新增记录和查询

新增和更新记录

```sh
curl -X PUT "localhost:9200/netdisk-document-v1/_doc/123" -H 'Content-Type: application/json' -d'
{
    "title": "这是一个测试标题", 
    "content": "这是一个测试内容", 
    "uploadDate": "2019-08-08T08:00:00"
}
'
```

删除记录

```sh
curl -X DELETE "localhost:9200/netdisk-document-v1/_doc/123"
```

查询 DSL

term/match/match_phrase 的区别 `https://www.jianshu.com/p/eb30eee13923`

设置 minimum_should_match `https://my.oschina.net/u/3625378/blog/1492575`

```sh
curl -XGET "http://localhost:9200/report-doc-cn/_search?pretty" -H 'Content-Type: application/json' -d'
{
    "query": {
        "match_phrase": {
            "title": {
                "query": "新能源"
            }
        }
    }
}'
```


### 测试 analyzer

```
curl -XPOST 'http://localhost:9200/_analyze?pretty' -H 'Content-Type: application/json' -d'
{
  "analyzer": "hanlp_index",
  "text": "5G是未来重要的趋势"
}'
```

