#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Martin'
#SITEURL = 'https://xingzuoshe.cn'
SITENAME = "Martin's Blog"
SITETITLE = "Martin's Blog"
SITESUBTITLE = "Martin's Blog"
SITEDESCRIPTION = 'Martin\'s Thoughts and Writings'
#SITELOGO = SITEURL + '/images/profile.png'
#FAVICON = SITEURL + '/images/favicon.ico'
BROWSER_COLOR = '#333333'
PYGMENTS_STYLE = 'default'

ROBOTS = 'index, follow'

PATH = 'content'
OUTPUT_PATH = 'blog/'

DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M'

TIMEZONE = 'Asia/Shanghai'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('about', '/blog/about.html'),
         ('astrobook', 'https://astrobook.cn/'),
         ('astrohub', 'https://astrohub.cn'),)

# Social widget
SOCIAL = (('github', 'https://github.com/openmartin'),
          ('rss', '/blog/feeds/all.atom.xml'),)


# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# Theme
THEME = "/Users/peng/pelican_env/pelican-themes/Flex"

PLUGIN_PATHS = ["/Users/peng/pelican_env/pelican-plugins"]
PLUGINS = ['sitemap']

# Sitemap
SITEMAP = {
    'format': 'xml',
    'changefreqs': {
        'articles': 'daily',
        'pages': 'daily',
        'indexes': 'daily',
    }
}


# Default theme language
I18N_TEMPLATE_LANG = 'zh'

DEFAULT_LANG = 'zh'
OG_LOCALE = 'zh_CN'
LOCALE = 'zh_CN'




# MENU 
DEFAULT_PAGINATION = 10
MAIN_MENU = True
HOME_HIDE_TAGS = True
USE_FOLDER_AS_CATEGORY = False
MENUITEMS = (('Archives', '/archives.html'),
             ('Categories', '/categories.html'),
             ('Tags', '/tags.html'),)


COPYRIGHT_YEAR = '2019'

# STATIC
STATIC_PATHS = ['images', 'extra']
CUSTOM_CSS = 'static/custom.css'

USE_LESS = True



# Third page service
DISQUS_SITENAME = "astro-2"
#GOOGLE_ANALYTICS = 'UA-1234-5678'
GOOGLE_ADSENSE = {
    'ca_id': 'ca-pub-8640171181637141',
    'page_level_ads': True,
    'ads': {
        'aside': '5604848266',
        'main_menu': '',
        'index_top': '',
        'index_bottom': '2770021113',
        'article_top': '',
        'article_bottom': '4393383534',
    }
}
