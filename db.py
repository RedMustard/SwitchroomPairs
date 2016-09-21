"""Switchroom Pairs Database API

Author: Travis Barnes, Aug 08 2016

This program functions as the API for manipulating the MySQL backend for the 
University of Oregon Switchroom Pairs app.
"""

from datetime import date, datetime
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
		date_added DATE NOT NULL
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


def db_commit(database):
	"""Permanently saves any change to the database.

	Keyword Arguments:
		database - A MYSQLConnection object
	"""
	database.commit()


def insert_entry(cursor, entry):
	"""Inserts an entry into the database.

	Keyword Arguments:
		cursor - A cursor object for the database to delete from
		entry - List containing strings for each column in the table
	"""
	if len(entry) == 7:
		print("\nInserting entry...")
		
		date_added = datetime.now().date()
		entry.append(date_added)

		add_entry = ('''INSERT INTO pairs (
						circuit_id, type, cl_pair, uo_pair, customer, cust_phone, 
						notes, date_added) 
						VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''')

		cursor.execute(add_entry, entry)

	elif len(entry) > 7:
		print("Your entry has too many variables")

	elif len(entry) < 7:
		print("Your entry has too few variables")

	else:
		print("An unexpected error occurred")


def delete_entry(cursor, entry_id):
	"""Deletes an entry in the database.

	Keyword Arguments:
		cursor - A cursor object for the database to delete from
		entry_id - The database ID number of the entry to be retrieved
	"""
	delete_query = ('''DELETE FROM pairs WHERE entry_id = %s''')
	cursor.execute(delete_query, (entry_id,))


def edit_entry(cursor, entry_id, entry):
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


def get_entry(cursor, entry_id):
	"""Returns an entry from the database.

	Keyword Arguments:
		cursor - A cursor object for the database to retrieve from
		entry_id - The database ID number of the entry to be retrieved
	"""
	# db_cursor = database.cursor()
	return


def get_entry_id(cursor, cl_pair, uo_pair):
	"""Retrieves an entry ID of an entry based on the Circuit ID, CL Pair, and
		UO Pair.

	Keyword Arguments:
		cursor - A cursor object for the database to retrieve from
		circuit_id - A string containing the Circuit ID
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
		entry_id - The database ID number of the entry to retrieve the timestamp
	
	Returns:
		timestamp - A date object
	"""
	get_time = ('''SELECT date_added FROM pairs WHERE entry_id = %s''')

	cursor.execute(get_time, (entry_id,))

	for entry in cursor:
		timestamp = entry

	return timestamp


def get_used_pairs(cursor):
	"""
	"""
	pairs = []

	get_pairs = ('''SELECT cl_pair, uo_pair FROM pairs''')
	cursor.execute(get_pairs)

	for entry in cursor:
		pairs.append(entry[0])
		pairs.append(entry[1])

	return pairs

def get_db(cursor):
	"""Retrieves the entire contents of the database.
	
	Keyword Arguments:
		cursor - A cursor object for the database to be retrieved 

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


# if __name__ == "__main__":
	
# 	database = connect_to_database()
# 	db_cursor = database.cursor()


# 	entry1 = ["543543535..n", "DSL", "1648", "208", "NTS", "5415555555", "Lorem Ipsum"]
# 	entry2 = ["5412226688", "Tel. #", "1501", "008", "Sam McSamface", "", ""]
# 	entry3 = ["5412226688", "Tel. #", "1501", "008", "Sam McSamface", ""]
# 	entry4 = ["5412226688", "Tel. #", "1501", "008", "Sam McSamface", "", "", ""]

# 	insert_entry(database, entry1)
# 	get_all_entries(database)
# 	print('\n')
# 	insert_entry(database, entry2)
# 	get_all_entries(database)
# 	print('\n')
# 	insert_entry(database, entry3)
# 	get_all_entries(database)
# 	print('\n')
# 	insert_entry(database, entry4)
# 	get_all_entries(database)