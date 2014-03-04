#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
from flask.ext.sqlalchemy import SQLAlchemy

from app import app

db = SQLAlchemy(app)

def setup_tables():
    db.create_all()


tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('feed_id', db.Integer, db.ForeignKey('feed.id'))
)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return u'<Tag %r>' % self.name


class Feed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False, unique=True)
    entries = db.relationship('Entry', backref='feed', lazy='dynamic')
    tags = db.relationship('Tag', secondary=tags,
        backref=db.backref('feeds', lazy='dynamic'), lazy='dynamic')

    title = db.Column(db.String)
    link = db.Column(db.String)
    subtitle = db.Column(db.String)
    author = db.Column(db.String)
    generator = db.Column(db.String)
    encoding = db.Column(db.String)
    updated = db.Column(db.DateTime)
    entries_hash = db.Column(db.String) # last updated entries hash
    refresh_interval = db.Column(db.Integer)
    max_entries = db.Column(db.Integer)
    highlight_news = db.Column(db.Boolean)

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return u'<Feed %r>' % self.url


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feed_id = db.Column(db.Integer, db.ForeignKey('feed.id'))

    url = db.Column(db.String) # ['id']
    link = db.Column(db.String) # ['link']
    title = db.Column(db.String)
    content = db.Column(db.Text) # ['value'], or ['content'][0]['value']
    mimetype = db.Column(db.String) # ['value'], or ['content'][0]['type']
    created = db.Column(db.DateTime) # or published
    updated = db.Column(db.DateTime)
    public = db.Column(db.Boolean)

    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __repr__(self):
        return u'<Entry %r>' % self.title


class Config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False, unique=True)

    default_refresh_interval = db.Column(db.Integer)
    default_max_entries = db.Column(db.Integer)
    default_highlight_news = db.Column(db.Boolean)

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def __repr__(self):
        return u'<Config of %r>' % self.login
