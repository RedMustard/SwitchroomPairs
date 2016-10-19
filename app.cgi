#! /usr/local/bin/python3.4

import site
site.addsitedir("/var/www/html/SwitchroomPairs/env/lib/python3.4/site-packages")

from wsgiref.handlers import CGIHandler
from pairApp import app

CGIHandler().run(app)