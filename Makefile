.PHONY: clean

all:
	python zenfeed/start.py

test-all:
	python -m unittest discover

test-parsing:
	python -m unittest test.test_feedparser.TestFeedParsing

clean:
	rm *.pyc zenfeed/*.pyc test/*.pyc

