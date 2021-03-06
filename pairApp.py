"""Century Link Demarcation & Cross-Connect Server

This program functions as the server for the University of Oregon/Century Link 
Demarcation & Cross-Connect app.

This server uses Flask to serve webpages. Flask documentation is available at:
	http://flask.pocoo.org/docs/0.11/
"""

import flask
from flask import render_template, session, redirect, url_for, escape, request
import flask_mail
from flask_mail import Mail, Message
from datetime import date, time, datetime, timedelta

import json
import logging
import config as cfg
import db

DATABASE = db.connect_to_database()
DB_CURSOR = DATABASE.cursor(buffered=True)

app = flask.Flask(__name__)
app.secret_key = cfg.KEY
app.debug = cfg.DEBUG
app.logger.setLevel(logging.DEBUG)
app.config.update(**cfg.mail_config_dictionary)
mail = Mail(app)


##########
##
##  WEB PAGES
##
##########
@app.route("/")
@app.route("/index")
def index():
	app.logger.debug("Main page entry")
	error = None

	if 'username' in session:
		session.pop('username', None)

	if 'password' in session: 
		session.pop('password', None)

	if 'error' in session:
		error = session['error']
		session.pop('error', None)

	return render_template('/index.html', error=error, entries=get_db(), 
		used_pairs=get_used_pairs())


@app.route("/login")
def login():
	app.logger.debug("Login page entry")
	return render_template('/login.html')


@app.route("/logout")
def logout():
	session.pop('username', None)
	session.pop('password', None)
	return redirect(url_for('index'))


@app.route("/admin")
def admin():
	app.logger.debug("Admin page entry")
	
	error = None

	if 'username' in session and 'password' in session:
		if is_admin(session['username'], session['password']):
			return render_template('/admin.html', entries=get_db(), 
				used_pairs=get_used_pairs(), error=error)
	else:
		error = 'You are not logged in'
		return render_template('/login.html', error=error)


@app.route("/admin", methods=['POST'])
def admin_login():
	app.logger.debug("Admin login attempt")

	error = None

	if request.method == 'POST':
		session['username'] = request.form['username']
		session['password'] = request.form['password']

		if is_admin(request.form['username'], request.form['password']):
			return render_template('/admin.html', entries=get_db(), 
				used_pairs=get_used_pairs(), error=error)

		else:
			error = 'Invalid username or password. Please try again.'
			session.pop('username', None)
			session.pop('password', None)

			return render_template('/login.html', error=error)
	else:
		error = "An unexpected error occurred. Please try again."
		return render_template("/login.html")


@app.route("/account")
def admin_account():
	app.logger.debug("Admin account page entry")
	error = None

	if 'username' in session and 'password' in session:
		if is_admin(session['username'], session['password']):
			return render_template('/account.html')
	else:
		error = 'You are not logged in'
		return render_template('/login.html', error=error)


@app.route("/update-account", methods=['POST']) 
def update_account():
	app.logger.debug("Admin account update attempt")

	error = None

	if request.method == 'POST':
		old_pass = request.form['old-password']
		new_pass = request.form['new-password']
		confirm_new_pass = request.form['verify-new-password']

		if new_pass != confirm_new_pass:
			error = ("Your new password and confirmation password did not " + 
				"match. Please try again.")
			return render_template('/account.html', error=error)

		# If the admin is currently logged in, verify the old password is 
		#	correct and then update with the new password
		if 'username' in session and 'password' in session:
			if is_admin(session['username'], old_pass):
				if old_pass == new_pass:
					error = ("Your new password cannot be the same as the " + 
						"old password.")
					return render_template('/account.html', error=error)
				else:	
					update_member = ('''UPDATE members SET password = MD5(%s) 
						WHERE username = %s''')
					DB_CURSOR.execute(update_member, (new_pass, 
						session['username']))
					db.db_commit(DATABASE)
					session['password'] = new_pass
					
					message = "Your password has been successfully changed"
					return render_template('/account.html', message=message)

			else:
				error = "The old password is incorrect. Please try again."
				return render_template('/account.html', error=error)

		else:
			error = 'You are not logged in.'
			return render_template('/login.html', error=error)
	else:
		error = "An unexpected error occurred. Please try again."
		return render_template("/account.html", error=error)


