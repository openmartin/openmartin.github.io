Title: Oracle Express on CentOS 7
Date: 2016-09-19 20:20
Modified: 2016-09-19 20:20
Category: Linux
Tags: linux, oracle
Slug: oracle-express-editon-on-centos7
Authors: Martin
Summary: 有些时候我们需要一个Oracle的环境来做测试或实验，但是苦于没有服务器，或者不在工作环境当中。值得高兴的是，Oracle有一个Oracle Express Edition，提供了rpm安装包，快捷方便。


有些时候我们需要一个Oracle的环境来做测试或实验，但是苦于没有服务器，或者不在工作环境当中。值得高兴的是，Oracle有一个Oracle Express Edition，提供了rpm安装包，快捷方便。

## VirtualBox VM
[下载CentOS 7 DVD](https://www.centos.org)

virtualbox的网络设置中建议选择桥接，因为我们需要从宿主机连接虚拟机，默认的NAT只能从虚拟机内部访问外部。

安装过程中建议选择Server with GUI，再选择develop tools。

安装完成之后，需要同意license(比较坑)，先按1，再按2同意条款，接下来按C继续。

## Oracle Express Edition
在Oracle 官网下载[Oracle Database Express Edition 11g Release 2](http://www.oracle.com/technetwork/database/database-technologies/express-edition/downloads/index.html)

下载下来之后是一个rpm包，`oracle-xe-11.2.0-1.0.x86_64.rpm`，上传到虚拟机当中安装，`sudo rmp -i oracle-xe-11.2.0-1.0.x86_64.rpm`

## CentOS
```shell
#使用root用户来初始化数据库，默认的实例名是XE
/etc/init.d/oracle-xe configure
```
`Usage: /etc/init.d/oracle-xe {start|stop|restart|force-reload|configure|status|enable|disable}`

Oracle Express Edition 安装好之后会有一个oracle用户，通过root切换到oracle用户，`source /u01/app/oracle/prduct/11.2.0/xe/bin/oracle_env.sh`设置Oracle 的环境变量，接下来就可以用一些Oracle的命令了。

### Disable Firewall
centos 默认有一个firewall，会阻止外部的访问，所以需要停止防火墙。
使用root用户登录
```
systemctl disable firewalld
systemctl stop firewalld
```

## Oracle SQL Developer
在macOS下没有PLSQL Developer这样方便的工具，Oracle官方出品的[Oracle SQL Developer](http://www.oracle.com/technetwork/developer-tools/sql-developer/downloads/index.html)可以体验一下，一般功能都有。

