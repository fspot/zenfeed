#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import print_function, unicode_literals
import unittest

from zenfeed.fetcher import (
    sanitize_url, parse_url, concat_urls, default_favicon_url
)

class TestParseUrl(unittest.TestCase):

    def test_parse_url_simple(self):
        # Arrange
        url = 'http://hveem.no'
        expected_url_begin = 'http://hveem.no'
        expected_url_host = 'http://hveem.no'
        # Act
        url_begin, url_host = parse_url(url)
        # Assert
        self.assertEqual(url_begin, expected_url_begin)
        self.assertEqual(url_host, expected_url_host)

    def test_parse_url_simple_with_trailing_slash(self):
        # Arrange
        url = 'http://hveem.no/'
        expected_url_begin = 'http://hveem.no/'
        expected_url_host = 'http://hveem.no'
        # Act
        url_begin, url_host = parse_url(url)
        # Assert
        self.assertEqual(url_begin, expected_url_begin)
        self.assertEqual(url_host, expected_url_host)

    def test_parse_url(self):
        # Arrange
        url = 'http://hveem.no/feed/'
        expected_url_begin = 'http://hveem.no/feed/'
        expected_url_host = 'http://hveem.no'
        # Act
        url_begin, url_host = parse_url(url)
        # Assert
        self.assertEqual(url_begin, expected_url_begin)
        self.assertEqual(url_host, expected_url_host)

    def test_parse_url_complicated(self):
        # Arrange
        url = 'http://hveem.no/feed/foo?baz=42&sort#hash'
        expected_url_begin = 'http://hveem.no/feed/foo'
        expected_url_host = 'http://hveem.no'
        # Act
        url_begin, url_host = parse_url(url)
        # Assert
        self.assertEqual(url_begin, expected_url_begin)
        self.assertEqual(url_host, expected_url_host)


class TestSanitizeUrl(unittest.TestCase):

    def test_sanitize_url_https(self):
        # Arrange
        url = 'https://hveem.no/foo?q=bar#hash'
        expected_sanitized_url = 'https://hveem.no/foo?q=bar#hash'
        # Act
        sanitized_url = sanitize_url(url)
        # Assert
        self.assertEqual(sanitized_url, expected_sanitized_url)

    def test_sanitize_url_missing_http(self):
        # Arrange
        url = 'hveem.no/foo?q=bar#hash'
        expected_sanitized_url = 'http://hveem.no/foo?q=bar#hash'
        # Act
        sanitized_url = sanitize_url(url)
        # Assert
        self.assertEqual(sanitized_url, expected_sanitized_url)


class TestConcatUrl(unittest.TestCase):

    def test_concat_url_simple_absolute(self):
        # Arrange
        url = 'http://hveem.no/foo/'
        path = '/index.html'
        expected_sum_url = 'http://hveem.no/index.html'
        # Act
        sum_url = concat_urls(url, path)
        # Assert
        self.assertEqual(sum_url, expected_sum_url)

    def test_concat_url_simple_relative(self):
        # Arrange
        url = 'http://hveem.no/foo/bar'
        path = 'baz/index.html'
        expected_sum_url = 'http://hveem.no/foo/bar/baz/index.html'
        # Act
        sum_url = concat_urls(url, path)
        # Assert
        self.assertEqual(sum_url, expected_sum_url)

    def test_concat_url_simple_relative_with_trailing_slash(self):
        # Arrange
        url = 'http://hveem.no/foo/'
        path = 'index.html'
        expected_sum_url = 'http://hveem.no/foo/index.html'
        # Act
        sum_url = concat_urls(url, path)
        # Assert
        self.assertEqual(sum_url, expected_sum_url)

    def test_concat_url_complicated(self):
        # Arrange
        url = 'http://hveem.no/foo/bar?q=baz'
        path = '/fizz/logo.png'
        expected_sum_url = 'http://hveem.no/fizz/logo.png'
        # Act
        sum_url = concat_urls(url, path)
        # Assert
        self.assertEqual(sum_url, expected_sum_url)


class TestDefaultFaviconUrl(unittest.TestCase):

    def setUp(self):
        self.favicon_url_expected = 'http://hveem.no/favicon.ico'

    def test_default_favicon_url_simple(self):
        # Arrange
        url = 'http://hveem.no'
        # Act
        favicon_url = default_favicon_url(url)
        # Assert
        self.assertEqual(favicon_url, self.favicon_url_expected)

    def test_default_favicon_url_trailing_slash(self):
        # Arrange
        url = 'http://hveem.no/'
        # Act
        favicon_url = default_favicon_url(url)
        # Assert
        self.assertEqual(favicon_url, self.favicon_url_expected)

    def test_default_favicon_url_complex(self):
        # Arrange
        url = 'http://hveem.no/feed'
        # Act
        favicon_url = default_favicon_url(url)
        # Assert
        self.assertEqual(favicon_url, self.favicon_url_expected)

    def test_default_favicon_url_complicated(self):
        # Arrange
        url = 'http://hveem.no/feed/foo/bar?baz=42&sort#hash'
        # Act
        favicon_url = default_favicon_url(url)
        # Assert
        self.assertEqual(favicon_url, self.favicon_url_expected)


if __name__ == '__main__':
    unittest.main()

