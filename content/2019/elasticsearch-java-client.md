Title: Elasticsearch Java Client
Date: 2019-08-22 10:57
Modified: 2019-08-22 10:57
Category: Java
Tags: java, elasticsearch
Slug: elasticsearch-java-client
Authors: Martin
Summary: Elasticsearch Java Client 配置和使用

## Java REST Client

### maven 配置

```xml
<dependency>
    <groupId>org.elasticsearch.client</groupId>
    <artifactId>elasticsearch-rest-high-level-client</artifactId>
    <version>7.2.0</version>
</dependency>
```

###　spring 构建 RestHighLevelClient 对象

```xml
<!-- config elasticsearch RestHighLevelClient -->
<bean id="httpHost" class="org.apache.http.HttpHost">
    <constructor-arg index="0" value="${elasticsearch.host}"/>
    <constructor-arg index="1" value="${elasticsearch.port}"/>
</bean>

<bean id="restClientBuilder" class="org.elasticsearch.client.RestClientBuilder">
    <constructor-arg index="0">
        <list>
            <bean class="org.elasticsearch.client.Node">
                <constructor-arg index="0" ref="httpHost"/>
            </bean>
        </list>
    </constructor-arg>
</bean>

<bean id="restHighLevelClient" class="org.elasticsearch.client.RestHighLevelClient" destroy-method="close">
    <constructor-arg index="0" ref="restClientBuilder"/>
</bean>
```

### 使用 Demo

API 使用方法 https://www.elastic.co/guide/en/elasticsearch/client/java-rest/current/java-rest-high-search.html

```java
SearchRequest searchRequest = new SearchRequest("web-log-2019-01");
SearchSourceBuilder searchSourceBuilder = new SearchSourceBuilder();

// 设置分页
searchSourceBuilder.from(0);
searchSourceBuilder.size(10);

// 设置查询条件
searchSourceBuilder.query(QueryBuilders.matchPhraseQuery("title", queryword));

// 设置 exclude
String[] excludeFields = new String[] {"content"};
searchSourceBuilder.fetchSource(null, excludeFields);

searchRequest.source(searchSourceBuilder);

// send request and get response
SearchResponse searchResponse = restHighLevelClient.search(searchRequest, RequestOptions.DEFAULT);
SearchHits hits = searchResponse.getHits();
SearchHit[] searchHits = hits.getHits();
for (SearchHit hit : searchHits) {
    // do something with the SearchHit
    System.out.println(hit.getSourceAsString());
}
```

## Elasticsearch SQL

### maven 配置

添加 repository

```xml
<repository>
    <id>elastic.co</id>
    <name>Elastic Repository</name>
    <url>https://artifacts.elastic.co/maven</url>
</repository>
```

dependency

```xml
<dependency>
    <groupId>org.elasticsearch.plugin</groupId>
    <artifactId>x-pack-sql-jdbc</artifactId>
    <version>${es.version}</version>
</dependency>
```

### Elasticsearch SQL + mybatis + spring

Elasticsearch SQL 可以和 mybatis, spring 结合起来，和关系型数据库一样的开发模式

因为 SQL 和 Elasticsearch DSL 不能完全对，适合比较简单的场景

