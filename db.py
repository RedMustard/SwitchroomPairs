"""Switchroom Pairs Database API

Author: Travis Barnes, Aug 08 2016

This program functions as the API for manipulating the MySQL backend for the 
University of Oregon Switchroom Pairs app.
"""

from datetime import date, time, datetime
import config
import mysql.connector as sql_con
import json


DATABASE_TABLES = {}
DATABASE_TABLES['pairs'] = (
	'''CREATE TABLE pairs (
		entry_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
	   	circuit_id VARCHAR(48) NOT NULL,
		type VARCHAR(24) NOT NULL,
		cl_pair INT(6) NOT NULL,
		uo_pair INT(6) NOT NULL,
		customer VARCHAR(96),
		cust_phone VARCHAR(16),
		notes VARCHAR(1024),
		date_added DATE NOT NULL,
		time_added DATETIME NOT NULL,
		user CHAR(12) NOT NULL
	)''')

DATABASE_TABLES['pairs_audit'] = (
	'''CREATE TABLE pairs_audit (
		entry_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
	   	circuit_id VARCHAR(48) NOT NULL,
		type VARCHAR(24) NOT NULL,
		cl_pair INT(6) NOT NULL,
		uo_pair INT(6) NOT NULL,
		customer VARCHAR(96),
		cust_phone VARCHAR(16),
		notes VARCHAR(1024),
		date_added DATE NOT NULL,
		audit_type VARCHAR(8) NOT NULL,
		audit_date DATE NOT NULL,
		audit_user CHAR(12) NOT NULL
	)''')

DATABASE_TABLES['members'] = (
	'''CREATE TABLE members (
		entry_id INT(11) AUTO_INCREMENT PRIMARY KEY,
		username VARCHAR(10) NOT NULL,
		password VARCHAR(40) NOT NULL
	)''')


def connect_to_database():
	"""Connects to a MYSQL database.
	
	Returns:
		database - A MYSQLConnection object
	"""
	try:
		database = sql_con.connect(**config.sql_config_dictionary)
		db_cursor = database.cursor()

	except sql_con.Error as err:
		if err.errno == sql_con.errorcode.ER_ACCESS_DENIED_ERROR:
			print("Incorrect username or password")

		elif err.errno == sql_con.errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")

		else:
			print(err)

	else:
		print("Connected to database.")

		################## DELETE TABLES #####################
		# print("\nDeleting previous tables...\n")
		# try:
		# 	db_cursor.execute('''DROP TABLE `pairs` ''')
		# 	print("Pairs table deleted")
		# 	db_cursor.execute('''DROP TABLE `pairs_audit` ''')
		# 	print("Pairs_audit table deleted")
		# 	db_cursor.execute('''DROP TABLE `members` ''')
		# 	print("Members table deleted\n")
		# except:
		# 	print("Error dropping table")
		######################################################

		create_database_tables(database)
		

		return database


def create_database_tables(database):
	"""Creates database tables defined in DATABASE_TABLES dictionary.

	Keyword Argumentss:
		database - A MYSQLConnection object
	"""
	db_cursor = database.cursor()

	for name, ddl in DATABASE_TABLES.items():
		try:
			print("Creating table {}: ".format(name), end='')
			db_cursor.execute(ddl)
			
		
		except sql_con.Error as err:
			if err.errno == sql_con.errorcode.ER_TABLE_EXISTS_ERROR:
				print("already exists.")
			
			else:
				print(err.msg)

		else:
			print("OK")

			if name == "members":
				insert_default_member(db_cursor)

	# create_audit_trigger(db_cursor)			


def db_commit(database):
	"""Permanently saves any change to the database.

	Keyword Arguments:
		database - A MYSQLConnection object
	"""
	database.commit()


def insert_default_member(cursor):
	"""Inserts a default member into the members database.
	"""
	username = "admin"
	password = "password"

	member = None

	get_member = ('''SELECT username, password FROM members 
		WHERE username = %s''')
	cursor.execute(get_member, (username,))

	for entry in cursor:
		member = entry
		print(member)

	if member == None:
		member = [username, password]

		print("Inserted default member...")
		insert_member = ('''INSERT INTO members (username, password) 
			VALUES (%s, MD5(%s)) ''')

		cursor.execute(insert_member, member)


