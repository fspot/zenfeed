#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
import gevent
from gevent.queue import Empty

from builder import FeedFromDict, EntryFromDict
from fetcher import fetch_and_parse_feed, sanitize_url
from models import db, Feed, Entry, update_feed, create_or_update_entry

def new_feed_worker(url, answer_box, manager_box):
    try:
        feed_dict = fetch_and_parse_feed(url)
    except:
        return answer_box.put(Exception("Error with feed: " + url))
    feed = FeedFromDict(feed_dict)
    feed.url = sanitize_url(url) # set the real feed url
    db.session.add(feed)
    for e in feed_dict['entries'][::-1]:
        entry = EntryFromDict(e)
        entry.feed = feed # set the corresponding feed
        db.session.add(entry)
    db.session.commit()
    answer_box.put(feed)
    manager_box.put({'type': 'new-deadline-worker', 'feed_id': feed.id})

def deadline_worker(feed, inbox):
    while True:
        try:
            msg = inbox.get(timeout=feed.refresh_interval)
        except Empty:
            msg = None # timeout -> refresh !
        if msg is not None:
            # TODO check msg type (Mail?) et tout
            #db.session.refresh(obj1) ?
            print("©©© Refresh forced.")
        try:
            feed_dict = fetch_and_parse_feed(feed.url)
        except:
            raise Exception("Error re-fetching: " + feed.url)
        print("©©© Updated feed:", feed.url)
        feed_changed = update_feed(feed, FeedFromDict(feed_dict))
        any_entry_changed = any(
            create_or_update_entry(feed, EntryFromDict(e))
            for e in feed_dict['entries']
        )
        db.session.commit()
        if any_entry_changed and not feed_changed:
            most_recent_entry = Entry.query.order_by(Entry.updated.desc()).first()
            feed.updated = most_recent_entry.updated
        if any_entry_changed or feed_changed:
            feed.has_news = True
        db.session.commit()
