#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
import gevent
import feedparser

from builder import FeedFromDict
from models import db

def new_feed_worker(url, answer_box):
    feed_dict = feedparser.parse(url)
    feed = FeedFromDict(feed_dict)
    feed.url = url # set the real feed url
    db.session.add(feed)
    db.session.commit()
    answer_box.put(feed)