def create_audit_trigger(cursor):
	"""
	"""
	insert_trigger = ('''CREATE TRIGGER log_entry_insert AFTER INSERT ON pairs
		FOR EACH ROW
		BEGIN
			INSERT INTO pairs_audit (circuit_id, type, cl_pair, uo_pair,
			customer, cust_phone, notes, date_added, user, audit_type,
			audit_date, audit_user)
			VALUES(NEW.circuit_id, NEW.type, NEW.cl_pair, NEW.uo_pair, 
			NEW.customer, NEW.cust_phone, NEW.notes, NEW.date_added, NEW.user,
			"Insert", NEW.time_added, NEW.user)
		END
		''')
	cursor.executemany(insert_trigger)



def insert_entry(cursor, entry):
	"""Inserts an entry into the database.

	Keyword Arguments:
		cursor - A cursor object for the database to delete from
		entry - List containing strings for each column in the table
	"""
	if len(entry) == 10:
		print("\nInserting entry...")

		add_entry = ('''INSERT INTO pairs (
						circuit_id, type, cl_pair, uo_pair, customer, 
						cust_phone, notes, date_added, time_added, user) 
						VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''')

		cursor.execute(add_entry, entry)
		__insert_entry_audit_insert(cursor, entry)

	elif len(entry) > 10:
		print("Your entry has too many variables")

	elif len(entry) < 10:
		print("Your entry has too few variables")

	else:
		print("An unexpected error occurred")


def __insert_entry_audit_insert(cursor, entry):
	"""Inserts an entry into pairs_audit whenever an insert is made in the 
		pairs table.
	"""
	insert_entry = ('''INSERT INTO pairs_audit (
						circuit_id, type, cl_pair, uo_pair, customer, 
						cust_phone, notes, date_added, audit_type, 
						audit_date, audit_user) 
						VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''')

	cursor.execute(insert_entry, (entry[0], entry[1], entry[2], entry[3], 
		entry[4], entry[5],entry[6],entry[7], "Insert", entry[7], 
		entry[9]))


def delete_entry(cursor, entry_id, user):
	"""Deletes an entry in the database.

	Keyword Arguments:
		cursor - A cursor object for the database to delete from
		entry_id - The database ID number of the entry to be retrieved
	"""
	__delete_entry_audit_insert(cursor, entry_id, user)

	delete_query = ('''DELETE FROM pairs WHERE entry_id = %s''')
	cursor.execute(delete_query, (entry_id,))

	# __delete_entry_audit_insert(cursor, entry_id)


def __delete_entry_audit_insert(cursor, entry_id, user):
	"""Inserts an entry into pairs_audit whenever a delete is made in the 
		pairs table.
	"""
	entry = get_entry(cursor, entry_id)
	print(entry)
	date_now = datetime.now().date()

	insert_entry = ('''INSERT INTO pairs_audit (
						circuit_id, type, cl_pair, uo_pair, customer,
						cust_phone, notes, date_added, audit_type, audit_date,
						audit_user)
						VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''')

	cursor.execute(insert_entry, (entry[0], entry[1], entry[2], entry[3], 
		entry[4], entry[5],entry[6],entry[7], "Delete", date_now, 
		user))


def edit_entry(cursor, entry_id, entry, user):
	"""Edits an entry in the database.

	Keyword Arguments:
		cursor - A cursor object for the database to edit
		entry_id - The database ID number of the entry to be edited
		entry - List containing strings for each column in the table
	"""

	edit_query = ('''UPDATE pairs SET customer = %s, cl_pair = %s, 
		type = %s, circuit_id = %s, cust_phone = %s, uo_pair = %s, 
		notes = %s WHERE entry_id = %s''')

	print("editing entry")
	cursor.execute(edit_query, (entry[0], entry[1], entry[2], entry[3], 
		entry[4], entry[5], entry[6], entry_id))

	__edit_entry_audit_insert(cursor, entry, entry_id, user)


