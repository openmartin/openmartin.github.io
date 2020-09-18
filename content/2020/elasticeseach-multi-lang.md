Title: Elasticsearch 多语言搜索
Date: 2020-09-07 11:00
Modified: 2020-09-07 12:00
Category: Java
Tags: java, elasticsearch
Slug: elasticsearch-multi-lang
Authors: Martin
Summary: Elasticsearch 多语言搜索

## Elasticsearch 多语言搜索

如果需要同时搜索多个语言，Elasticsearch 应该如何优化

方案1 是在分词层面做，比如让[中文分词器可以处理中英文混合文档](https://blog.csdn.net/hereiskxm/article/details/47441911)
方案2 把资料切分成不同的语言，根据用户的主语言自动选择不同的 index 或者 field [每份文档一种语言](https://www.elastic.co/guide/cn/elasticsearch/guide/current/one-lang-docs.html) [混合语言的陷阱](https://www.elastic.co/guide/cn/elasticsearch/guide/current/language-pitfalls.html)
方案3 把资料切分成不同的语言，搜索的时候同时搜索

### 实践

根据目前的实际情况，采用方案3

- 根据原始数据分了两个 index (cn-index, en-index)
- 中文搜索采用 matchPhraseQuery 需要完全匹配关键词，但是英文因为词形的变化，会自动转换成词根，所以用 matchPhrase
- 优先显示中文， matchPhraseQuery 的 boost 调高

