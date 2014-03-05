#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
import gevent
from gevent.queue import Empty

from builder import FeedFromDict
from fetcher import fetch_and_parse_feed
from models import db, Feed, Entry

def new_feed_worker(url, answer_box):
    try:
        feed_dict = fetch_and_parse_feed(url)
    except:
        return answer_box.put(Exception("Error with feed: " + url))
    feed = FeedFromDict(feed_dict)
    feed.url = url # set the real feed url
    db.session.add(feed)
    db.session.commit()
    answer_box.put(feed)

def deadline_worker(feed, inbox):
    while True:
        try:
            msg = inbox.get(timeout=feed.refresh_interval)
        except Empty:
            msg = None
        if msg is not None:
            # TODO check msg type (Mail?) et tout
            #db.session.refresh(obj1)
            print("¿?¿?¿ Refresh forced.")
        feed_dict = fetch_and_parse_feed(feed.url)
        print("¿?¿?¿ Deadline. Feed title:", feed_dict['feed']['title'])