def __edit_entry_audit_insert(cursor, entry, entry_id, user):
	"""Inserts an entry into pairs_audit whenever an update is made in the
		pairs table.
	"""
	date_now = datetime.now().date()
	date_added = get_entry_datestamp(cursor, entry_id)

	insert_entry = ('''INSERT INTO pairs_audit (
		customer, cl_pair, type, circuit_id, cust_phone, uo_pair, notes,
		date_added, audit_type, audit_date, audit_user) 
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''')

	cursor.execute(insert_entry, (entry[0], entry[1], entry[2], entry[3], 
		entry[4], entry[5], entry[6], date_added, "Edit", date_now, user))


def get_entry(cursor, entry_id):
	"""Retrieves an entry from the pairs table with the given entry_id.

	Keyword argument:
		cursor - A cursor object for the database to retrieve from
		entry_id - The ID number of the entry to retrieve

	Returns:
		entry - List containing the entry information.
	"""
	entry = []

	get_entry = ('''SELECT circuit_id, type, cl_pair, uo_pair, customer, 
		cust_phone, notes, date_added FROM pairs WHERE entry_id = %s''')
	cursor.execute(get_entry, (entry_id,))

	for item in cursor:
		entry.append(item)

	return entry[0]


def get_entry_id(cursor, cl_pair, uo_pair):
	"""Retrieves an entry ID of an entry based on the CL Pair, and
		UO Pair.

	Keyword Arguments:
		cursor - A cursor object for the database to retrieve from
		cl_pair - A string containing the CL Pair
		uo_pair - A string containing the UO Pair

	Returns:
		entry_id - The retrieved ID number for the given entry
	"""
	get_id = ('''SELECT entry_id FROM pairs WHERE cl_pair = %s OR 
		uo_pair = %s''')

	cursor.execute(get_id, (cl_pair, uo_pair))

	for entry in cursor:
		entry_id = entry

	return entry_id[0]


def get_entry_timestamp(cursor, entry_id):
	"""Retrieves the insertion timestamp for an entry.

	Keyword Arguments:
		cursor - A cursor object for the database to retrieve from
		entry_id - The ID number of the entry to retrieve the timestamp
	
	Returns:
		timestamp - A time object
	"""
	get_time = ('''SELECT time_added FROM pairs WHERE entry_id = %s''')

	cursor.execute(get_time, (entry_id,))
	for entry in cursor:
		timestamp = entry
	
	return timestamp[0]


def get_entry_datestamp(cursor, entry_id):
	"""Retrieves the insertion datestamp for an entry.

	Keyword arguments:
		cursor - A cursor object for the database to retrieve from
		entry_id - The ID number of the entry to retrieve the datestamp

	Returns:
		datestamp - A date object
	"""
	get_date_added = ('''SELECT date_added FROM pairs WHERE entry_id = %s''')
	cursor.execute(get_date_added, (entry_id,))

	for item in cursor:
		date_added = item

	return date_added[0]


def get_entry_author(cursor, entry_id):
	"""Retrieves the author of a given entry.

	Keyword Arguments:
		cursor - A cursor object for the database to be retrieved from
		entry_id - The database ID number of the entry to retrieve the author

	Returns:
		author - A string containing the author of the entry
	"""
	get_author = ('''SELECT user FROM pairs WHERE entry_id = %s''')

	cursor.execute(get_author, (entry_id,))

	for entry in cursor:
		author = entry

	return author[0]


def get_db(cursor):
	"""Retrieves the entire contents of the 'pairs' database.
	
	Keyword Arguments:
		cursor - A cursor object for the database to be retrieved from

	Returns:
		entries - A list containing each database entry
	"""
	entries = []

	print("\nRetrieving full db...")

	query_database = ('''SELECT circuit_id, type, cl_pair, uo_pair, customer, 
		cust_phone, notes, date_added FROM pairs''')

	cursor.execute(query_database)

	for entry in cursor:
		entries.append(entry)

	return entries


def get_log_db(cursor):
	"""Retrieves the entire contents of the 'pairs_audit' database.

	Keyword Arguments:
		cursor - A cursor object for the database to be retrieved from

	Returns:
		entries - A list containing each database entry
	"""
	entries = []

	print("Retrieving full log db...")
	query_database = ('''SELECT circuit_id, type, cl_pair, uo_pair, customer, 
						cust_phone, notes, date_added, audit_type, 
						audit_date, audit_user FROM pairs_audit''')

	cursor.execute(query_database)

	for entry in cursor:
		entries.append(entry)

	return entries