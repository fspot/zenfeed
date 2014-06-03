#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
import gevent
from gevent.queue import Queue, Empty
from requests.exceptions import ConnectionError

from actor import Mail
from builder import FeedFromDict, EntryFromDict
from fetcher import (fetch_and_parse_feed, sanitize_url,
                     save_favicon, fetch_favicon, FetchingException)
from log import logger
from app import app
from flask import url_for
from models import db, Feed, Entry, Config, update_feed, create_or_update_entry


def new_feed_worker(url, favicon_dir, answer_box, manager_box):
    logger.info("Fetching feed... [%s]", url)
    try:
        fetched = fetch_and_parse_feed(url)
        feed_dict, real_url = fetched['feed'], fetched['real_url']
    except FetchingException:
        return answer_box.put(Exception("Error with feed: " + url))

    feed = FeedFromDict(feed_dict, Config.get())
    feed.url = sanitize_url(real_url) # set the real feed url
    logger.info("Fetching favicon... [%s]", feed.url)
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
    manager_box.put({'type': 'refresh-cache', 'feed_id': feed.id})


def fetching_work(feed, manager_box):
    fetched = fetch_and_parse_feed(feed.url)
    feed_dict, real_url = fetched['feed'], fetched['real_url']
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
        manager_box.put({'type': 'refresh-cache', 'feed_id': feed.id})


def deadline_worker(feed, inbox, manager_box):
    while True:
        try:
            msg = inbox.get(timeout=feed.refresh_interval)
        except Empty:
            msg = None # timeout -> refresh !
        feed = Feed.query.get(feed.id)  # refresh
        if msg is not None:
            # msg types :
            # - stop
            # - refresh
            if isinstance(msg, Mail):
                if msg.body['type'] == 'stop':
                    return msg.answer_box.put('okay')
            logger.warning("©©© Refresh forced.")
        try:
            fetching_work(feed, manager_box)
        except FetchingException as e:
            logger.error("Error re-fetching feed %s : %s", feed.url, e.value)
            continue
        except ConnectionError:
            logger.error("Connection error re-fetching feed %s", feed.url)
            continue


def cache_worker(feed_id):
    with app.test_request_context('/'):
        if feed_id is not None:
            app.cache.delete(feed_id=feed_id)
            app.view_functions['feed_view'](feed_id=feed_id, bot_flag=True)
        app.cache.delete('/')
        app.view_functions['index']()


def delete_worker(worker, feed_id, answer_box, kill_timeout=30):
    if worker is not None:
        logger.warning("Going to stop gracefully feed %d", feed_id)
        inbox = Queue()
        mail = Mail(inbox, {'type': 'stop'})
        worker['queue'].put(mail)
        resp = inbox.get(timeout=kill_timeout)
        if resp is None:
            logger.warning("Going to KILL feed %d !", feed_id)
            worker['worker'].kill()
    feed = Feed.query.get(feed_id)
    if feed is None:
        logger.error("Why doesn't feed [%d] exist ?!", feed_id)
        return answer_box.put({'success': False})
    db.session.delete(feed)
    db.session.commit()
    logger.warning("Okay, feed %d has been deleted !", feed_id)
    answer_box.put({'success': True})
