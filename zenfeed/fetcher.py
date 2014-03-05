#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
from BeautifulSoup import BeautifulSoup
import requests
import feedparser

DEFAULT_RSS_ICON = "http://www.php-geek.fr/wp-content/themes/www.php-geek.fr/images/rss_icon.png"

class FaviconException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


# Utils :

def sanitize_url(url):
    if not (url.startswith('http://') or url.startswith('https://')):
        url = 'http://%s' % url
    return url.lower()

def parse_url(url):
    url = sanitize_url(url)
    # delete eventual query string and anchor:
    url_begin = url.partition('#')[0].partition('?')[0]
    url_host = '/'.join(url_begin.split('/')[:3])
    return url_begin, url_host

def concat_urls(url, path):
    url_begin, url_host = parse_url(url)
    if path.startswith('/'):
        return url_host + path
    else:
        if not url_begin.endswith('/'):
            url_begin = url_begin + '/'
        return url_begin + path

def fetch_url(url):
    url = sanitize_url(url)
    resp = requests.get(url)
    return resp


# Feed stuff :

def fetch_and_parse_feed(url, etag=None, last_modified=None):
    # TODO implement etag & last_modified header
    resp = fetch_url(url)
    if resp.status_code != 200:
        return None
    return feedparser.parse(resp.content)


# Favicon stuff :

def fetch_icon_in_page(resp):
    if resp.status_code != 200:
        raise FaviconException("Http code != 200 for url: " + resp.url)
    soup = BeautifulSoup(resp.content)
    icon_tags = [tag for tag in soup.findAll("link")
                 if tag.has_key("rel")
                 and "icon" in tag.attrMap["rel"]
                 and tag.has_key("href")]
    if not icon_tags:
        raise FaviconException("No icon tags found in: " + resp.url)
    icon = icon_tags[0]
    icon_href = icon.attrMap["href"]
    
    if icon_href.startswith("http"):
        icon_url = icon_href
    else:
        icon_url = concat_urls(resp.url, icon_href)
    return icon_url

def fetch_icon_url(url):
    resp = fetch_url(url)
    return fetch_icon_in_page(resp)

def fetch_root_icon_url(url):
    _, root_url = parse_url(url)
    return fetch_icon_url(root_url)

def default_favicon_url(url):
    return concat_urls(url, '/favicon.ico')

def fetch_favicon(url, page=None):
    try:
        # search icon url in page:
        if page is None:
            icon_url = fetch_icon_url(url)
        else:
            icon_url = fetch_icon_in_page(page)
    except FaviconException:
        try:
            # search icon url in root page ('/'):
            icon_url = fetch_root_icon_url(url)
        except FaviconException:
            # fallback to /favicon.ico:
            icon_url = default_favicon_url(url)
    resp = fetch_url(icon_url)
    if resp.status_code != 200:
        resp = fetch_url(DEFAULT_RSS_ICON)
    return resp.content
