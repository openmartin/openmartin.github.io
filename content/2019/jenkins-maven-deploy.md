Title: 使用 Jenkins 来自动化部署 Maven 项目
Date: 2019-07-08 15:06
Modified: 2019-07-08 15:06
Category: Java
Tags: java, jenkins, maven, tomcat
Slug: jenkins-maven-deploy
Authors: Martin
Summary: 使用 Jenkins 来自动化部署 Maven 项目，把一个 WebApp 项目部署到 tomcat


## 安装 Jenkins

下载 [jenkin.war](https://jenkins.io/zh/download/), 可以当作一个独立的 jar 文件运行。

```
nohup java -jar jenkins.war --httpPort=8080 &
```


### 安装后设置向导

参考[官方文档](https://jenkins.io/zh/doc/book/installing/#setup-wizard)

### 安装 BlueOcean 和 Maven 插件

下面三个 GitLab 如果是需要 GitLab Push 触发，则需要安装

- Blue Ocean (BlueOcean Aggregator)
- Maven Integration plugin
- GitLab Plugin
- GitLab API plugin
- GitLab Hook Plugin

## 配置 Maven

编辑`$HOME/.m2/settings.xml`， 如果是在内网中，需要设置代理，如果网速不够快，可以设置 aliyun 镜像

```xml
<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0
  https://maven.apache.org/xsd/settings-1.0.0.xsd">
  <proxies>

    <proxy>
      <id>http proxy</id>
      <active>true</active>
      <protocol>http</protocol>
      <host>192.168.8.8</host>
      <port>8080</port>
      <username></username>
      <password></password>
    </proxy>

    <proxy>
      <id>https proxy</id>
      <active>true</active>
      <protocol>https</protocol>
      <host>192.168.8.8</host>
      <port>8080</port>
      <username></username>
      <password></password>
    </proxy>
  </proxies>

  <mirrors>
    <mirror>
      <id>aliyun</id>
      <name>aliyun maven</name>
      <url>http://maven.aliyun.com/nexus/content/groups/public/</url>
      <mirrorOf>central</mirrorOf>
    </mirror>
  </mirrors>

</settings>
```


## 配置 Jenkins 流水线

编辑 `Jenkinsfile` 文件

很多例子中都是用了 docker 来准备环境，其实不是用 docker 也可以，前提条件是系统中配置了所需要的工具，比如 maven，java

如果是通过 `java -jar jenkins.war --httpPort=8080` 运行的，则可以使用的命令和当前用户一样

如果是通过 yum，apt 之类的工具安装的 Jenkins service，则使用的是 jenkins 用户，需要配置 jenkins 用户的 shell 环境。

```
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'mvn -B -DskipTests clean package'
            }
        }
        stage('Deploy') {
            steps {
                sh './doc/deploy-test.sh'
            }
        }
    }
}
```

## 使用 curl 通过 tomcat manager 部署 war

先配置登录 manager 的用户

1. 配置 webapps\manager\META-INF\context.xml，允许远程登录
```xml
<Context antiResourceLocking="false" privileged="true" >
  <Valve className="org.apache.catalina.valves.RemoteAddrValve"
         allow="127\.\d+\.\d+\.\d+|::1|0:0:0:0:0:0:0:1|192\.168\.\d+\.\d+\.|10\.\d+\.\d+\.\d+" />
  <Manager sessionAttributeValueClassNameFilter="java\.lang\.(?:Boolean|Integer|Long|Number|String)|org\.apache\.catalina\.filters\.CsrfPreventionFilter\$LruCache(?:\$1)?|java\.util\.(?:Linked)?HashMap"/>
</Context>
```

2. 配置 conf\tomcat-user.xml
```xml
  <role rolename="manager-gui"/>
  <role rolename="manager-script"/>
  <role rolename="manager-status"/>
  <user username="tomcat" password="tomcat" roles="manager-gui"/>
  <user username="jenkins" password="jenkins" roles="manager-script, manager-status"/>
```

3. curl 

在 tomcat 配置完之后，就可以使用 curl 来 undeploy 和 deploy war 文件， 所有可以使用的命令参考 [tomcat manager](http://192.168.142.239:8080/docs/manager-howto.html#Supported_Manager_Commands)

```shell
# !/bin/bash
unset http_proxy
unset https_proxy

echo 'undeploy rms'
set -x
curl -s -u jenkins:jenkins "http://192.168.142.239:8080/manager/text/undeploy?path=/rms"
set +x

echo 'deploy rms'
set -x
curl -s -u jenkins:jenkins -T target/rms.war "http://192.168.142.239:8080/manager/text/deploy?path=/rms"
set +x
```

## Gitlab 触发 Jenkins pipline

参考 [https://www.jianshu.com/p/156de44a44c2](https://www.jianshu.com/p/156de44a44c2)


1. 在 GitLab 中添加 ssh key，在 Jenkins 运行的用户下可以免密码 clone
2. Jenkins Job 的构建触发器 选择 Build when a change is pushed to GitLab. GitLab webhook URL: http://10.80.28.27:8080/project/deploy-test，在高级选项中可以设置 Allowed branches -> master
3. 在 GitLab 项目 Settings -> Integrations -> Webhooks 配置上面的 URL，下面有测试的按钮，如果是 200 OK 就正常

