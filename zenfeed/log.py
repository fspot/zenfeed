#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
from logging import handlers
logger = logging.getLogger('zenfeed')


def parse_level(level):
    return {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warn': logging.WARNING,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL,
    }[level]

def setup_logger(**params):
    params['level'] = parse_level(params['level'].lower())
    if not 'format' in params:
        params['format'] = "%(asctime)s %(name)-8s %(levelname)-8s | %(message)s"
    if params['type'] == 'file':
        handler = logging.FileHandler(params['filename'])
    elif params['type'] == 'stderr':
        handler = logging.StreamHandler()
    elif params['type'] == 'syslog':
        handler = handlers.SysLogHandler(address='/dev/log')
    logger.setLevel(params['level'])
    handler.setLevel(params['level'])
    handler.setFormatter(logging.Formatter(params['format']))
    logger.addHandler(handler)
