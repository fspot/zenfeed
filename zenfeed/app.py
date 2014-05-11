#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
from flask import Flask
from flask.ext.babel import Babel
from flask.ext.cache import Cache

from settings import CACHE_CONFIG

app = Flask(__name__)
babel = Babel(app)
cache = Cache(app, config=CACHE_CONFIG)
