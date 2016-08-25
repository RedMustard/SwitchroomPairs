"""Switchroom Pairs Database API

Author: Travis Barnes, Aug 08 2016

This program functions as the API for manipulating the MySQL backend for the 
University of Oregon Switchroom Pairs app.
"""

from datetime import date, datetime
import config
import mysql.connector as sql_con


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

		print("\nDeleting previous tables...\n")
		try:
			db_cursor.execute('''DROP TABLE `pairs` ''')
			print("Pairs table deleted")
			db_cursor.execute('''DROP TABLE `pairs_audit` ''')
			print("Pairs_audit table deleted")
			db_cursor.execute('''DROP TABLE `members` ''')
			print("Members table deleted\n")
		except:
			print("Error dropping table")


		create_database_tables(database)

		return database


def create_database_tables(database):
	"""Creates database tables defined in DATABASE_TABLES dictionary.

	Keyword Args:
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

	Keyword Args:
		database - A MYSQLConnection object
	"""
	database.commit()


def insert_entry(database, entry):
	"""Inserts an entry into the database.

	Keyword Args:
		entry - List containing strings for each column in the table
	"""
	db_cursor = database.cursor()

	if len(entry) == 7:
		print("\nInserting entry...")
		
		date_added = datetime.now().date()
		entry.append(date_added)

		add_entry = ('''INSERT INTO pairs (
						circuit_id, type, cl_pair, uo_pair, customer, cust_phone, 
						notes, date_added) 
						VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''')

		db_cursor.execute(add_entry, entry)
		db_commit(database)

	elif len(entry) > 7:
		print("Your entry has too many variables")

	elif len(entry) < 7:
		print("Your entry has too few variables")

	else:
		print("An unexpected error occurred")

	# database.close()


def delete_entry(database, entry_id):
	"""Deletes an entry in the database.

	Keyword Args:
		entry_id - The database ID number of the entry
	"""
	db_cursor = database.cursor()

	delete_query = ('''DELETE FROM pairs WHERE entry_id = %s''')

	db_cursor.execute(delete_query, (entry_id,))
	db_commit(database)



def edit_entry(database, entry_id):
	"""Edits an entry in the database.

	Keyword Args:
		entry_id - The database ID number of the entry
	"""
	db_cursor = database.cursor()


def get_entry(database, entry_id):
	"""Returns an entry from the database.

	Keyword Args:
		entry_id - The database ID number of the entry
	"""
	db_cursor = database.cursor()


def get_entry_id(database):
	"""
	"""
	db_cursor = database.cursor()
	

def get_all_entries(database):
	"""Retrieves the entire contents of the database."""
	# database = connect_to_database()
	db_cursor = database.cursor()

	print("\nRetrieving full db...")

	query_database = ('''SELECT * FROM pairs''')

	db_cursor.execute(query_database)

	return db_cursor

	# for (entry_id, circuit_id, circuit_type, cl_pair, uo_pair, customer, 
	# 	cust_phone, notes, date_added) in db_cursor:
		
	# 	print(entry_id, circuit_id, circuit_type, cl_pair, uo_pair, 
	# 		customer, cust_phone, notes, date_added)

	# database.close()
	


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



















	# try:
	# 	db_connect = sql_con.connect(**config.sql_config_dictionary)
	# 	db_cursor = db_connect.cursor()

	# except sql_con.Error as err:
	# 	if err.errno == sql_con.errorcode.ER_ACCESS_DENIED_ERROR:
	# 		print("Incorrect username or password")

	# 	elif err.errno == sql_con.errorcode.ER_BAD_DB_ERROR:
	# 		print("Database does not exist")

	# 	else:
	# 		print(err)

	# else:
	# 	print("Connected to database.")
	# 	create_database_tables(db_cursor)

# 	insert_entry()
	# get_full_db()
# 	print("\nDeleting previously inserted entry...")
# 	# delete_entry(29)
# 	get_full_db()