@app.route("/update-account") 
def update_account_without_post():
	app.logger.debug("Admin account update without POST attempt")
	error = None

	if 'username' in session and 'password' in session:
		if is_admin(session['username'], session['password']):
			return render_template("/account.html")

	else:
		error = "You are not logged in."
		return render_template("/login.html", error=error)


@app.route("/log")
def db_log():
	app.logger.debug("Log page entry")
	error = None

	if 'username' in session and 'password' in session:
		if is_admin(session['username'], session['password']):
			return render_template('/log.html', entries=get_log_db())
	else:
		error = 'You are not logged in.'

	return render_template('/login.html', error=error)


@app.errorhandler(404)
def page_not_found(error):
	app.logger.debug("Page not found")
	session['linkback'] = url_for("index")

	return render_template("page_not_found.html")


#####################
##
##	Functions used within pages
##
#####################
def is_admin(username, password):
	"""Authenticates a user based on a given username and password.

	Keyword Arguments:
		username - String containing the username to be authenticated
		password - String containing the password to be authenticated

	Returns:
		True - User is an admin
		False - User is not an admin
	"""
	member = None

	get_member = ('''SELECT * FROM members WHERE username = %s AND 
		password = MD5(%s)''')
	DB_CURSOR.execute(get_member, (username, password))

	for entry in DB_CURSOR:
		member = entry

	if member == None:
		return False
	else:
		return True


@app.template_filter('admin_db')
def get_db():
	"""Retrieves the entire contents of the 'pairs' table.

	Returns:
		entries - List containing each row of the table
	"""
	entries = db.get_db(DB_CURSOR)
	return entries


def get_log_db():
	"""Retrieves the entire contents of the 'pairs_audit' table.

	Returns:
		entries - List containing each row of the table
	"""
	entries = db.get_log_db(DB_CURSOR)
	return entries


def get_used_pairs():
	"""Retrieves all pairs stored in the database.

	Returns:
		pairs - List containing all pairs
	"""
	pairs = []

	get_pairs = ('''SELECT cl_pair, uo_pair FROM pairs''')
	DB_CURSOR.execute(get_pairs)

	for entry in DB_CURSOR:
		pairs.append(entry[0])
		pairs.append(entry[1])

	return pairs


def __send_email(action, entry_data):
	"""Sends an email whenever the database is updated by centlink users.
	"""
	msg = Message("Demarcation database {} performed".format(action),
			recipients=[cfg.MAIL_RECIPIENT])

	if action == "insert" or action == "edit":
		msg.body = ("An {} has been performed on the demarc ".format(action) +
				"database with the following information: \n\n" + 
				"Circuit ID: {} \n".format(entry_data[0] if action=="insert" 
					else entry_data[3]) +
				"Circuit Type: {} \n".format(entry_data[1] if action=="insert" 
					else entry_data[2]) +
				"Century Link Pair: {} \n".format(entry_data[2] if action=="insert" 
					else entry_data[1]) +
				"UO Cross-Connect Pair: {} \n".format("N/A" 
					if int(entry_data[3] if action=="insert" else entry_data[5]
							) == 0 
					else '%03d' % int(entry_data[3] if action=="insert" 
										else entry_data[5])) +
				"Customer Name: {} \n".format(entry_data[4] if action=="insert" 
					else entry_data[0]) +
				"Customer Phone: {} \n".format(entry_data[5] if action=="insert" 
					else entry_data[4]) +
				"Notes: {} \n".format(entry_data[6]))

	elif action == "delete":
		msg.body = ("A {} has been performed on the demarc ".format(action) +
				"database with the following information: \n\n" + 
				"Century Link Pair: {} \n".format(entry_data[0]) +
				"UO Cross-Connect Pair: {} \n".format(
					"N/A" if int(entry_data[1]) == 0 
						else '%03d' % int(entry_data[1])))

	else:
		msg.body = """An error occured compiling the body of this message.
			Check the log database in order to determine what was changed."""

	mail.send(msg)


