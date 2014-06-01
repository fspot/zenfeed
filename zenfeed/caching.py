#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function

from functools import wraps

class Cache(object):
	def __init__(self, app):
		self.memory = {}
		self.enabled = app.config['CACHE_ENABLED']
		app.cache = self

	def to_key(self, args, kwargs):
		tup1 = tuple(args)
		tup2 = tuple(kwargs.items())
		return (tup1, tup2)

	def get(self, *args, **kwargs):
		if not self.enabled: return
		key = self.to_key(args, kwargs)
		return self.memory[key]

	def put(self, value, *args, **kwargs):
		if not self.enabled: return value
		key = self.to_key(args, kwargs)
		self.memory[key] = value
		return value

	def has(self, *args, **kwargs):
		if not self.enabled: return
		key = self.to_key(args, kwargs)
		return key in self.memory

	def delete(self, *args, **kwargs):
		if not self.enabled: return
		key = self.to_key(args, kwargs)
		if key in self.memory:
			del self.memory[key]
