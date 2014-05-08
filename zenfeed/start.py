#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""Zen RSS feed reader.

Usage:
  zenfeed [-d URI -f PATH -p PORT -l LOG --debug]
  zenfeed genstatic PATH
  zenfeed -h | --help
  zenfeed -v | --version

Options:
  -h --help           Show this screen.
  -v --version        Show version.
  -d --database URI   Specify database URI (SQLAlchemy format).
                      For SQLite, this is just a file name.
                      [default: ./zenfeed.db]
  -f --favicons PATH  Specify where favicons will be put.
                      [default: ./]
  -p --port PORT      Specify on which port to listen.
                      [default: 5000]
  -l --log LOG        Specify where to log messages, and which level to set.
                      Can be "stderr", "syslog", or a filename, followed by the level.
                      [default: stderr:INFO]
  --debug             Use werkzeug debug WSGI server.

"""

from __future__ import unicode_literals, print_function
from docopt import docopt
from path import path
import logging

# avoid side effects with imports…
import gevent
from gevent.monkey import patch_socket, patch_ssl
import zenfeed
from log import setup_logger, logger

def genstatic(dst):
    path.copytree(path(zenfeed.__path__[0]) / 'static', dst)

def main():
    args = docopt(__doc__, version='zenfeed ' + zenfeed.__version__)
    if args['genstatic']:
        return genstatic(args['PATH'])

    port = int(args['--port'])
    log_arg, log_level = args['--log'].rsplit(':', 1)
    if log_arg not in ('stderr', 'syslog'):
        setup_logger(type='file', filename=path(log_arg).abspath(),
                     level=log_level)
    else:
        setup_logger(type=log_arg, level=log_level)
    db_uri = args['--database']
    if db_uri == ':memory:':
        db_uri = 'sqlite://'
    elif not "://" in db_uri:
        db_uri = 'sqlite:///%s' % path(db_uri).abspath()

    from app import app
    app.config.update(
        DEBUG = args['--debug'],
        SQL_DEBUG = False,
        SECRET_KEY = 'ssshhhh',
        SQLALCHEMY_DATABASE_URI = db_uri,
        FAVICON_DIR = path(args['--favicons']).abspath(),
    )

    from models import setup_tables, Feed
    patch_socket()
    patch_ssl()
    setup_tables()

    from deadline_manager import deadlineManager
    import views
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)

    feeds = Feed.query.all()
    deadlineManager.favicon_dir = path(args['--favicons']).abspath()
    deadlineManager.launch_deadline_workers(feeds)
    deadlineManager.start()

    if args['--debug']:
        logger.info("Server started in DEBUG mode at port %d", port)
        app.run(host='0.0.0.0', port=port, debug=True)
    else:
        logger.info("Server started in PRODUCTION mode at port %d", port)
        from gevent.wsgi import WSGIServer
        http_server = WSGIServer(('0.0.0.0', port), app)
        try:
            http_server.serve_forever()
        except KeyboardInterrupt:
            pass
    #gevent.joinall([deadlineManager])

if __name__ == '__main__':
    main()