@app.route("/submit", methods=['POST'])
def insert_entry_into_database():
	"""Inserts an entry into the 'pairs' table.
	"""
	form_fields = ['circuit_id', 'circuit_type', 'cl_pair', 'uo_pair', 
		'customer_name', 'customer_phone', 'notes']
	entry = []
	error = None
	
	if request.method == 'POST':
		for item in form_fields:
			session[item] = request.form[item]
			entry.append(request.form[item])

		date_added = datetime.now().date()
		time_added = datetime.now()

		entry.append(date_added)
		entry.append(time_added)

		if 'username' in session:
			entry.append(session['username'])
		else:
			entry.append('centlink')
			__send_email("insert", entry)

		db.insert_entry(DB_CURSOR, entry)
		db.db_commit(DATABASE)

	else:
		error = '**ERROR: An error occurred processing your request.**'
		session['error'] = error

	return admin()


@app.route("/delete", methods=['POST'])
def delete_entry_from_database():
	"""Deletes an entry from the 'pairs' table.
	"""
	error = None

	if request.method == 'POST':
		cl_pair = request.form['cl_pair']
		uo_pair = request.form['uo_pair']

		if uo_pair == "N/A":
			uo_pair = 0

		entry_id = db.get_entry_id(DB_CURSOR, cl_pair, uo_pair)

		# If admin is logged in, edit the entry
		if 'username' in session:
			user = "admin"
			db.delete_entry(DB_CURSOR, entry_id, user)
			db.db_commit(DATABASE)
			return redirect(url_for("admin"))

		# Else, did a centlink user submit the entry? Was it less than 60 
		#	minutes ago?
		else:
			if db.get_entry_author(DB_CURSOR, entry_id) == 'centlink':
				time_now = datetime.now()
				time_delta = timedelta(hours=1)
				time_entry = db.get_entry_timestamp(DB_CURSOR, entry_id)

				if time_entry > (time_now - time_delta):
					user = "centlink"
					entry = [cl_pair, uo_pair]
					db.delete_entry(DB_CURSOR, entry_id, user)
					db.db_commit(DATABASE)
					__send_email("delete", entry)
					return redirect(url_for("index"))

				else:
					error = ("**ERROR: This entry is over 1 hour old and " + 
						"cannot be deleted by standard users.**")
					session['error'] = error
					return error
			else:
				error = ("**ERROR: An admin created this entry and cannot be " + 
					"deleted by standard users.**")
				session['error'] = error
				return error
	else:
		error = '**ERROR: An error occurred processing your request.**'
		session['error'] = error

	return redirect(url_for("index"))


@app.route("/edit", methods=['POST'])
def edit_entry_in_database():
	"""Edits an entry in the 'pairs' table.
	"""
	form_fields = ['customer_name', 'cl_pair', 'circuit_type', 'circuit_id', 
		'customer_phone', 'uo_pair', 'notes']
	entry = []
	error = None

	if request.method == 'POST':
		for field in form_fields:
			entry.append(request.form[field])

		entry_id = db.get_entry_id(DB_CURSOR, entry[1], entry[5])

		# If admin is logged in, edit the entry
		if 'username' in session:
			user = "admin"
			db.edit_entry(DB_CURSOR, entry_id, entry, user)
			db.db_commit(DATABASE)
			return redirect(url_for("admin"))

		# Else, did a centlink user submit the entry? Was it less than 60 
		#	minutes ago?
		else:
			if db.get_entry_author(DB_CURSOR, entry_id) == 'centlink':
				time_now = datetime.now()
				time_delta = timedelta(hours=1)
				time_entry = db.get_entry_timestamp(DB_CURSOR, entry_id)

				if time_entry > (time_now - time_delta):
					user = "centlink"
					db.edit_entry(DB_CURSOR, entry_id, entry, user)
					db.db_commit(DATABASE)
					__send_email("edit", entry)
					return redirect(url_for("index"))

				else:
					error = ("**ERROR: This entry is over 1 hour old and " + 
						"cannot be edited by standard users.**")
					session['error'] = error
					return redirect(url_for("index"))
			else:
				error = ("**ERROR: An admin created the entry and cannot be " + 
					"edited by standard users.**")
				session['error'] = error
				return redirect(url_for("index"))
	else:
		error = '**ERROR: An error occurred processing your request.**'
		session['error'] = error

	return redirect(url_for("index"))


if __name__ == "__main__":
	import uuid
	app.secret_key = cfg.KEY
	app.debug = cfg.DEBUG
	app.logger.setLevel(logging.DEBUG)
	app.run(port=cfg.PORT)