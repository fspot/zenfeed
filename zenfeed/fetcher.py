#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
from hashlib import sha256
from path import path
from bs4 import BeautifulSoup
import requests
import feedparser

class FaviconException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class FetchingException(Exception):
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
    resp = requests.get(url, verify=False)
    return resp


# Feed stuff :

def fetch_and_parse_feed(url, etag=None, last_modified=None):
    # TODO implement etag & last_modified header
    resp = fetch_url(url)
    if resp.status_code != 200:
        raise FetchingException("status_code != 200")
    feed_parsed = feedparser.parse(resp.content)
    if feed_parsed.version == '':
        # it's probably html instead of rss/atom
        soup = BeautifulSoup(resp.content)
        first_candidate = soup.find_all("link", rel="alternate")[0]['href']
        if not first_candidate.startswith("http"):
            first_candidate = concat_urls(resp.url, first_candidate)
        resp = fetch_url(first_candidate)
        if resp.status_code != 200:
            raise FetchingException("status_code != 200")
        feed_parsed = feedparser.parse(resp.content)
    return {"feed": feed_parsed, "real_url": resp.url}


# Favicon stuff :

def fetch_icon_in_page(resp):
    if resp.status_code != 200:
        raise FaviconException("Http code != 200 for url: " + resp.url)
    soup = BeautifulSoup(resp.content)
    icon_tags = [tag for tag in soup.find_all("link")
                 if tag.has_attr("rel")
                 and "icon" in tag.attrs["rel"]
                 and tag.has_attr("href")]
    if not icon_tags:
        raise FaviconException("No icon tags found in: " + resp.url)
    icon = icon_tags[0]
    icon_href = icon.attrs["href"]

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
    return resp

def mocked_default_favicon():
    class Obj: pass
    obj = Obj()
    obj.url = 'default'
    obj.content = (path(__file__).dirname().relpath() / 'static' / 'img' / 'feedicon.png').bytes()
    return obj

def save_favicon(resp, directory):
    if resp.status_code != 200 or len(resp.content) < 10:
        resp = mocked_default_favicon()
    name = sha256(resp.url).hexdigest()
    save_image(resp.content, path(directory) / name)
    return name

def save_image(content, name):
    with open(name, 'wb') as f:
        f.write(content)
