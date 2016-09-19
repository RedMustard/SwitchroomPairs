"""
"""

import flask
from flask import render_template, session, redirect, url_for, escape, request

import json
import logging
import config as cfg
import uuid 
import db

app = flask.Flask(__name__)
app.secret_key = str(uuid.uuid4())
app.debug = cfg.DEBUG
app.logger.setLevel(logging.DEBUG)

DATABASE = db.connect_to_database()
DB_CURSOR = DATABASE.cursor(buffered=True)



##########
##
##  PAGES
##
##########
@app.route("/")
@app.route("/index")
def index():
	app.logger.debug("Main page entry")
	return render_template('index.html', entries=return_admin_db())


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
	return render_template('admin.html')


@app.template_filter('admin_db')
def return_admin_db():
	"""
	"""
	entries = db.get_db(DB_CURSOR)
	return entries


@app.route("/submit", methods=['POST'])
def insert_entry_into_database():
	"""
	"""
	form_fields = ['circuit_id', 'circuit_type', 'cl_pair', 'uo_pair', 'customer_name', 'customer_phone', 'notes']
	entry = []
	error = None
	print("submit sent")
	if request.method == 'POST':
		print('request is post')

		for item in form_fields:
			session[item] = request.form[item]
			# print(request.form[item])
			entry.append(request.form[item])


		db.insert_entry(DB_CURSOR, entry)
		db.db_commit(DATABASE)

	else:
		error = 'An error occurred processing your request.'

	# print("redirecting")
	# return render_template('index.html')
	# return redirect(url_for('index'))
	# return Response(response=json.dumps({'url': url_for('index')}, mimetype="text/json"))
	return index()


@app.route("/delete", methods=['POST'])
def delete_entry_from_database():
	"""
	"""
	error = None

	if request.method == 'POST':
		circuit_id = request.form['circuit_id']
		cl_pair = request.form['cl_pair']
		uo_pair = request.form['uo_pair']

		print("getting id...")
		entry_id = db.get_entry_id(DB_CURSOR, circuit_id, cl_pair, uo_pair)

		db.delete_entry(DB_CURSOR, entry_id)
		db.db_commit(DATABASE)

	else:
		error = 'An error occurred processing your request.'

	return index()
	# db.delete_entry(cursor, db.get_entry_id(cursor, ))


if __name__ == "__main__":
	import uuid
	app.secret_key = str(uuid.uuid4())
	app.debug = cfg.DEBUG
	app.logger.setLevel(logging.DEBUG)
	app.run(port=cfg.PORT)