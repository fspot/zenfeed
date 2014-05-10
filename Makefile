.PHONY: clean

all:
	mkdir -p favicons
	python zenfeed/start.py -d zenfeed.db -f favicons/

babel-extract:
	pybabel extract -F babel.cfg -o babel.pot zenfeed

#babel-init: pybabel init -i messages.pot -d zenfeed/translations -l en

babel-update:
	pybabel update -i babel.pot -d zenfeed/translations

babel-compile:
	pybabel compile -d zenfeed/translations

test-all:
	python -m unittest discover

test-parsing:
	python -m unittest test.test_feedparser.TestFeedParsing

clean:
	rm -rf *.pyc zenfeed/*.pyc test/*.pyc build/ dist/ zenfeed.egg-info/

