#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function

import gevent
from gevent.monkey import patch_all
patch_all()
from models import setup_tables
setup_tables()
from app import app
import views
from werkzeug.contrib.fixers import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)
from deadline_manager import deadlineManager

deadlineManager.start()

if app.config['DEBUG']:
    app.run(host='0.0.0.0', port=5000)
else:
    from gevent.wsgi import WSGIServer
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()

#gevent.joinall([deadlineManager])
