"""Century Link Demarcation & Cross-Connect Data Initialization

This program functions as a method to insert an initial batch of entries
from a CSV file into the database for the University of Oregon/Century Link 
Demarcation & Cross-Connect app.

The CSV file should be in the following format:
	Circuit ID, Type, CL Pair, UO Pair, Customer, Customer Phone, Notes
"""

import db, fileinput
from datetime import date, time, datetime, timedelta


DATABASE = db.connect_to_database()
DB_CURSOR = DATABASE.cursor()


def open_file():
	"""Opens a csv files and prepares it to be read.

	Returns:
		file - CSV file ready to be parsed.
	"""
	file = fileinput.input()

	return file



def parse_csv_data(file):
	"""Parses a CSV file containing a batch of entries.

	Returns:
		entries - List containing parsed entry data
	"""
	entries = [[i.strip() for i in line.split(',')[:7]] for line in file]

	return entries


def insert_entry(entry):
	"""Inserts an entry into the database.

	Keyword Arguments:
		cursor - A cursor object for the database to delete from
		entry - List containing strings for each column in the table
	"""

	if len(entry) == 10:
		add_entry = ('''INSERT INTO pairs (
						circuit_id, type, cl_pair, uo_pair, customer, 
						cust_phone, notes, date_added, time_added, user) 
						VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, "admin")''')

		DB_CURSOR.execute(add_entry, entry)
		__insert_entry_audit_insert(DB_CURSOR, entry)

	elif len(entry) > 10:
		print("Your entry has too many variables")

	elif len(entry) < 10:
		print("Your entry has too few variables")

	else:
		print("An unexpected error occurred")




if __name__ == "__main__":
	for entry in parse_csv_data(open_file()):
		date_added = datetime.now().date()
		time_added = datetime.now()
		entry.append(date_added)
		entry.append(time_added)

		if entry[0] != "":
			print(entry)
			print("\n")
