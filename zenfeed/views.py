#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
from flask import render_template
from gevent.queue import Queue

from actor import Mail
from app import app
from models import db, Tag, Feed, Entry
from deadline_manager import deadlineManager


@app.route('/')
def index():
    feeds = Feed.query.order_by(Feed.updated.desc())
    favicon_path_begin = '/static/img/'
    return render_template('feeds.html',
        feeds=feeds, favicon_path_begin=favicon_path_begin)

@app.route('/<int:feed_id>/')
def feed_view(feed_id):
    feed = Feed.query.get(feed_id)
    if feed.has_news:
        feed.has_news = False
        db.session.commit()
    entries = feed.entries.order_by(Entry.updated.desc())
    return render_template('feed.html', feed=feed, entries=entries)

@app.route('/<int:feed_id>/<int:entry_id>/')
def entry_view(feed_id, entry_id):
    entry = Entry.query.get(entry_id)
    return render_template('entry.html', entry=entry)

@app.route('/new-feed/<path:url>')
def add_feed(url):
    inbox = Queue()
    mail = Mail(inbox, {'type': 'new-feed', 'url': url})
    deadlineManager.inbox.put(mail)
    feed = inbox.get()
    raise Exception("Be zen !")
    return "poulpe"
