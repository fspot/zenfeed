#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
from gevent.queue import Queue

from actor import Mail
from app import app
from models import Tag, Feed, Entry
from deadline_manager import deadlineManager

@app.route('/test')
def test():
    nb = len(Tag.query.all())
    return 'Yo. Nb of tags : %d' % nb

@app.route('/')
def index():
    feeds = Feed.query.order_by(Feed.updated.desc())
    s = '<br>'.join(feed.title for feed in feeds)
    return s

@app.route('/<int:feed_id>/')
def feed_view(feed_id):
    feed = Feed.query.get(feed_id)
    entries = feed.entries.order_by(Entry.updated.desc())
    s = '<br>'.join(e.title for e in entries)
    return feed.url + '<br>' + s

@app.route('/<int:feed_id>/<int:entry_id>/')
def entry_view(feed_id, entry_id):
    entry = Entry.query.get(entry_id)
    return entry.url

@app.route('/new-feed/<path:url>')
def add_feed(url):
    inbox = Queue()
    mail = Mail(inbox, {'type': 'new-feed', 'url': url})
    deadlineManager.inbox.put(mail)
    feed = inbox.get()
    raise Exception("Be zen !")
    return "poulpe"
