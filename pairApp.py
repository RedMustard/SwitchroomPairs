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


@app.route("/login")
def login():
	app.logger.debug("Login page entry")

	return flask.render_template('login.html')


@app.route("/admin")
@app.route("/admin", methods=['POST'])
def admin():
	app.logger.debug("Admin page entry")
	## INSERT LOGIN LOGIC ##
	## If request isn't POST and session cookie is expired, send to login page
	## Else, send to admin page
	#########
	if request.method != 'POST':
		return flask.render_template('login.html')
	else:
		
		return flask.render_template('admin.html') ## Only return if login is successful


@app.errorhandler(404)
def page_not_found(error):
	app.logger.debug("Page not found")
	flask.session['linkback'] = flask.url_for("index")

	return flask.render_template("page_not_found.html")


if __name__ == "__main__":
	import uuid
	app.secret_key = str(uuid.uuid4())
	app.debug = cfg.DEBUG
	app.logger.setLevel(logging.DEBUG)
	app.run(port=cfg.PORT)