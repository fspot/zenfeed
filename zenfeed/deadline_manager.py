#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
import gevent
from gevent.queue import Queue

from actor import Actor
from workers import new_feed_worker, deadline_worker

class DeadlineManager(Actor):
    def __init__(self):
        self.workers = {}
        Actor.__init__(self)

    def launch_deadline_workers(self, feeds):
        for feed in feeds:
            inbox = Queue()
            w = gevent.spawn(deadline_worker, feed, inbox)
            self.workers[feed.id] = {
                'feed': feed,
                'worker': w,
                'queue': inbox,
            }

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
        elif msg_type == "force-refresh-feed":
            print("++> force-refresh-feed request:", message['id'])
            self.workers[message['id']]['queue'].put({
                'type': 'force-refresh',
                'answer_box': answer_box,
            }) # TODO put Mail instead ?

deadlineManager = DeadlineManager()