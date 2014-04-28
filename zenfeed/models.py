#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
from flask.ext.sqlalchemy import SQLAlchemy

import arrow

from app import app


db = SQLAlchemy(app)

def setup_tables():
    db.create_all()
    db.engine.echo = app.config['SQL_DEBUG']


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
    has_news = db.Column(db.Boolean)
    favicon_path = db.Column(db.String)

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return u'<Feed %r>' % self.url

    def date(self):
        if self.updated is not None:
            return arrow.Arrow.fromdatetime(self.updated)

    def last_entry(self):
        return self.entries.order_by(Entry.updated.desc()).first()


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

    def date(self):
        return arrow.Arrow.fromdatetime(self.updated)


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


def _update_attr(attr_name, old_obj, new_obj):
    """ Update an object if necessary. Return True if updated. """

    old_value = getattr(old_obj, attr_name)
    new_value = getattr(new_obj, attr_name)
    if new_value != old_value and new_value is not None:
        setattr(old_obj, attr_name, new_value)
        return True


def update_feed(feed, new_feed):
    """ Return True if the feed has changed. """
    assert isinstance(feed, Feed)
    assert isinstance(new_feed, Feed)
    fields = ['title', 'link', 'subtitle', 'author', 'generator',
              'encoding', 'entries_hash'] # no 'updated' field any more

    changed = any([_update_attr(f, feed, new_feed) for f in fields])
    if changed:
        db.session.merge(feed)
    return changed


def create_or_update_entry(feed, new_entry):
    """ Return True if the entry is new or updated.
        When updated, I assume the 'updated' field has changed.
        (I don't force this behaviour). """
    assert isinstance(feed, Feed)
    assert isinstance(new_entry, Entry)
    fields = ['url', 'link', 'title', 'content', 'mimetype',
              'created', 'updated']

    entry = Entry.query.filter_by(feed_id=feed.id, url=new_entry.url).first()
    if entry is None: # create
        new_entry.feed = feed
        print("→→ new entry:", new_entry.title)
        db.session.merge(new_entry)
        return True
    else: # update
        changed = any([_update_attr(f, entry, new_entry) for f in fields])
        if changed:
            print("→→ changed entry:", entry.title)
            db.session.merge(entry)
        return changed
