#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function

from log import logger
import models


def get_step_list(from_version):
    # Zenfeed versions introducing migrations
    versions = [
        '0.0.3',
    ]
    return versions[versions.index(from_version) + 1:]


# def migration__0_0_4():
#     models.db.engine.execute("ALTER TABLE config ADD COLUMN foo INT;")


def run_migrations(from_version):
    step_list = get_step_list(from_version)
    for step in step_list:
        migration_func = globals()['migration__' + step.replace('.', '_')]
        logger.warning("Migration from v%s to v%s...", from_version, step)
        migration_func()
        models.Config.get().version = step
        models.db.session.commit()
        from_version = step
