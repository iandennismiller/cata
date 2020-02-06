# Python Makefile

SHELL=/bin/bash
MOD_NAME=catalog
TEST_CMD=nosetests -w $(MOD_NAME) -c etc/tests.cfg --with-coverage --cover-package=$(MOD_NAME)

install:
	python setup.py install

requirements:
	pip install -r requirements.txt

develop:
	pip install -r .requirements-dev.txt

clean:
	rm -rf build dist *.egg-info
	find . -name '*.pyc' -delete
	find . -name __pycache__ -delete

docs:
	rm -rf build/sphinx
	sphinx-build -b html docs build/sphinx

watch:
	watchmedo shell-command -R -p "*.py" -c 'date; $(TEST_CMD); date' .

test:
	$(TEST_CMD)

tox:
	tox

release:
	# 1. create ~/.pypirc
	# 2. python setup.py register # notify pypi of new package
	python setup.py sdist upload

coverage:
	nosetests --with-xcoverage --cover-package=$(MOD_NAME) --cover-tests -c etc/tests.cfg

# create a homebrew install script
homebrew:
	bin/poet-homebrew.sh
	cp /tmp/catalog.rb etc/catalog.rb

.PHONY: clean install test watch docs release tox develop homebrew coverage requirements