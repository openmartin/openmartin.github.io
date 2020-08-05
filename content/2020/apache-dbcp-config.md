Title: apache dbcp 配置
Status: published
Date: 2020-08-05 14:00
Modified: 2020-08-05 14:00
Category: Java
Tags: java, dbcp, apache
Slug: apache-dbcp-config
Authors: Martin
Summary: apache dbcp 各个属性的配置

## dbcp 连接属性

官方文档 [https://commons.apache.org/proper/commons-dbcp/configuration.html](https://commons.apache.org/proper/commons-dbcp/configuration.html) 里详细写了每个属性的意义


| 属性                 | 描述                                               |
| :------------------- | :------------------------------------------------- |
| username             |                                                    |
| password             |                                                    |
| url                  | example: jdbc:oracle:thin:@192.168.100.1:1521:orcl |
| driverClassName      | example: oracle.jdbc.driver.OracleDriver           |
| connectionProperties | 连接时的属性，分号分隔  propertyName=property;     |


| 属性                        | 默认值         | 描述                                                                                          |
| :-------------------------- | :------------- | :-------------------------------------------------------------------------------------------- |
| defaultAutoCommit           | driver default | auto-commit 状态，如果没有设置，则使用 driver 的默认值                                        |
| defaultReadOnly             | driver default | read-only 状态，如果没有设置，则使用 driver 的默认值                                          |
| defaultTransactionIsolation | driver default | 默认的事务隔离类型 NONE \ READ_COMMITTED \ READ_UNCOMMITTED \ REPEATABLE_READ \ SERIALIZABLE  |
| defaultCatalog              |                | 比如 mysql 和sqlserver 可以指定哪个库                                                         |
| cacheState                  | true           | auto-commit 和    read-only 的状态在第一次读和写就缓存了，避免额外的查询和 getter 调用        |
| defaultQueryTimeout         | null           | null 使用 driver 的默认值，或者是一个 Integer 表示 超时时间                                   |
| enableAutoCommitOnReturn    | true           | true 当connections被归还给pool 时，设置 Connection.setAutoCommit(true)                        |
| rollbackOnReturn            | true           | true 当 auto-commit 没被启用，而且不是 read-only 时，roll back  当 connection 被归还给 pool时 |


## dbcp pool 属性

| 属性          | 默认值 | 描述                                                       |
| :------------ | :----- | :--------------------------------------------------------- |
| initialSize   | 0      | 连接池初始化的时候连接数                                   |
| maxTotal      | 8      | 连接池中最大被占用的连接数，-1 是没有限制                  |
| maxIdle       | 8      | 连接池中最大空闲的连接数，-1 是没有限制                    |
| minIdle       | 0      | 连接池中最小空闲的连接数，如果有空闲的连接则不用再创建一个 |
| maxWaitMillis | 0      | 从连接池中获取连接的超时时间， -1 是一只等待               |


| 属性                           | 默认值     | 描述                                                                                                 |
| :----------------------------- | :--------- | :--------------------------------------------------------------------------------------------------- |
| validationQuery                | 0          | 测试连接的语句，在返回给申请数据库连接的 caller 之前调用，如果不设置，调用 driver 的 isValid()       |
| validationQueryTimeout         | no timeout | 测试连接的语句的执行超时时间                                                                         |
| testOnCreate                   | false      | 在连接创建时是否测试有效，如果连接无效，则导致连接连接创建的 borrow 操作会失败                       |
| testOnBorrow                   | true       | 从连接池中 borrow 时是否测试有效，如果无效，则从连接池中 drop 这个连接，再次尝试 borrow              |
| testOnReturn                   | false      | 归还给连接池的时候是否测试有效                                                                       |
| testWhileIdle                  | false      | 是否测试空闲的数据库连接                                                                             |
| timeBetweenEvictionRunsMillis  | -1         | evictor线程检测空闲连接是否有效的间隔，-1 是不启动线程                                               |
| numTestsPerEvictionRun         | 3          | 设定evictor线程在进行空闲连接检测有效时，每次检查几个链接                                            |
| minEvictableIdleTimeMillis     | 1000×60×30 | 一个连接多长时候空闲之后，被evictor线程销毁                                                          |
| softMinEvictableIdleTimeMillis | -1         | 一个连接多长时候空闲之后，且当前连接池的空闲连接数大于最小空闲连接数 minIdle，被evictor线程销毁      |
| maxConnLifetimeMillis          | -1         | 一个连接最长的生命周期，如果超过了这个时间，下一次 activation, passivation or validation test 将失败 |
| logExpiredConnections          | true       | 超过 maxConnLifetimeMillis 关闭连接的日志标志                                                        |
| connectionInitSqls             | null       | 当连接创建时设置执行的SQL                                                                            |
| lifo                           | true       | 获取连接时的策略，true LIFO 后进先出, false FIFO 先进先出                                            |


| 属性                      | 默认值    | 描述                                                             |
| :------------------------ | :-------- | :--------------------------------------------------------------- |
| poolPreparedStatements    | false     | 是否启用 prepared statement pooling                              |
| maxOpenPreparedStatements | unlimited | 最大的 open statements，跟数据库的支持也有关系，比如最大有游标数 |


当连接被获取后，没有被释放，而且也没有执行任何操作，可以由连接池主动回收，下面就是这样的配置

Creating a Statement, PreparedStatement or CallableStatement or using one of these to execute a query (using one of the execute methods) resets the lastUsed property of the parent connection.

| 属性                         | 默认值 | 描述                                                          |
| :--------------------------- | :----- | :------------------------------------------------------------ |
| removeAbandonedOnMaintenance | false  | 设置 timeBetweenEvictionRunsMillis 之后，evictor线程主动回收  |
| removeAbandonedOnBorrow      | false  | getNumActive() > getMaxTotal() - 3 && getNumIdle() < 2        |
| removeAbandonedTimeout       | 300    | 标记为 Abandoned 连接的超时时间                               |
| logAbandoned                 | false  | 是否打印日志，true 打印 stack trace，影响性能                 |
| abandonedUsageTracking       | false  | true 每次调用连接池中的方法都会打印 stack trace，严重影响性能 |

## 调用的时序图


见 官方文档 [https://commons.apache.org/proper/commons-dbcp/guide/sequencediagrams.html](https://commons.apache.org/proper/commons-dbcp/guide/sequencediagrams.html)