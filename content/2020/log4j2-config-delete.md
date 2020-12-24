Title: log4j2 配置日志清理
Status: published
Date: 2020-12-21 22:00
Modified: 2020-12-21 22:00
Category: Java
Tags: java, log4j2
Slug: log4j2-config-delete
Authors: Martin
Summary: log4j2 配置日志清理

## log4j2 delete

[官方文档 Delete on Rollover](https://logging.apache.org/log4j/2.x/manual/appenders.html#CustomDeleteOnRollover)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Configuration status="warn" name="MyApp" packages="">
  <Properties>
    <Property name="baseDir">logs</Property>
  </Properties>
  <Appenders>
    <RollingFile name="RollingFile" fileName="${baseDir}/app.log"
          filePattern="${baseDir}/$${date:yyyy-MM}/app-%d{yyyy-MM-dd}.log.gz">
      <PatternLayout pattern="%d %p %c{1.} [%t] %m%n" />
      <CronTriggeringPolicy schedule="0 0 0 * * ?"/>
      <DefaultRolloverStrategy>
        <Delete basePath="${baseDir}" maxDepth="2">
          <IfFileName glob="*/app-*.log.gz" />
          <IfLastModified age="60d" />
        </Delete>
      </DefaultRolloverStrategy>
    </RollingFile>
  </Appenders>
  <Loggers>
    <Root level="error">
      <AppenderRef ref="RollingFile"/>
    </Root>
  </Loggers>
</Configuration>
```

可以按照文件名，最后修改时间，文件数量，文件大小，第一个条件必须是 IfFileName，后面的条件如果有多个可以用 IfAll IfAny IfNot 后者本身来嵌套组合

```
<IfFileName glob="*/app-*.log.gz" />
<IfLastModified age="60d" />
<IfAccumulatedFileCount exceeds="180" />
<IfAccumulatedFileSize exceeds="10 GB" />
```

```
<Delete basePath="${baseDir}" maxDepth="2">
  <IfFileName glob="*/app-*.log.gz">
    <IfLastModified age="30d">
      <IfAny>
        <IfAccumulatedFileSize exceeds="100 GB" />
        <IfAccumulatedFileCount exceeds="10" />
      </IfAny>
    </IfLastModified>
  </IfFileName>
</Delete>
```















