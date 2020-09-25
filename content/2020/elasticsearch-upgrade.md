Title: Elasticsearch upgrade
Date: 2020-09-17 10:00
Modified: 2020-09-17 12:00
Category: Java
Tags: java, elasticsearch
Slug: elasticsearch-upgrade
Authors: Martin
Summary: Elasticsearch upgrade

## Elasticsearch Upgrade

elasticseach 版本升级 (rpm 安装)

### rpm

```
systemctl stop elasticsearch.service
systemctl stop kibana.service
yum install elasticsearch-7.5.1
yum install kibana-7.5.1
systemctl start elasticsearch.service
systemctl start kibana.service
```

## elasticsearch-analysis-hanlp

ES_HOME=/usr/share/elasticsearch
ES_DATA=/var/lib/elasticsearch

```
/usr/share/elasticsearch/bin/elasticsearch-plugin install https://github.com/KennFalcon/elasticsearch-analysis-hanlp/releases/download/v7.5.1/elasticsearch-analysis-hanlp-7.5.1.zip
```

```
/usr/share/elasticsearch/bin/elasticsearch-plugin install file:///root/es-hanlp/elasticsearch-analysis-hanlp-7.5.1.zip
```

```
cp data-1.7.5.zip /usr/share/elasticsearch/plugins/analysis-hanlp
unzip data-1.7.5.zip
```


