.PHONY: clean

all:
	@echo "plop"

test-all:
	python -m unittest discover

test-parsing:
	python -m unittest test.test_feedparser.TestFeedParsing

clean:
	rm *.pyc
