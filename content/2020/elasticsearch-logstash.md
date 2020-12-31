Title: Elasticsearch Logstash
Status: published
Date: 2020-11-27 11:00
Modified: 2020-11-27 12:00
Category: Java
Tags: elasticsearch, logstash
Slug: elasticsearch-logstash
Authors: Martin
Summary: Elasticsearch Logstash 配置

## Logstash + GELF

配置文件

```
input {
    gelf {
        port => 12201
    }
}
filter {
    json {
        source => "message"
		remove_field => [ "server", "server.fqdn", "timestamp" ]
    }
}
output {
  stdout { codec => rubydebug }

if "_jsonparsefailure" not in [tags] {
  elasticsearch {
    hosts => ["192.168.100.100:9200"]
    index => "logstash-search-log-%{+YYYYMMDD}"
    }
  }
}
```

logstash 启动命令

```
bin\logstash.bat -f log4j2-gelf.conf
```


log4j2 gelf 配置

添加依赖关系

```xml
<dependency>
  <groupId>biz.paluch.logging</groupId>
  <artifactId>logstash-gelf</artifactId>
  <version>1.13.0</version>
</dependency>
```

log4j2.xml 中添加 Gelf 配置, 然后在需要的包下添加 appender 就行

```xml
<Gelf name="GELF" host="udp:127.0.0.1" port="12201" version="1.1" extractStackTrace="true"
      filterStackTrace="true" mdcProfiling="true" includeFullMdc="true" maximumMessageSize="8192"
      originHost="%host{fqdn}" additionalFieldTypes="fieldName1=String,fieldName2=Double,fieldName3=Long">
    <Field name="timestamp" pattern="%d{dd MMM yyyy HH:mm:ss,SSS}" />
    <Field name="level" pattern="%level" />
    <Field name="simpleClassName" pattern="%C{1}" />
    <Field name="className" pattern="%C" />
    <Field name="server" pattern="%host" />
    <Field name="server.fqdn" pattern="%host{fqdn}" />

    <!-- This is a field using MDC -->
    <Field name="userId" mdc="userId" />
</Gelf>
```

```java
ObjectMapper objectMapper = new ObjectMapper();
HashMap<String, Object> jsonLog = new HashMap<>();
jsonLog.put("ip", IpUtils.getIpAddr(request));
jsonLog.put("ua", userAgent);
jsonLog.put("browser", browser);
jsonLog.put("browserType", browserType);
jsonLog.put("browserMajorVersion", browserMajorVersion);
jsonLog.put("deviceType", deviceType);
jsonLog.put("platform", platform);
jsonLog.put("platformVersion", platformVersion);

logger.info(searchMarker, objectMapper.writeValueAsString(jsonLog));
```