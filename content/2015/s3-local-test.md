Title: s3 本地测试环境的搭建
Date: 2015-09-30 20:20
Modified: 2015-09-30 20:20
Category: Python
Tags: s3, aws
Slug: s3-local-test
Authors: Martin
Summary: s3 本地测试环境的搭建


s3 ninja
--------

<http://s3ninja.net/> s3 ninja 在本地模拟S3 API, 而且自带一个管理界面, 但是需要修改代码或者增加配置,把endpoint\_url指定为 <http://localhost:9444/s3>

如果我们不想修改代码,可以通过一些简单的配置把请求导向本地 s3 ninja

s3 virtual hosted-style and path-style access
---------------------------------------------

访问s3 bucket上的文件,有两种方式:

    # example bucket名字 johnsmith  文件 homepage.html

    # Path Style
    http://s3.amazonaws.com/johnsmith/homepage.html

    # Virtual Hosted–Style
    http://johnsmith.s3.amazonaws.com/homepage.html

更多信息参考

<http://docs.aws.amazon.com/zh_cn/AmazonS3/latest/dev/UsingBucket.html#access-bucket-intro> <http://docs.aws.amazon.com/zh_cn/AmazonS3/latest/dev/VirtualHosting.html>

如何配置
--------

我们要达到的目的如下,把原本对亚马逊的HTTP请求指向本地的S3 ninja

mybucket.s3.amazonaws.com -&gt; localhost:9444:s3/mybucket

### /etc/hosts

添加一行:

    127.0.0.1 mybucket.s3.amazonaws.com

这样可以把亚马逊的域名指向本地，但是端口和访问路径Path的修改需要nginx来实现

### nginx

nginx 把127.0.0.1:80 的请求转向 127.0.0.1:9444

配置文件如下:

    server {
    listen       80;
    server_name  localhost;
    location / {
        proxy_pass http://127.0.0.1:9444;
        rewrite ^(.*)$ /s3/mybucket$1 break; #例如 /homepage.html => /s3/mybucket/homepage.html
    }

配置多个bucket
--------------

上面的配置只说了一个bucket的情况，如果有多个bucket需要测试，我们使用nginx virtualhost的功能就可以做到，把server\_name 改成 bucket的域名就行

推荐工具
--------

在 Mac 上 gas mask 可以很方便的切换和编辑hosts文件 <http://clockwise.ee/>

在 Mac 上 安装 nginx，可以使用brew install nginx <http://brew.sh/> 启动命令 sudo nginx， sudo nginx -s reload