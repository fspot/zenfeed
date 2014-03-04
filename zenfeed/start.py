#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function

from models import setup_tables
setup_tables()

from app import app
import views

app.run(host="0.0.0.0", port=8000)

