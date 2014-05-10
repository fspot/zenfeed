#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import print_function, unicode_literals
import unittest

import feedparser
from path import path

from sys import version_info as python_version
if python_version[0] == 3:
    basestring = (bytes, str)

class TestFeedParsing(unittest.TestCase):

    def setUp(self):
        self.files = path("test/fixtures/feeds").listdir()

    def test_feeds_parsing_succeed(self):
        self.assertTrue(len(self.files) > 0)
        for filename in self.files:
            feed = feedparser.parse(filename)
            self.assertIsInstance(feed, feedparser.FeedParserDict, msg=filename)


class TestFeedFields(unittest.TestCase):

    def setUp(self):
        files = path("test/fixtures/feeds").listdir()
        self.feeds = [feedparser.parse(filename) for filename in files]

    def test_feeds_have_string_title(self):
        for feed in self.feeds:
            self.assertIsInstance(feed['feed']['title'], basestring)


if __name__ == '__main__':
    unittest.main()

