#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
from functools import wraps
from hashlib import sha256
from flask import (render_template, send_from_directory, request,
                   redirect, url_for, session)
from gevent.queue import Queue
import arrow

from actor import Mail
from app import app
from models import db, Tag, Feed, Entry, Config
from deadline_manager import deadlineManager


def need_root(vue):
    @wraps(vue)
    def decorated(*args, **kwargs):
        if not Config.validate_password(session.get('pw')):
            return redirect(url_for('login', next=request.path))
        return vue(*args, **kwargs)
    return decorated


@app.route('/')
def index():
    feeds = Feed.query.order_by(Feed.updated.desc())
    return render_template('feeds.html', feeds=feeds)

@app.route(app.static_url_path + '/favicon/<favicon>')
def get_favicon(favicon):
    return send_from_directory(app.config['FAVICON_DIR'], favicon)

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

@app.route('/login/', methods=['GET', 'POST'])
def login():
    next_page = request.args.get('next') or url_for('index')
    if request.method == 'POST':
        session['pw'] = Config.hash(request.form['pw'])
        return redirect(next_page)
    return render_template('login.html', next_page=next_page)

@app.route('/logout/')
def logout():
    next_page = request.args.get('next') or url_for('index')
    session.pop('pw', None)
    return redirect(next_page)

@app.route('/admin/')
@need_root
def admin_index():
    return render_template('admin.html')

# Jinja :
@app.template_filter('humanize_date')
def _jinja2_humanize_datetime(date, locale):
    if date is not None:
        return arrow.Arrow.fromdatetime(date).humanize(locale=locale)
