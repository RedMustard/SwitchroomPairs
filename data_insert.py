"""Century Link Demarcation & Cross-Connect Data Initialization

This program functions as a method to insert an initial batch of entries
from a CSV file into the database for the University of Oregon/Century Link 
Demarcation & Cross-Connect app.


Make sure to run pairApp.py at least one time before running this script.


The CSV file should contain a header row with the following format:
	Circuit ID, Type, CL Pair, UO Pair, Customer, Customer Phone, Notes

The data for the CSV file should be appear in the same format as the header.
For example, the file should look similar to:
	Circuit ID, Type, CL Pair, UO Pair, Customer, Customer Phone, Notes
	541-555-5555, Tel #, 1501, 302, John Doe, 541-555-5555, This is a test
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
	print("Opening File...")
	file = fileinput.input()
	return file


def parse_csv_data(file):
	"""Parses a CSV file containing a batch of entries.

	Keyword Arguments:
		file - An opened CSV file

	Returns:
		entries - List containing parsed entry data
	"""
	print("Parsing file...")
	na_list = ["NA", "na", "Na", "nA", "N/A", "n/a", "N/A", "n/A"]
	entries = [[0 if i.strip() in na_list else i.strip() for i in 
		line.split(',')[:7]] for line in file]
	
	return entries


if __name__ == "__main__":
	for entry in parse_csv_data(open_file())[1:]:
		date_added = datetime.now().date()
		time_added = datetime.now()
		entry.append(date_added)
		entry.append(time_added)
		entry.append("admin")

		if entry[0] != "":
			print("Inserting entry...")
			db.insert_entry(DB_CURSOR, entry)
			print(entry)
			print("\n")

	db.db_commit(DATABASE)
