#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
from datetime import datetime
from functools import wraps
from hashlib import sha256
from flask import (render_template, send_from_directory, request,
                   redirect, url_for, session, jsonify)
from gevent.queue import Queue
from flask.ext.babel import format_datetime

from actor import Mail
from app import app, babel, cache
from models import db, Tag, Feed, Entry, Config
from deadline_manager import deadlineManager
from settings import LANGUAGES


def need_root(vue):
    @wraps(vue)
    def decorated(*args, **kwargs):
        if not Config.validate_password(session.get('pw')):
            return redirect(url_for('login', next=request.path))
        return vue(*args, **kwargs)
    return decorated

def refresh_highlighted_feeds(vue):
    @wraps(vue)
    def decorated(*args, **kwargs):
        feed_id = kwargs['feed_id']
        if not kwargs.get('bot_flag'):
            feed = Feed.query.get(feed_id)
            if feed.has_news:
                feed.has_news = False
                db.session.commit()
                deadlineManager.inbox.put(
                    {'type': 'refresh-cache', 'feed_id': None}
                )
        return vue(*args, **kwargs)
    return decorated

# main site routes :

@app.route('/')
@cache.cached(timeout=86400*365, key_prefix='%s')
def index():
    feeds = Feed.query.order_by(Feed.updated.desc())
    return render_template('feeds.html', feeds=feeds)

@app.route(app.static_url_path + '/favicon/<favicon>')
def get_favicon(favicon):
    return send_from_directory(app.config['FAVICON_DIR'], favicon)

@app.route('/<int:feed_id>/')
@refresh_highlighted_feeds
@cache.cached(timeout=86400*365, key_prefix='%s')
def feed_view(feed_id, bot_flag=False):
    feed = Feed.query.get(feed_id)
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

# login / logout :

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

# admin and api :

@app.route('/admin/')
@need_root
def admin_index():
    return render_template('admin.html')

@app.route('/admin/<filename>.html')
@need_root
def admin_view(filename):
    return redirect(app.static_url_path + '/html/' + filename + '.html')

@app.route('/api/config/', methods=['GET', 'POST'])
@need_root
def api_config():
    config = Config.get()
    if request.method == 'POST':
        # update all fields, no checks (TODO)
        config_fields = config.fields_set(exclude_fields=['id', 'password'])
        fields = config_fields & set(request.json.keys())
        for field in fields:
            setattr(config, field, request.json[field])
        # change password if the field isnt empty
        pw = request.json.get('pw')
        if pw:
            Config.change_password(pw)
        db.session.merge(config)
        db.session.commit()
        Config.refresh_instance()  # unnecessary ?
        return jsonify({'msg': 'Success !'})
    return jsonify(config.to_dict(exclude_fields=['password', 'id']))

def clean_feed_to_dict(feed):
    f = feed.to_dict(exclude_fields=['entries', 'tags', 'entries_hash'])
    f['updated'] = int(feed.updated.strftime("%s"))
    f['favicon_url'] = url_for('get_favicon', favicon=feed.favicon_path)
    f['nb_of_entries'] = feed.entries.count()
    return f

@app.route('/api/feed/')
@need_root
def api_feed():
    feeds = Feed.query.order_by(Feed.updated.desc())
    ret = {'feeds': []}
    for feed in feeds:
        f = clean_feed_to_dict(feed)
        ret['feeds'].append(f)
    return jsonify(ret)

@app.route('/api/feed/add/', methods=['POST'])
@need_root
def api_add_feed():
    url = request.json['url']
    inbox = Queue()
    mail = Mail(inbox, {'type': 'new-feed', 'url': url})
    deadlineManager.inbox.put(mail)
    feed = inbox.get()
    dictfeed = clean_feed_to_dict(feed)
    return jsonify({"msg": feed.title, 'feed': dictfeed})

@app.route('/api/feed/delete/', methods=['POST'])
@need_root
def api_delete_feed():
    feed_id = request.json['id']
    inbox = Queue()
    mail = Mail(inbox, {'type': 'delete-feed', 'feed_id': feed_id})
    deadlineManager.inbox.put(mail)
    resp = inbox.get()
    return jsonify({"msg": resp['success']})

# Babel

@babel.localeselector
def get_locale():
    return (app.config['FIXED_LANGUAGE'] or
            request.accept_languages.best_match(LANGUAGES.keys()))

# Jinja

@app.template_filter('humanize_date')
def _jinja2_humanize_datetime(date, locale=None):
    if date is not None:
        fmt = "d/MM, H':'mm"
        if datetime.now().year != date.year:
            fmt = "d/MM/yyyy"
        return format_datetime(date, fmt)
