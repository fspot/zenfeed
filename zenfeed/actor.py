#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
import gevent
from gevent.queue import Queue

class Mail:
    def __init__(self, answer_box, message):
        self.answer_box = answer_box
        self.body = message

class Actor(gevent.Greenlet):
    def __init__(self):
        self.inbox = Queue()
        gevent.Greenlet.__init__(self)

    def on_message(self, message, answer_box=None):
        """ Define in your subclass. """
        raise NotImplemented()

    def send_to(self, dest, message):
        mail = Mail(self.inbox, message)
        if isinstance(dest, Actor):
            dest = dest.inbox
        dest.put(mail)

    def _run(self):
        self.running = True
        while self.running:
            message = self.inbox.get()
            if isinstance(message, Mail):
                self.on_message(message.body, answer_box=message.answer_box)
            else:
                self.on_message(message)
