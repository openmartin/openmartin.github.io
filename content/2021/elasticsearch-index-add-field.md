Title: Elasticsearch index 添加新字段
Status: published
Date: 2021-04-12 10:00
Modified: 2021-04-12 12:00
Category: Java
Tags: java, elasticsearch
Slug: elasticsearch-index-add-field
Authors: Martin
Summary: Elasticsearch index 添加新字段


Elasticsearch 添加新字段和修改字段类型

## 新增字段

新增字段如果没有特别制定的类型，es会自动创建这个字段，如果需要指定分词工具或者特殊类型的，需要修改 mapping

```bash
# 查看 mapping
curl -XGET 'localhost:9200/netdisk-document-v1/_mapping/?pretty'

# 修改索引 可以只传增加的字段
curl -X PUT "localhost:9200/netdisk-document-v1" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "content_add": {"type": "text" , "analyzer": "hanlp_index", "search_analyzer": "hanlp_nlp", "index_options" : "offsets"}, 
    }
  }
}
'
```

## 修改字段类型需要 reindex

es 不支持修改字段类型，如果需要修改字段类型，先新建一个索引， 设置新的 mapping，然后把原数据 reindex 到新的索引上

```bash
# 新建 索引
curl -X PUT "localhost:9200/netdisk-document-v2" -H 'Content-Type: application/json' -d'
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
# reindex
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
# 修改 别名指向
curl -X DELETE "localhost:9200/netdisk-document-v1/_alias/netdisk-document?pretty"
curl -X PUT "localhost:9200/netdisk-document-v2/_alias/netdisk-document?pretty"
```



