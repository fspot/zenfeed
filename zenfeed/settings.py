#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
from path import path

sqlite_database = path('zenfeed.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % sqlite_database.abspath()
DEBUG = True
SECRET_KEY = 'ssshhhh'

