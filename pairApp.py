"""
"""

import flask
from flask import render_template
from flask import request
from flask import url_for

import json
import logging
import config as cfg
import uuid 


app = flask.Flask(__name__)
app.secret_key = str(uuid.uuid4())
app.debug = cfg.DEBUG
app.logger.setLevel(logging.DEBUG)


###
# PAGES
###
@app.route("/")
@app.route("/index")
def index():
	app.logger.debug("Main page entry")

	return flask.render_template('index.html')


if __name__ == "__main__":
	import uuid
	app.secret_key = str(uuid.uuid4())
	app.debug = cfg.DEBUG
	app.logger.setLevel(logging.DEBUG)
	app.run(port = cfg.PORT)