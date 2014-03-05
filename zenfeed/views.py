#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
from gevent.queue import Queue

from actor import Mail
from app import app
from models import Tag, Feed, Entry
from deadline_manager import deadlineManager

@app.route('/')
def index():
    nb = len(Tag.query.all())
    return 'Yo. Nb of tags : %d' % nb

@app.route('/new-feed/<path:url>')
def add_feed(url):
    inbox = Queue()
    mail = Mail(inbox, {'type': 'new-feed', 'url': url})
    deadlineManager.inbox.put(mail)
    feed = inbox.get()
    raise Exception("Be zen !")
    return "poulpe"
