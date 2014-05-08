#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
import gevent
from gevent.queue import Empty
from requests.exceptions import ConnectionError

from builder import FeedFromDict, EntryFromDict
from fetcher import fetch_and_parse_feed, sanitize_url
from log import logger
from models import db, Feed, Entry, Config, update_feed, create_or_update_entry
from fetcher import save_favicon, fetch_favicon, FetchingException


def new_feed_worker(url, favicon_dir, answer_box, manager_box):
    try:
        fetched = fetch_and_parse_feed(url)
        feed_dict, real_url = fetched['feed'], fetched['real_url']
    except FetchingException:
        return answer_box.put(Exception("Error with feed: " + url))

    feed = FeedFromDict(feed_dict, Config.get())
    feed.url = sanitize_url(real_url) # set the real feed url
    feed.favicon_path = save_favicon(fetch_favicon(feed.url), favicon_dir)
    db.session.add(feed)
    for e in feed_dict['entries'][::-1]:
        entry = EntryFromDict(e, feed.url)
        entry.feed = feed # set the corresponding feed
        db.session.add(entry)
    db.session.commit()

    most_recent_entry = feed.entries.order_by(Entry.updated.desc()).first()
    feed.updated = most_recent_entry.updated
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
            logger.warning("©©© Refresh forced.")
        try:
            fetched = fetch_and_parse_feed(feed.url)
        except FetchingException as e:
            logger.error("Error re-fetching feed %s : %s", feed.url, e.value)
            continue
        except ConnectionError:
            logger.error("Connection error re-fetching feed %s", feed.url)
            continue
        feed_dict, real_url = fetched['feed'], fetched['real_url']
        feed = Feed.query.get(feed.id)  # refresh
        if feed.url != real_url:
            logger.warning("©©© Feed url changed from %s to %s", feed.url, real_url)
            feed.url = sanitize_url(real_url)
        logger.info("©©© Updated feed: %s", feed.url)
        feed_changed = update_feed(feed, FeedFromDict(feed_dict, Config.get()))
        any_entry_created = any([
            create_or_update_entry(feed.id, EntryFromDict(e, feed.url))
            for e in feed_dict['entries']
        ])
        db.session.commit()

        if any_entry_created:
            most_recent_entry = feed.entries.order_by(Entry.updated.desc()).first()
            feed.updated = most_recent_entry.updated
            feed.has_news = feed.has_news or feed.highlight_news
            db.session.merge(feed)
            db.session.commit()
