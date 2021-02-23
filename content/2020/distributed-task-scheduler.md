Title: Distributed Task Scheduler
Status: published
Date: 2021-01-26 10:00
Modified: 2021-01-26 12:00
Category: Data
Tags: data
Slug: distributed-task-scheduler
Authors: Martin
Summary: 分布式任务调度

## 任务调度

简单的任务调度可以使用操作系统的服务，比如 cron 或者 windows 下的计划任务

在各个编程语言也有定时任务的支持，比如在 java 的 spring scheduler 或者 quartz

### 分布式任务调度

自从大数据浪潮开始之后，市面上有很多任务调度工具，但是很多都是只支持大数据

1. apache dolphinscheduler
2. azkaban
3. elastic-job
4. xxl-job

#### apache dolphinscheduler

[dolphinscheduler的架构设计](https://dolphinscheduler.apache.org/zh-cn/docs/1.3.4/user_doc/architecture-design.html)

依赖 zookeeper

目前正在快速更新，但是时间比较短，2019.03 开始的

### azkaban

[azkaban](https://github.com/azkaban/azkaban)

项目历史比较长，7年了

可以指定 executor

事件触发只支持 kafaka

### elastic-job

目前已经是 apache shardingsphere 的子项目 [elastic-job](https://github.com/apache/shardingsphere-elasticjob)

依赖 zookeeper

不支持指定 executor

### xxl-job

[xxl-job](https://github.com/xuxueli/xxl-job)

特点是比较轻量，跟 spring 集成非常方便

缺点就是不支持DAG和只支持cron触发
















