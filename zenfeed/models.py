#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
from hashlib import sha256
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import class_mapper, ColumnProperty

from app import app
from log import logger
from migrations import run_migrations
from settings import (VERSION, DEFAULT_LOGIN, DEFAULT_PASSWORD,
    DEFAULT_REFRESH_INTERVAL, DEFAULT_MAX_ENTRIES, DEFAULT_HIGHLIGHT_NEWS,
    DEFAULT_ENTRIES_PER_PAGE)


db = SQLAlchemy(app)

def setup_tables():
    db.create_all()
    if Config.get() is None:
        logger.info("Creating Config single instance")
        Config.query.delete()
        c = Config(
            version=VERSION,
            login=DEFAULT_LOGIN,
            password=Config.hash(DEFAULT_PASSWORD),
            default_refresh_interval=DEFAULT_REFRESH_INTERVAL,
            default_max_entries=DEFAULT_MAX_ENTRIES,
            default_highlight_news=DEFAULT_HIGHLIGHT_NEWS,
            default_entries_per_page=DEFAULT_ENTRIES_PER_PAGE,
        )
        db.session.add(c)
        db.session.commit()
        Config.refresh_instance()
    elif Config.get().version != VERSION:
        run_migrations(from_version=Config.get().version)
    db.engine.echo = app.config['SQL_DEBUG']


tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('feed_id', db.Integer, db.ForeignKey('feed.id'))
)


class Base(object):
    @classmethod
    def fields_set(cls, exclude_fields=None):
        exclude_fields = exclude_fields or []
        my_fields = [prop.key for prop in class_mapper(cls).iterate_properties
                     if isinstance(prop, ColumnProperty)]
        return set(my_fields) - set(exclude_fields)

    def to_dict(self, exclude_fields=None):
        fields = self.fields_set(exclude_fields)
        return dict((field, getattr(self, field)) for field in fields)



class Tag(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return u'<Tag %r>' % self.name


class Feed(db.Model, Base):
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
    entries_per_page = db.Column(db.Integer)
    highlight_news = db.Column(db.Boolean)
    has_news = db.Column(db.Boolean)
    favicon_path = db.Column(db.String)

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return u'<Feed %r>' % self.url

    def last_entry(self):
        return self.entries.order_by(Entry.updated.desc()).first()


class Entry(db.Model, Base):
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


class Config(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String)
    login = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False, unique=True)

    default_refresh_interval = db.Column(db.Integer)
    default_max_entries = db.Column(db.Integer)
    default_entries_per_page = db.Column(db.Integer)
    default_highlight_news = db.Column(db.Boolean)

    instance = None
    salt = "saltpepperandcurry"

    @staticmethod
    def get():
        if Config.instance is None:
            Config.refresh_instance()
        return Config.instance

    @staticmethod
    def refresh_instance():
        Config.instance = Config.query.get(1)

    @staticmethod
    def validate_password(pw):
        return Config.get().password == pw

    @staticmethod
    def change_password(pw):
        logger.warning("Password changed !")
        Config.get().password = Config.hash(pw)

    @staticmethod
    def hash(pw):
        string = (pw + Config.salt).encode('utf-8')
        return sha256(string).hexdigest()

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
              'encoding',] # no more ['updated', 'entries_hash'] fields

    changed = any([_update_attr(f, feed, new_feed) for f in fields])
    if changed:
        db.session.merge(feed)
    return changed


def create_or_update_entry(feed_id, new_entry):
    """ Return True if the entry is new.
        When updated, I assume the 'updated' field has changed.
        (I don't force this behaviour). """
    # assert isinstance(feed, Feed)
    assert isinstance(new_entry, Entry)
    fields = ['url', 'link', 'title', 'content', 'mimetype',
              'created', 'updated']

    entry = Entry.query.filter_by(feed_id=feed_id, url=new_entry.url).first()
    if entry is None: # create
        new_entry.feed_id = feed_id
        logger.info("→→ new entry: %s", new_entry.title)
        db.session.merge(new_entry)
        return True
    else: # update
        changed_fields = [_update_attr(f, entry, new_entry) for f in fields]
        changed_fields_strings = [s for s,b in zip(fields, changed_fields) if b]
        changed = any(changed_fields)
        if changed:
            logger.info("→→ changed entry: %s | %s", entry.title, repr(changed_fields_strings))
            db.session.merge(entry)
        return False
