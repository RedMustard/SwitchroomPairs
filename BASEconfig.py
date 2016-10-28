"""
Duplicate this file and name 'config.py'.
Then, in the new file, fill in the missing information.
"""

## Local development environment
sql_config_dictionary = {
	'user': 'INSERT DATABASE USERNAME',
	'password': 'INSERT DATABASE PASSWORD',
	'host': '127.0.0.1',
	'database': 'INSERT DATABASE NAME',
	'raise_on_warnings': True
}

PORT=5000 ## Port for Flask server
DEBUG=False ## Development debug mode on or off


##################################
## Generating a strong app key:
##
## 		Run a python interpreter and type the following in:
##			import os
##			os.urandom(24) 
##
KEY='INSERT APP KEY' ## For use with Flask session cookies