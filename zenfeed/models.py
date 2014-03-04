#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
from flask.ext.sqlalchemy import SQLAlchemy

from app import app

db = SQLAlchemy(app)

def setup_tables():
    db.create_all()

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return u'<Tag %r>' % self.name

