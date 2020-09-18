Title: Elasticsearch join 关联查询
Date: 2020-09-08 11:00
Modified: 2020-09-08 12:00
Category: Java
Tags: java, elasticsearch
Slug: elasticsearch-join
Authors: Martin
Summary: Elasticsearch join 关联查询

## Elasticsearch join 关联查询

> 下面都是基于 Elasticsearch 7.3，有些语句低版本可能不支持

下面以 question answer 一对多举例

```
curl -X PUT "localhost:9200/question-answer" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "question_id": {"type": "long"},
      "content": {"type": "text"},
      "answer_id": {"type": "long"},
      "qaRelation":{"type": "join",
         "relations": {
          "question": "answer"
           }
         },
      "dataType": {"type": "keyword"}
    }
  }
}
'
```

```
curl -X PUT "localhost:9200/question-answer/_doc/1?refresh&pretty" -H 'Content-Type: application/json' -d'
{
  "question_id": "1",
  "content": "This is a question",
  "qaRelation": {
    "name": "question" 
  },
  "dataType": "question"
}
'
curl -X PUT "localhost:9200/question-answer/_doc/2?refresh&pretty" -H 'Content-Type: application/json' -d'
{
  "question_id": "2",
  "content": "This is another question",
  "qaRelation": {
    "name": "question" 
  },
  "dataType": "question"
}
'
curl -X PUT "localhost:9200/question-answer/_doc/3?routing=1&refresh&pretty" -H 'Content-Type: application/json' -d'
{
  "answer_id": "3",
  "content": "This is an answer",
  "qaRelation": {
    "name": "answer", 
    "parent": "1" 
  },
  "dataType": "answer"
}
'
curl -X PUT "localhost:9200/question-answer/_doc/4?routing=1&refresh&pretty" -H 'Content-Type: application/json' -d'
{
  "answer_id": "4",
  "content": "This is another answer",
  "qaRelation": {
    "name": "answer",
    "parent": "1"
  },
  "dataType": "answer"
}
'
curl -X PUT "localhost:9200/question-answer/_doc/4?routing=2&refresh&pretty" -H 'Content-Type: application/json' -d'
{
  "answer_id": "4",
  "content": "This is a special answer",
  "qaRelation": {
    "name": "answer",
    "parent": "2"
  },
  "dataType": "answer"
}
'
```


### has_child

找出 answer 中内容有 another 的 question

```
GET question-answer/_search
{
  "query": {
    "has_child": {
      "type": "answer",
      "query": {
        "match": {
          "content": "another"
        }
      }
    }
  }
}
```



### has_parent

找出 question 中内容有 another 的 answer

```
GET question-answer/_search
{
  "query": {
    "has_parent": {
      "parent_type": "question",
      "query": {
        "match": {
          "content": "another"
        }
      }
    }
  }
}
```

### parent_id

根据 parent_id 找出 所有 answer

```
GET question-answer/_search
{
  "query": {
    "parent_id": {
      "type": "answer",
      "id": "1"
    }
  }
}
```


### 组合查询

question 或者 answer 中包含 another 的

```
GET question-answer/_search
{
  "query": {
    "bool": {
      "should": [
        {
          "has_child": {
            "type": "answer",
            "query": {
              "match": {
                "content": "another"
              }
            }
          }
        },
        {
          "bool": {
            "must": [
              {
                "match": {
                  "content": "another"
                }
              },
              {
                "term": {
                  "dataType": {
                    "value": "question"
                  }
                }
              }
            ]
          }
        }
      ],
      "minimum_should_match": 1
    }
  }
}
```

### Java 代码

用 RestHighLevelClient，有 DSL 对应的

```
BoolQueryBuilder hasChildBoolQueryBuilder = QueryBuilders.boolQuery();
```
 

