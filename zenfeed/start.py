#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function

# avoid side effects with imports…
import gevent
from gevent.monkey import patch_socket, patch_ssl
from models import setup_tables, Feed

def main():
    patch_socket()
    patch_ssl()
    setup_tables()
    from app import app
    import views
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    from deadline_manager import deadlineManager

    feeds = Feed.query.all()
    deadlineManager.launch_deadline_workers(feeds)
    deadlineManager.start()

    if app.config['DEBUG']:
        app.run(host='0.0.0.0', port=5000)
    else:
        from gevent.wsgi import WSGIServer
        http_server = WSGIServer(('0.0.0.0', 5000), app)
        http_server.serve_forever()
    #gevent.joinall([deadlineManager])

if __name__ == '__main__':
    main()

