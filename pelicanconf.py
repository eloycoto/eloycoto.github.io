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

EXTRA_PATH_METADATA = {
    'extra/CNAME': {'path': 'CNAME'},
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/gpg_public_key': {'path': 'gpg_public_key'},
}

STATIC_PATHS = [
    'extra/robots.txt',
    'extra/CNAME',
    'extra/gpg_public_key',
    'img',
]

CONTRIBUTIONS = {
    "Containers": [
        {"name": "cilium", "desc": "Linux-native network security", "url": "https://github.com/cilium/cilium"}],
    "DevOps": [
        {"name": "Hashicorp/Terraform", "desc": "Infraestructure as code", "url": "https://github.com/hashicorp/terraform"},
        {"name": "Hashicorp/Packer", "desc": "Build Automated Machine Images", "url": "https://www.packer.io/"},
        {"name": "Vmware/Govmomi", "desc": "Go Bindings for Vsphere", "url": "https://github.com/vmware/govmomi"},
        ],
    "VoIP": [
        {"name": "Kamailio", "desc": "Core Contributor", "url": "https://www.kamailio.org/w/"},
        {"name": "CGrates", "desc": "Golang Real time billing", "url": "https://github.com/cgrates/cgrates"}],
    "Misc": [
        {"name": "Firefox/servo", "desc": "Web browser Engine", "url": "https://servo.org/"},
        {"name": "Firefox/euclid", "desc": "Rust library for Geometry types", "url": "https://github.com/servo/euclid/"},
        {"name": "Radix", "desc": "Golang Redis client", "url": "https://github.com/mediocregopher/radix.v2"},
        {"name": "Grafana", "desc": "Analytics and monitoring", "url": "https://github.com/grafana/grafana-docker-dev-env/pull/1"}
        ],
}

AUTHORS_BIO = {
  "eloycoto": {
    "name": "Eloy Coto",
    "cover": "img/profile.jpg",
    "image": "img/profile.jpg",
    "website": "http://acalustra.com",
    "github": "eloycoto",
    "twitter": "eloycoto",
    "linkedin": "eloycoto",
    "location": "Galicia",
    "bio": "Senior software engineer with experience in Golang, C and Python and CI/CD"
  }
}

SOCIAL = (('twitter', 'https://twitter.com/eloycoto'),
          ('github', 'https://github.com/eloycoto'),
          ('envelope','mailto:eloycoto@gmail.com'))

HEADER_COVER = 'img/oia.jpg'
