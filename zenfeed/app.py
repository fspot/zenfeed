#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
from flask import Flask

from settings import *

app = Flask(__name__)
app.config.from_object(__name__)

