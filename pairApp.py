"""
"""

import flask
from flask import render_template, session, redirect, url_for, escape, request

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

	return render_template('index.html')


@app.route("/login")
def login():
	app.logger.debug("Login page entry")

	return render_template('login.html')


# @app.route("/admin")
# @app.route("/admin", methods=['POST'])
def admin():
	app.logger.debug("Admin page entry")
	## INSERT LOGIN LOGIC ##
	## If request isn't POST and session cookie is expired, send to login page
	## Else, send to admin page
	# #########

	if 'username' in session:
		return 'Logged in as %s' % escape(session['username'])

	return 'You are not logged in'


	# if request.method != 'POST':
	# 	return flask.render_template('login.html')
	# else:
		
	# 	return flask.render_template('admin.html') ## Only return if login is successful


@app.route("/admin", methods=['POST'])
def admin_login():
	app.logger.debug("Admin login attempt")

	error = None

	if request.method == 'POST':
		session['username'] = request.form['username']
		if valid_login(request.form['username'], request.form['password']):
			return log_the_user_in(request.form['username'])
		else:
			error = 'Invalid username/password'
		
		return render_template('login.html', error=error)

@app.route("/logout")
def logout():
	session.pop('username', None)

	return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(error):
	app.logger.debug("Page not found")
	session['linkback'] = url_for("index")

	return render_template("page_not_found.html")


#####################
##
##	Functions used within templates
##
#####################
def valid_login(username, password):
	"""
	"""
	if username == "admin":
		if password == "password":
			return True
		else:
			return False
	else:
		return False


def log_the_user_in(username):
	"""
	"""
	return flask.render_template('admin.html')


if __name__ == "__main__":
	import uuid
	app.secret_key = str(uuid.uuid4())
	app.debug = cfg.DEBUG
	app.logger.setLevel(logging.DEBUG)
	app.run(port=cfg.PORT)