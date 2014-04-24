.PHONY: clean

all:
	python zenfeed/start.py

test-all:
	python -m unittest discover

test-parsing:
	python -m unittest test.test_feedparser.TestFeedParsing

clean:
	rm -rf *.pyc zenfeed/*.pyc test/*.pyc build/ dist/ zenfeed.egg-info/

