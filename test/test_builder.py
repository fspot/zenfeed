#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import print_function, unicode_literals
import unittest

import feedparser
from path import path
from zenfeed.builder import normalize_feed_dict, normalize_entry_dict

from sys import version_info as python_version
if python_version[0] == 3:
    basestring = (bytes, str)


class TestBuilding(unittest.TestCase):

    def setUp(self):
        files = path("test/fixtures/feeds").listdir()
        self.feeds = [feedparser.parse(filename) for filename in files]

    def test_feeds_have_string_url(self):
        for feed in self.feeds:
            dico = normalize_feed_dict(feed)
            url_begin = dico['url'][:4]
            self.assertEqual(url_begin, 'http')

    def test_entries_have_string_url(self):
        for feed in self.feeds:
            entries = feed['entries']
            for e in entries:
                dico = normalize_entry_dict(e)
                self.assertIsInstance(dico['content'], basestring, msg=dico['url'])
                url_begin = dico['url'][:4]
                self.assertEqual(url_begin, 'http')


if __name__ == '__main__':
    unittest.main()

