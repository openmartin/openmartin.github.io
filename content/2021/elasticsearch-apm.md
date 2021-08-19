Title: Elasticsearch APM 监控
Status: published
Date: 2021-08-11 18:00
Modified: 2021-08-11 19:00
Category: Java
Tags: java, elasticsearch
Slug: elasticsearch-apm-monitoring
Authors: Martin
Summary: 设置免费的 Elasticsearch APM 和 网页性能监控


## Elasticsearch APM

[添加 Elasticsearch RPM Repo](https://www.elastic.co/guide/en/elasticsearch/reference/current/rpm.html)

安装 APM Server

```
yum install -y apm-server-7.10.2
systemctl start apm-server
systemctl status apm-server
```

修改配置文件 `/etc/apm-sever/apm-server.yml`，允许外部访问，如果有防火墙设置的话，设置防火墙例外。

```
host: "0.0.0.0:8200"
```


安装 [APM Agent](https://www.elastic.co/guide/en/apm/agent/index.html)

选择对应的 Agent 安装方式，下面介绍一下 tomcat 怎么添加 agent

在 setenv.bat(windows) 中添加

```
set "JAVA_OPTS=-javaagent:D:\apache-tomcat-8.5.39\lib\elastic-apm-agent-1.25.0.jar -Delastic.apm.service_name=rms-test -Delastic.apm.server_url=http://192.168.100.1:8200 -Delastic.apm.application_packages=com.example"
```

在 kibana 的界面 Observability -> APM 可以看到监测的结果，可以看到每个请求的响应时间，会拆分到SQL执行的时长，Java的执行时长，方便后续分析问题。

## Elasticsearch User Experience Monitoring

默认没有启用这块的配置，需要先[改配置文件](https://www.elastic.co/guide/en/apm/server/7.14/configuration-rum.html)，然后重启 apm-server

```yaml
  rum:
    enabled: true
    event_rate:
      limit: 300
      lru_size: 1000
    allow_origins: ['*']
```

在页面引入 js agent，参考[install RUM agent](https://www.elastic.co/guide/en/apm/agent/rum-js/current/install-the-agent.html)






