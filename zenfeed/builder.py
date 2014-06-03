#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function

import datetime

from models import Feed, Entry
from fetcher import concat_urls
from sys import version_info as python_version
if python_version[0] == 3:
    basestring = (bytes, str)

def normalize_feed_dict(dico):
    """
        feedparser.FeedParserDict from different sites may differ
        in their attributes : we have to normalize that.
    """

    norm = {}
    assert isinstance(dico, dict)
    f = dico['feed']
    e = dico['entries']
    f_id = f.get('id')
    if isinstance(f_id, basestring) and f_id[:4] == 'http':
        norm['url'] = f_id
    else:
        norm['url'] = f.get('link')
    norm['title'] = f.get('title') or f.get('id')
    norm['link'] = f.get('link')
    if not norm['link'].startswith('http'):
        norm['link'] = 'http://' + norm['link']
    norm['subtitle'] = f.get('subtitle')
    norm['author'] = f.get('author')
    norm['generator'] = f.get('generator')
    norm['encoding'] = dico.get('encoding')
    structTime = f.get('updated_parsed')
    try:
        norm['updated'] = datetime.datetime(*structTime[:6])
    except (TypeError, ValueError) as err:
        norm['updated'] = None
    norm['entries_hash'] = id(e) # TODO hash
    return norm


def normalize_entry_dict(dico, feed_url):
    """
        feedparser.FeedParserDict from different sites may differ
        in their attributes : we have to normalize that.
    """

    norm = {}
    assert isinstance(dico, dict)
    e_id = dico.get('id')
    if isinstance(e_id, basestring) and e_id[:4] == 'http':
        norm['url'] = e_id
    else:
        norm['url'] = dico.get('link')
    if not norm['url'].startswith('http'):
        norm['url'] = concat_urls(feed_url, norm['url'])
    norm['link'] = dico.get('link')
    if not norm['link'].startswith('http'):
        norm['link'] = concat_urls(feed_url, norm['link'])
    norm['title'] = dico.get('title')
    norm['content'] = dico.get('value')
    if norm['content'] is None:
        try:
            norm['content'] = dico['content'][0]['value']
        except (KeyError, IndexError) as err:
            norm['content'] = dico.get('summary')
    try:
        norm['mimetype'] = dico['content'][0]['type']
    except (KeyError, IndexError) as err:
        norm['mimetype'] = None
    structTime = dico.get('published_parsed')
    try:
        norm['created'] = datetime.datetime(*structTime[:6])
    except (TypeError, ValueError) as err:
        norm['created'] = None
    structTime = dico.get('updated_parsed')
    try:
        norm['updated'] = datetime.datetime(*structTime[:6])
    except (TypeError, ValueError) as err:
        norm['updated'] = None
    if norm['created'] is None and norm['updated'] is not None:
        norm['created'] = norm['updated']
    elif norm['updated'] is None and norm['created'] is not None:
        norm['updated'] = norm['created']
    return norm


def FeedFromDict(dico, config):
    dico = normalize_feed_dict(dico)
    feed = Feed(dico['url'])
    feed.title = dico['title']
    feed.link = dico['link']
    feed.subtitle = dico['subtitle']
    feed.author = dico['author']
    feed.generator = dico['generator']
    feed.encoding = dico['encoding']
    feed.updated = dico['updated']
    feed.entries_hash = dico['entries_hash']
    feed.refresh_interval = config.default_refresh_interval
    feed.max_entries = config.default_max_entries
    feed.highlight_news = config.default_highlight_news
    feed.entries_per_page = config.default_entries_per_page
    feed.has_news = False
    return feed


def EntryFromDict(dico, feed_url):
    dico = normalize_entry_dict(dico, feed_url)
    entry = Entry(dico['title'], dico['content'])
    entry.url = dico['url']
    entry.link = dico['link']
    entry.title = dico['title']
    entry.content = dico['content']
    entry.mimetype = dico['mimetype']
    entry.created = dico['created']
    entry.updated = dico['updated']
    entry.public = False
    return entry
