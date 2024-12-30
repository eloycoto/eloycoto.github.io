#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Eloy Coto'
SITENAME = u'A Calustra'
SITEURL = 'https://acalustra.com'
DEFAULT_DATE_FORMAT = ('%A %d-%m-%Y')
RELATIVE_URLS = False

GOOGLE_ANALYTICS = "UA-36310774-1"
PATH = 'content'

TIMEZONE = 'Europe/Madrid'

DEFAULT_LANG = u'en'
DISQUS_SITENAME = 'acalustra'

COLOR_SCHEME_CSS='monokai.css'
CSS_OVERRIDE = ['theme/css/eloy.css']

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'rss.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS = ()
# Social widget
SOCIAL = ()

DEFAULT_PAGINATION = 10

PLUGIN_PATHS = ["pelican-plugins/"]
PLUGINS = ['sitemap','related_posts']
THEME = 'theme/simple/'
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}
RELATED_POSTS_MAX = 5
READERS = {'html': None}
STATIC_PATHS = [
    'extra/robots.txt',
    'extra/CNAME',
    'extra/gpg_public_key',
    'img',
    'extra/tools',
]

EXTRA_PATH_METADATA = {
    'extra/CNAME': {'path': 'CNAME'},
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/gpg_public_key': {'path': 'gpg_public_key'},
}

SOCIAL = (('twitter', 'https://twitter.com/eloycoto'),
          ('github', 'https://github.com/eloycoto'),
          ('envelope','mailto:eloycoto@gmail.com'))

HEADER_COVER = 'img/oia.jpg'
