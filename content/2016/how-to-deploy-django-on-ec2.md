Title: 如何在 aws ec2 上部署 django 应用
Date: 2016-04-19 20:20
Modified: 2016-04-19 20:20
Category: Django
Tags: django, aws
Slug: how-to-deploy-django-on-ec2
Authors: Martin
Summary: 如何在 aws ec2 上部署 django 应用


很多时候我们会在环境配置上花大量的时间，这里我记录了一下我配置的过程，希望能节省大家一些的时间。

我的环境是amazon ec2，选择的操作系统是Amazon Linux AMI 2015.03 (HVM) ，选择的最常见的部署方案 nginx + gunicorn + django + mysql

mysql
-----

首先安装mysql-sever:

    $sudo yum install mysql-server mysql mysql-devel
    $sudo chown mysql.mysql -R /var/lib/mysql

修改配置文件/etc/my.cnf:

    [mysqld]
    datadir=/var/lib/mysql # 数据文件存放的位置,修改成适合的位置

    character-set-server=utf8 # 设置默认编码

    [client]
    default-character-set=utf8 # 设置默认编码

启动mysql:

    $sudo service mysqld start

设置root密码，执行/usr/bin/mysql\_secure\_installation

如果需要通过客户端工具管理MySQL，需要添加远程连接MySQL权限:

    $mysql -u root -p

    mysql>GRANT ALL PRIVILEGES ON *.* TO root@"%" IDENTIFIED BY '<password>' WITH GRANT OPTION;
    mysql>FLUSH PRIVILEGES;

一般不建议root用户连接MySQL，所以需要添加一个普通用户:

    create user 'blog'@'localhost' identified by '<password>';
    flush privileges;
    grant all privileges on blog.* to blog@localhost identified  by '<password>';

配置python环境
--------------

我目前的python版本是2.7.9，所以不需要安装pip

### pip

如果Python版本是2.7.9或者是3.4 以上，pip默认包含于Python的安装包中

怎么安装pip，参考这里 <https://pip.pypa.io/en/latest/installing.html>

### virtualenv

virtualenv 用于创建独立的Python环境，可以不受全局的site-packages当中安装的包的影响。:

    pip install virtualenv
    # 创建虚拟环境
    virtualenv ENV
    cd ENV
    source ./bin/activate

磨刀不误砍柴工，接下来开始大展身手啦。

### 安装必须的python库

如果项目中有requirements.txt文件，可直接执行，自动安装所有依赖关系，没有的话如果有可以从开发环境导出一份:

    $pip freeze >> requirements.txt # 在开发环境中执行
    $pip install -r requirements.txt

我们在这里列出一些经常需要的依赖包:

    $pip install gunicorn # gunicorn
    $pip install gevent   # 让gunicorn使用gevent worker，提高并发性能
    $pip install django
    $pip install MySQL-python # 如果要连接mysql数据库，需要安装
    $pip install Pillow   # 代替Python Image Library

如果使用gunicron部署django应用，需要小小修改settings.py一下，就是在INSTALLED\_APPS最后添加上gunicorn。

gunicron 启动脚本:

    nohup gunicorn --worker-class=gevent myblog.wsgi:application --bind 127.0.0.1:8001 >gunicorn.log 2>&1 &

上面的步骤完成之后，我们的应用就可以启动了，但是我们一般在gunicorn之前使用ngnix做反向代理。有两个好处，一是静态文件交给nginx处理，可以减少响应时间，二是如果一个服务器上部署多个站点，仅仅用gunicorn无法达到目的，这时我们需要用apache或者nginx的虚拟服务器功能。

nginx
-----

不同的Linux发行版上安装的方法，配置文件的位置可能不太一样，我们理解了整个配置的思路之后就可以举一反三了:

    $sudo yum install nginx
    $sudo service start nginx

编辑 /etc/nginx/conf.d/virtual.conf:

    server {
        listen       80;

        server_name  blog.dailyastrology.info;

        access_log /var/log/nginx/blog.dailyastrology.info-access.log;
        error_log /var/log/nginx/blog.dailyastrology.info-error.log;

        location / {
            proxy_pass http://127.0.0.1:8001;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
        location /static {
            root /home/ec2-user/blogenv/myblog;
        }
    }

如果仅仅作为个人的站点，上述的配置应该就够用的，如果是需要高级的功能就需要自己去研究每个软件的配置和运维方法。
