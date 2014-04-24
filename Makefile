.PHONY: clean

all:
	mkdir -p favicons
	python zenfeed/start.py -d zenfeed.db -f favicons/

test-all:
	python -m unittest discover

test-parsing:
	python -m unittest test.test_feedparser.TestFeedParsing

clean:
	rm -rf *.pyc zenfeed/*.pyc test/*.pyc build/ dist/ zenfeed.egg-info

