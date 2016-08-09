"""Switchroom Pairs Database API

Author: Travis Barnes, Aug 08 2016

This program functions as the API for manipulating the MySQL backend for the 
Switchroom Pairs app.
"""

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

# DATABASE_TABLES['pairs_audit'] = (
# 	"CREATE TABLE 'pairs_audit' ("
# 	"	'entry_id' int(11) NOT NULL AUTO_INCREMENT,"
# 	"   'circuit_id' varchar(48) NOT NULL,"
# 	"	'type' varchar(24) NOT NULL,"
# 	"	'cl_pair' int(6) NOT NULL,"
# 	"	'uo_pair' int(6) NOT NULL,"
# 	"	'customer' varchar(96),"
# 	"	'cust_phone' varchar(16),"
# 	"	'notes' varchar(1024),"
# 	"	'date_added' date NOT NULL,"
# 	"	'audit_type' varchar(8) NOT NULL,"
# 	"	'audit_date' date NOT NULL,"
# 	"	'audit_user' char(12) NOT NULL,"
# 	"	PRIMARY KEY ('entry_id')"
# 	") ENGINE=InnoDB")




# else:
# 	db_connect.close()


def create_database():
	"""
	"""
	try:
		db_connect = sql_con.connect(**config.config_dictionary)
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


def create_database_tables(cursor):
	"""
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


def db_commit():
	"""
	"""
	return


def insert_entry(entry):
	"""
	"""
	return


def delete_entry(entry_id):
	"""
	"""
	return


def edit_entry(entry_id):
	"""
	"""
	return


def get_entry(entry_id):
	"""
	"""
	return


def get_full_db():
	"""
	"""
	return
	


if __name__ == "__main__":
	create_database()