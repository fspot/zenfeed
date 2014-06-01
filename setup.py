#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages
import zenfeed

setup(
    name="zenfeed",
    version=zenfeed.__version__,
    install_requires=["beautifulsoup4", "Flask", "Flask-SQLAlchemy", "docopt",
                      "feedparser", "gevent", "path.py", "requests",
                      "flask-babel", "pytz"],
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

