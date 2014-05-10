#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
from flask import Flask
from flask.ext.babel import Babel

app = Flask(__name__)
babel = Babel(app)

