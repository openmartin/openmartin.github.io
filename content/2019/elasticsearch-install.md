Title: Elasticsearch 安装
Date: 2019-07-30 14:06
Modified: 2019-07-30 14:06
Category: Java
Tags: elasticsearch, kibana
Slug: elasticsearch-install
Authors: Martin
Summary: Elasticsearch 安装，Kibana 安装，


## ElasticSearch 安装

### environment

CentOS 7.2

ElasticSearch 7.3.0

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

### rpm 安装 ElasticSearch 之后的目录结构

```
/usr/share/elasticsearch  # ES_HOME
/var/log/elasticsearch    # log 目录
/etc/elasticsearch        # config 目录
/var/lib/elasticsearch    # data 目录
```

### plugin elasticsearch-analysis-hanlp

https://github.com/KennFalcon/elasticsearch-analysis-hanlp

建议使用 Elasticsearch 命令行安装插件

```
./elasticsearch-plugin install file:///home/demo/elasticsearch-analysis-hanlp-7.3.0.zip
```

插件 在 `/usr/share/elasticsearch/plugins/anlysis-hanlp` 目录下
配置文件在 `/etc/elasticsearch/analysis-hanlp` 目录下

修改 hanlp.properties, root 修改为绝对路径 `root=/usr/share/elasticsearch/plugins/analysis-hanlp/`

然后把 hanlp 的 数据文件复制到 /usr/share/elasticsearch/plugins/analysis-hanlp/data

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














