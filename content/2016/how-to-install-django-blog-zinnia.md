Title: 如何使用 django-zinnia-blog 建立个人博客
Date: 2016-04-19 20:20
Modified: 2016-04-19 20:20
Category: Django
Tags: django, aws, zinnia
Slug: how-to-install-django-blog-zinnia
Authors: Martin
Summary: 使用 django-zinnia-blog 建立个人博客，一步一步


[django-zinnia-blog](http://django-blog-zinnia.com/) 顾名思义就是一套用Django开发的个人博客程序，虽然比大名鼎鼎的wordpress略显简陋，不过在以Python作为开发语言的博客系统中算是很不错的。

pip
---

如果Python版本是2.7.9或者是3.4 以上，pip默认包含于Python的安装包中

怎么安装pip，参考这里 <https://pip.pypa.io/en/latest/installing.html>

virtualenv
----------

virtualenv 用于创建独立的Python环境，可以不受全局的site-packages当中安装的包的影响。:

    pip install virtualenv
    # 创建虚拟环境
    virtualenv ENV
    cd ENV
    source ./bin/activate

磨刀不误砍柴工，接下来开始大展身手啦。

django-zinnia-blog
------------------

直接使用pip安装:

    pip install Pillow
    pip install django-zinnia-blog
    #如果数据库使用MySQL
    pip install python-mysql

然后按照 <http://docs.django-blog-zinnia.com/en/develop/getting-started/install.html> 建立一个django-project

Django1.7的命令和以前有些不一样，记录一下:

    manage.py migrate
    mamage.py createsuperuser

安装theme
---------

使用zinnia不像wordpress那样有丰富多样的主题可以选择，需要我们手动修改一番，我们可以选择zinnia-theme-bootstrap，然后在这个基础上修修改改:

    pip install django-app-namespace-template-loader

    下载zinnia-theme-bootstrap，解压到你的项目文件夹下
    https://github.com/django-blog-zinnia/zinnia-theme-bootstrap

    zinnia_bootstrap\templates\zinnia
    base.html
    skeleton.html

上面是两个最关键的模板，可以按照自己的想法修改

使用reStructuredText写博客
--------------------------

如果你喜欢用reStructuredText写文档的话，zinnia也支持，不过需要我们配置一下。:

    pip install docutils
    pip install zinnia-wysiwyg-markitup

    #settings.py 中需要添加一行
    ZINNIA_MARKUP_LANGUAGE = 'restructuredtext'

settings.py和urls.py
--------------------

在配置文件中有很多坑，我被坑了好长时间才爬出来，希望后来人不要接着被坑了。

settings.py中需要注意的片段:

    # 如果DEBUG=False 这个地方需要配置，否则会有HTTP 400的错误
    ALLOWED_HOSTS = ['*']

    # Email backend
    EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

    INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'django_comments',
    'django.contrib.sitemaps',
    'mptt',
    'tagging',
    'zinnia_bootstrap',
    'zinnia',
    'zinnia_markitup',
    )

    # Template
    # List of callables that know how to import templates from various sources.
    TEMPLATE_LOADERS = (
    'app_namespace.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
    )

    # 语言代码是zh-hans 对应 zh_Hans
    LANGUAGE_CODE = 'zh-hans'

    # zinnia config
    ZINNIA_MARKUP_LANGUAGE = 'restructuredtext'

urls.py可以按照以下来配置:

    from django.conf.urls import patterns, include, url
    from django.contrib import admin
    from django.views.generic.base import RedirectView

    from zinnia.sitemaps import TagSitemap
    from zinnia.sitemaps import EntrySitemap
    from zinnia.sitemaps import CategorySitemap
    from zinnia.sitemaps import AuthorSitemap

    urlpatterns = patterns('',
        # Examples:
        # url(r'^$', 'myblog.views.home', name='home'),
        # url(r'^blog/', include('blog.urls')),
        url(r'^$', RedirectView.as_view(url='/weblog/')),  
        url(r'^admin/', include(admin.site.urls)),
        url(r'^weblog/', include('zinnia.urls', namespace='zinnia')),
        url(r'^comments/', include('django_comments.urls')),
    )



    sitemaps = {'tags': TagSitemap,
                'blog': EntrySitemap,
                'authors': AuthorSitemap,
                'categories': CategorySitemap,}

    urlpatterns += patterns(
        'django.contrib.sitemaps.views',
        url(r'^sitemap.xml$', 'index',
            {'sitemaps': sitemaps}),
        url(r'^sitemap-(?P<section>.+)\.xml$', 'sitemap',
            {'sitemaps': sitemaps}),)
