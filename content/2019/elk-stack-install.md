Title: ELK 全家桶安装
Date: 2019-07-30 14:06
Modified: 2019-07-30 14:06
Category: Java
Tags: java, elasticsearch, kibana
Slug: elk-stack-install
Authors: Martin
Summary: ELK 全家桶安装


## ElasticSearch 安装

### environment

CentOS 7.2

ElasticSearch 7.2.0

### install

通过 rpm 安装，参考 https://www.elastic.co/guide/en/elasticsearch/reference/current/rpm.html

### 启动和优化

```
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable elasticsearch.service
sudo systemctl start elasticsearch.service
sudo systemctl stop elasticsearch.service
sudo systemctl status kibana.service
```

/etc/elasticsearch/jvm.options

```
-Xms32g
-Xms32g
```

/etc/elasticsearch/elasticsearch.yml 单机只有一个节点

```
network.host: 0.0.0.0
cluster.name: my-application  # 集群中的名称
node.name: master  # 该节点名称
cluster.initial_master_nodes: ["master"] 
```


### plugin elasticsearch-analysis-hanlp

https://github.com/KennFalcon/elasticsearch-analysis-hanlp

建议使用方式二，然后把 Hanlp 的 model 文件复制到 /usr/share/elasticsearch/plugins/analysis-hanlp/data/model

```
chown -R elasticsearch:elasticsearch /usr/share/elasticsearch/plugins/
```


## Kibana 安装

### install

通过 rpm 安装，参考 https://www.elastic.co/guide/en/kibana/current/rpm.html

### 启动和配置

```
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable kibana.service
sudo systemctl start kibana.service
sudo systemctl stop kibana.service
sudo systemctl status kibana.service
```

/etc/kibana/kibana.yml

```
server.host: "0.0.0.0"
```


## Java REST Client


```xml
<dependency>
    <groupId>org.elasticsearch.client</groupId>
    <artifactId>elasticsearch-rest-high-level-client</artifactId>
    <version>7.2.0</version>
</dependency>
```


## Elasticsearch SQL

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


Elasticsearch SQL 可以和 mybatis, spring 结合起来，和关系型数据库一样的开发模式











