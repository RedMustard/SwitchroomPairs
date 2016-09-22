"""
"""

import flask
from flask import render_template, session, redirect, url_for, escape, request
from datetime import date, time, datetime, timedelta

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

	error = None
	if 'username' in session:
		session.pop('username', None)

	if 'error' in session:
		error = session['error']
		session.pop('error', None)

	return render_template('index.html', error=error, entries=get_db(), used_pairs=get_used_pairs())


@app.route("/login")
def login():
	app.logger.debug("Login page entry")

	return render_template('login.html')


@app.route("/logout")
def logout():
	session.pop('username', None)

	return redirect(url_for('index'))


@app.route("/admin")
def admin():
	app.logger.debug("Admin page entry")
	## INSERT LOGIN LOGIC ##
	## If request isn't POST and session cookie is expired, send to login page
	## Else, send to admin page
	# #########

	if 'username' in session:
		return log_the_user_in(session['username'])
	else:
		error = 'You are not logged in'

	return render_template('login.html', error=error)


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


@app.route("/log")
def db_log():
	if 'username' in session:
		# if session['username'] == is_admin()
		return render_template('log.html', entries=get_log_db())
	else:
		error = 'You are not logged in'

	return render_template('login.html', error=error)


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

	################################### CHANGE TO SELECT ADMIN USER FROM DB 'is_admin()'
	if username == 'admin':
		return render_template('admin.html', entries=get_db(), used_pairs=get_used_pairs())


@app.template_filter('admin_db')
def get_db():
	"""Retrieves 
	"""
	entries = db.get_db(DB_CURSOR)
	return entries


def get_log_db():
	"""
	"""
	entries = db.get_log_db(DB_CURSOR)
	return entries


def get_used_pairs():
	"""Retrieves all pairs stored in the database.

	Returns:
		pairs - A list containing all used pairs
	"""
	pairs = db.get_used_pairs(DB_CURSOR)
	return pairs


@app.route("/submit", methods=['POST'])
def insert_entry_into_database():
	"""
	"""
	form_fields = ['circuit_id', 'circuit_type', 'cl_pair', 'uo_pair', 
		'customer_name', 'customer_phone', 'notes']
	entry = []
	error = None
	print("submit sent")
	if request.method == 'POST':
		for item in form_fields:
			session[item] = request.form[item]
			entry.append(request.form[item])

		date_added = datetime.now().date()
		time_added = datetime.now()

		print(datetime.now())
		print("TIME ADDED: {}".format(time_added))

		entry.append(date_added)
		entry.append(time_added)

		if 'username' in session:
			entry.append(session['username'])
		else:
			entry.append('centlink')

		print("Inserting entry...")
		db.insert_entry(DB_CURSOR, entry)
		db.db_commit(DATABASE)

	else:
		error = 'An error occurred processing your request.'
		session['error'] = error

	return admin()


@app.route("/delete", methods=['POST'])
def delete_entry_from_database():
	"""
	"""
	error = None

	if request.method == 'POST':
		cl_pair = request.form['cl_pair']
		uo_pair = request.form['uo_pair']

		print("Getting entry id...")
		entry_id = db.get_entry_id(DB_CURSOR, cl_pair, uo_pair)

		print("Deleting entry...")
		db.delete_entry(DB_CURSOR, entry_id)
		db.db_commit(DATABASE)

	else:
		error = 'An error occurred processing your request.'
		session['error'] = error

	return index()


@app.route("/edit", methods=['POST'])
def edit_entry_in_database():
	"""
	"""
	form_fields = ['customer_name', 'cl_pair', 'circuit_type', 'circuit_id', 
		'customer_phone', 'uo_pair', 'notes']
	entry = []
	error = None

	if request.method == 'POST':
		for field in form_fields:
			entry.append(request.form[field])

		print("Getting entry id...")	
		entry_id = db.get_entry_id(DB_CURSOR, entry[1], entry[5])

		# If admin is logged in, edit the entry
		if 'username' in session:
			print("Editing entry as admin...")
			db.edit_entry(DB_CURSOR, entry_id, entry)
			return redirect(url_for("admin"))

		# Else, did a centlink user submit the entry? Was it less than 60 minutes ago?
		else:
			print("Checking which user submitted entry...")
			if db.get_entry_author(DB_CURSOR, entry_id) == 'centlink':
				print("Checking timestamp for std user....")
				time_now = datetime.now()
				time_delta = timedelta(seconds=1)
				time_entry = db.get_entry_timestamp(DB_CURSOR, entry_id)

				if time_entry > (time_now - time_delta):
					print("Entry is less than 1 hour old and can be edited by centlink user...")
					db.edit_entry(DB_CURSOR, entry_id, entry)
					return redirect(url_for("index"))

				else:
					error = "This entry is greater than 1 hour old and cannot be edited by centlink user."
					session['error'] = error
					return redirect(url_for("index"))

			else:
				error = "Admin created the entry and cannot be edited by centlink user"
				session['error'] = error
				return redirect(url_for("index"))

	else:
		error = 'An error occurred processing your request.'
		session['error'] = error

	return redirect(url_for("index"))


if __name__ == "__main__":
	import uuid
	app.secret_key = str(uuid.uuid4())
	app.debug = cfg.DEBUG
	app.logger.setLevel(logging.DEBUG)
	app.run(port=cfg.PORT)