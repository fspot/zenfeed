#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function

from app import app
from models import Tag

@app.route('/')
def index():
    nb = len(Tag.query.all())
    return 'Yo. Nb of tags : %d' % nb

