#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
import gevent

from actor import Actor
from workers import new_feed_worker

class DeadlineManager(Actor):
    def __init__(self):
        self.workers = {} # TODO url => workers
        Actor.__init__(self)

    def on_message(self, message, answer_box=None):
        """
            Message type can be :
            - new-feed
            - force-refresh-feed
            - remove-feed
            - edit-refresh-interval-feed
        """

        assert isinstance(message, dict)
        msg_type = message.get('type')
        if msg_type == 'new-feed':
            print("++> new-feed request:", message['url'])
            gevent.spawn(new_feed_worker, message['url'], answer_box)

deadlineManager = DeadlineManager()
