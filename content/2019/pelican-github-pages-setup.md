Title: 使用 Pelican 和 Github Pages 建立博客网站
Date: 2019-06-09 22:20
Modified: 2019-06-09 22:30
Category: Python
Tags: python, pelican, github
Slug: pelican-github-pages-setup
Authors: Martin
Summary: Pelican 是一个 Python 语言开发的静态网站生成工具，用 markdown 写完博客之后，发布到Github Pages，免费而且好用，不过配置过程有些复杂，下面记录一下配置的过程。


## 安装 pelican

在 Python 3.5 以上，官方已经集成了虚拟环境功能，不需要再使用 `virtualenv`

```
python3 -m venv pelican_env
cd pelican_env
source bin/active
pip install pelican markdown ghp-import
```

## 新建 pelican 项目

- 先在 github 上新建一个 repo `yourname.github.io`, 然后 clone 到本地，
- 在项目文件夹中运行 `pelican-quickstart`

在选择的过程中注意选择 default language, time zone, Using Github Pages

```
Welcome to pelican-quickstart v4.0.1.

This script will help you create a new Pelican-based website.

Please answer the following questions so this script can generate the files
needed by Pelican.


> Where do you want to create your new web site? [.]
> What will be the title of this web site? Martin's Blog
> Who will be the author of this web site? Martin
> What will be the default language of this web site? [zh] zh
> Do you want to specify a URL prefix? e.g., https://example.com   (Y/n) n
> Do you want to enable article pagination? (Y/n) Y
> How many articles per page do you want? [10] 10
> What is your time zone? [Europe/Paris] Asia/Shanghai
> Do you want to generate a tasks.py/Makefile to automate generation and publishing? (Y/n) Y
> Do you want to upload your website using FTP? (y/N) N
> Do you want to upload your website using SSH? (y/N) N
> Do you want to upload your website using Dropbox? (y/N) N
> Do you want to upload your website using S3? (y/N) N
> Do you want to upload your website using Rackspace Cloud Files? (y/N) N
> Do you want to upload your website using GitHub Pages? (y/N) y
> Is this your personal page (username.github.io)? (y/N) y
Done. Your new project is available at /home/demo/pelican_env/yourname.github.io
```

## pelican config

quick-start 生成的只是最简单的配置，如果想要更好看一点需要更多的自定义配置

下面有一份配置的示例，使用 Flex 主题，sitemap 插件，配置了 disqus 和 Google Adsense

{% include_code ../code/pelicanconf.py lang:python %}

## 新建一篇 markdown

在 `content` 文件夹下可以放 markdown 文件和一些图片，或者自定义的 css,js 文件

和普通的 markdown 不同的是在文件头上需要写一些 metadata，参考[官方文档](https://docs.getpelican.com/en/stable/content.html#file-metadata)

```markdown
Title: My super title
Date: 2010-12-03 10:20
Modified: 2010-12-05 19:30
Category: Python
Tags: pelican, publishing
Slug: my-super-post
Authors: Alexis Metaireau, Conan Doyle
Summary: Short version for index and feeds
```

## Github Pages 提交

- .gitignore 添加 output 文件夹 参考 [官方博客](https://github.com/getpelican/pelican-blog/blob/master/.gitignore)
- 新建`source`分支，把原始的 markdown 文件和 配置文件都放到`source` 分支上

```
git checkout -b source
git add .
git commit -a -m "Initial commit"
git push -u origin source
```
- 把生成的 html 放到 master 分支上，然后 push 到 Github 上

```
ghp-import output -r origin -b master
git push origin master
```

- 这个时候就可以通过 `yourname.github.io` 来访问你的博客了

## Github Pages CNAME 设置

参考 [Github Help](https://help.github.com/en/articles/about-supported-custom-domains)

这里是设置 

- 在 dns 服务商 设置域名 @泛解析 A 记录到 Github 的地址
- 然后在 Github Pages 的设置里添加域名


## daily workflow

- 编辑 markdown
- make html
- make github



## Editor

推荐使用 vscode 来编辑 markdown
