"""Switchroom Pairs Database API

Author: Travis Barnes, Aug 08 2016

This program functions as the API for manipulating the MySQL backend for the 
Switchroom Pairs app.
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


# def connect_database():
	# """
	# """

	# db_connect.close()


def create_database_tables(cursor):
	"""Creates database tables defined in DATABASE_TABLES dictionary.
	"""
	for name, ddl in DATABASE_TABLES.items():
		try:
			print("Creating table {}: ".format(name), end='')
			cursor.execute(ddl)
		
		except sql_con.Error as err:
			if err.errno == sql_con.errorcode.ER_TABLE_EXISTS_ERROR:
				print("already exists.")
			
			else:
				print(err.msg)

		else:
			print("OK")


def db_commit(database):
	"""
	"""
	database.commit()


def insert_entry():
	"""
	"""
	print("\nInserting entry...")

	add_entry = ('''INSERT INTO pairs (
					circuit_id, type, cl_pair, uo_pair, customer, cust_phone, 
					notes, date_added) 
					VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''')

	data_entry1 = ('testCircuitID', 'ISDN', 123, 456, 'John Doe', '541-555-5555',
	 'afdsfffsdfasfd', datetime.now().date())

	db_cursor.execute(add_entry, data_entry1)
	db_commit(db_connect)


def delete_entry(entry_id):
	"""
	"""
	delete_query = ('''DELETE FROM pairs WHERE entry_id = %s''')

	db_cursor.execute(delete_query, (entry_id,))
	db_commit(db_connect)


def edit_entry(entry_id):
	"""
	"""
	return


def get_entry(entry_id):
	"""
	"""
	


def get_full_db():
	"""Retrieves the entire contents of the database."""

	print("\nRetrieving full db...")

	query_database = ('''SELECT * FROM pairs''')

	db_cursor.execute(query_database)

	for (entry_id, circuit_id, circuit_type, cl_pair, uo_pair, customer, 
		cust_phone, notes, date_added) in db_cursor:
		
		print(entry_id, circuit_id, circuit_type, cl_pair, uo_pair, 
			customer, cust_phone, notes, date_added)

	# db_connect.close()
	


if __name__ == "__main__":
	try:
		db_connect = sql_con.connect(**config.sql_config_dictionary)
		db_cursor = db_connect.cursor()

	except sql_con.Error as err:
		if err.errno == sql_con.errorcode.ER_ACCESS_DENIED_ERROR:
			print("Incorrect username or password")

		elif err.errno == sql_con.errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")

		else:
			print(err)

	else:
		print("Connected to database.")
		create_database_tables(db_cursor)

	insert_entry()
	get_full_db()
	print("\nDeleting previously inserted entry...")
	delete_entry(29)
	get_full_db()