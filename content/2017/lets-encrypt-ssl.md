Title: 在 Amazon Linux 使用 Let's encrypt 免费的SSL
Date: 2017-04-03 20:20
Modified: 2017-04-03 20:20
Category: Linux
Tags: aws, linux, ssl
Slug: lets-encrypt-ssl
Authors: Martin
Summary: 在 Amazon Linux 使用 Let's encrypt 免费的SSL

如果你使用ELB来做负载均衡，在AWS上可以很方便的使用SSL。如果不使用ELB就需要自己来配置SSL。
Let's encrypt 提供期限为三个月的免费SSL证书，到期之后需要renew，官方还提供自动renew的工具certbot

## certbot
certbot 是一个自动申请和续期SSL证书的工具。在[官网certbot.eff.org](https://certbot.eff.org/)可以找到各种OS和Web服务器下的安装方法。常见的Ubuntu和CentOS安装起来十分方便。

## Amazon Linux
在AWS EC2上，官方推荐的是OS是Amazon Linux，基于RHEL 6源码重新编译的，提供了Amazon自己的工具和源。certbot的安装方式类似于RHEL 6/CentOS 6

## 申请SSL证书步骤
- ssh到Server
- 下载certbot
```
wget https://dl.eff.org/certbot-auto
chmod a+x certbot-auto
```
- 执行certbot
```
sudo ./certbot-auto --debug -v --server https://acme-v01.api.letsencrypt.org/directory certonly -d YOUR_WEBSITE_HERE
```
- 验证
```
How would you like to authenticate with the ACME CA?
---------------------------
1: Place files in webroot directory (webroot)
2: Spin up a temporary webserver (standalone)
---------------------------
```
选择1certbot会把一个验证文件放到webroot下，所以需要配置一下nginx的默认静态目录
选择2certbot会启动一个web服务，占用443端口，所以需要暂停一下nginx，一般情况下选择2比较省事。

`记得在AWS EC2的安全组中放开443端口`

- 证书路径
```
Certificate: /etc/letsencrypt/live/YOUR_WEBSITE_HERE/cert.pem
Full Chain: /etc/letsencrypt/live/YOUR_WEBSITE_HERE/fullchain.pem
Private Key: /etc/letsencrypt/live/YOUR_WEBSITE_HERE/privkey.pem
```

## nginx 启用SSL
启用SSL之后，http需要默认跳转到https，还有SSL证书的配置，下面是个配置的例子
```
server {
    listen       80;

    server_name  YOUR_WEBSITE_HERE;
    
	# Redirect all HTTP requests to HTTPS with a 301 Moved Permanently response.
    return 301 https://YOUR_WEBSITE_HERE$request_uri;

}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;

	server_name YOUR_WEBSITE_HERE;
    
    # certs sent to the client in SERVER HELLO are concatenated in ssl_certificate
    ssl_certificate /etc/letsencrypt/live/YOUR_WEBSITE_HERE/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/YOUR_WEBSITE_HERE/privkey.pem;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_session_tickets off;
    access_log /var/log/nginx/YOUR_WEBSITE_HERE-access.log;
    error_log /var/log/nginx/YOUR_WEBSITE_HERE-error.log;
    location / {
        proxy_pass http://127.0.0.1:8003;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## 自动更新证书
- 使用root用户
```
sudo -i
```
- 增加定时任务
```
crontab -e
```
增加一行，每个月1号2点30分更新
```
30 2 1 * * /path/to/certbot renew --pre-hook "service nginx stop" --post-hook "service nginx start"
```
- dry run
```
./path/to/certbot-auto renew --dry-run
```

## chrome 变绿
在chrome下需要全站都使用https地址栏才会变绿，需要检查一下网站里面的各种URL，比如外链图片或JS文件，都需要使用https才行。



参考资料:
- http://frontenddev.org/article/using-certbot-deployment-let-s-encrypt-free-ssl-certificate-implementation-https.html
- https://segmentfault.com/a/1190000005797776
- https://nouveauframework.org/blog/installing-letsencrypts-free-ssl-amazon-linux/
- https://ksmx.me/letsencrypt-ssl-https/
- https://diamondfsd.com/article/e221b455-b0e7-40b7-a6c7-9bb7e3e35657

