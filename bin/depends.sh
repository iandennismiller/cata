#!/usr/bin/bash
# catalog (c) Ian Dennis Miller

source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv -a . -r requirements-dev.txt catalog
source ~/.virtualenvs/catalog/bin/activate
