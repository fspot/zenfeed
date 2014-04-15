#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="zenfeed",
    version="0.0.1", # update it in __init__.py also. Now!
    install_requires=["BeautifulSoup", "Flask", "Flask-SQLAlchemy", "feedparser", "gevent", "path.py", "requests"],
    packages=find_packages(),
    author="fspot",
    author_email="fred@fspot.org",
    description="Zen RSS feed reader.",
    long_description=open("README.md").read(),
    include_package_data=True,
    zip_safe=False,
    url="http://github.com/fspot/zenfeed",
    entry_points = {
        "console_scripts": [
            'zenfeed = zenfeed.start:main',
        ],
    },
    license="BSD",
)

