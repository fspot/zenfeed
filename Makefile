.PHONY: clean

all:
	mkdir -p favicons
	python zenfeed/start.py -d zenfeed.db -f favicons/ --lang fr --tz Europe/Paris

babel-extract:
	pybabel extract -F babel.cfg -o babel.pot zenfeed

#babel-init: pybabel init -i babel.pot -d zenfeed/translations -l en

babel-update:
	pybabel update -i babel.pot -d zenfeed/translations

babel-compile:
	pybabel compile -d zenfeed/translations

test-all:
	python -m unittest discover

test-parsing:
	python -m unittest test.test_feedparser.TestFeedParsing

python3setup:
	pip install Cython==0.20.1
	pip install -r requirements_py3.txt

#build-deb: dpkg-buildpackage -us -uc

clean:
	rm -rf *.pyc zenfeed/*.pyc test/*.pyc build/ dist/ zenfeed.egg-info/

