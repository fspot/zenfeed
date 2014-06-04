#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
import sys

from flask import Flask
from flask.ext.babel import Babel

def current_module():
	return sys.modules[__name__]

def create_flask_app(prefix):
	current_module().app = Flask(__name__, static_url_path=prefix + "/static")
	create_babel()
	return current_module().app

def create_babel():
	current_module().babel = Babel(current_module().app)
