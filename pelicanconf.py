#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os
BASE_DIR = os.path.dirname(__file__)
ENV_DIR = os.path.dirname(BASE_DIR)

AUTHOR = 'Martin'
#SITEURL = 'https://xingzuoshe.cn'
SITENAME = "Martin's Blog"
SITETITLE = "Martin's Blog"
SITESUBTITLE = "Martin's Blog"
SITEDESCRIPTION = 'Martin\'s Thoughts and Writings'
SITELOGO = '/images/default_profile_200x200.png'
FAVICON = '/images/default_profile_200x200.png'
BROWSER_COLOR = '#333333'
PYGMENTS_STYLE = 'default'

ROBOTS = 'index, follow'

PATH = 'content'

DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M'

TIMEZONE = 'Asia/Shanghai'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
         ('astrobook', 'https://astrobook.cn/'),
         ('astrohub', 'https://astrohub.cn'),)

# Social widget
SOCIAL = (('github', 'https://github.com/openmartin'),
          ('rss', '/blog/feeds/all.atom.xml'),)


# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# Theme
THEME = os.path.join(ENV_DIR, "pelican-themes", "Flex")

PLUGIN_PATHS = [os.path.join(ENV_DIR, "pelican-plugins")]
PLUGINS = ['sitemap', 'i18n_subsites', 'liquid_tags.img']

JINJA_ENVIRONMENT = {
    'extensions': ['jinja2.ext.i18n'],
}

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
DISPLAY_PAGES_ON_MENU = False
MAIN_MENU = True
HOME_HIDE_TAGS = True
USE_FOLDER_AS_CATEGORY = False
MENUITEMS = (('Archives', '/archives.html'),
             ('Categories', '/categories.html'),
             ('Tags', '/tags.html'),)


COPYRIGHT_YEAR = '2019'

# STATIC
STATIC_PATHS = ['images', 'extra']
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'},}
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
