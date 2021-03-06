File Structure:

SwitchroomPairs														-- Main folder containing all folders and files
	static															-- Folder containing css, images, and js files
		css 														-- Folder containing css files
			bootstrap 												-- Folder containing css files for bootstrap v4 library
				bootstrap.css										-- CSS file for bootstrap library
				bootstrap.css.map									-- CSS file for bootstrap library (if using Sass or Less)

			bootstrap-table 										-- Folder containing css files for bootstrap-table library
				bootstrap-table.css 								-- CSS file for bootstrap-table library
				bootstrap-table.min 								-- Compressed version of bootstrap-table.min

			pairs.css												-- Main CSS file for the app/site
		
		images 														-- Folder containing images
			favicon.ico												-- Favicon for the app/site
			uo-logo.png												-- UO logo used across app/site

		js 															-- Folder containing JavaScript scripts
			bootstrap 												-- Folder containing JS scripts for bootstrap library
				Extras 												-- Folder containing additional features for bootstrap library
					alert.js 										-- JS script to create bootstrap alerts (i.e. error/success messages)
					button.js 										-- JS script to create bootstrap buttons (i.e. submit/edit buttons)
					dropdown.js 									-- JS script to create bootstrap dropdown menus
					modal.js 										-- JS script to create modal dialog prompts (i.e. edit entry window)
					util.js 										-- Dependency for other JS scripts in this folder
				
				bootstrap.js 										-- Main JS script for bootstrap library
				bootstrap.min.js 									-- Compressed version of bootstrap.js

			boostrap-table 											-- Folder containing JS scripts for bootstrap-table library
				extras 												-- Folder containing additional features for bootstrap-table library
					editable										-- Folder containing JS scripts for editable feature
						bootstrap-table-editable.js 				-- Dependency for other bootstrap-table features
						bootstrap-table-editable.min.js  			-- Compressed version of bootstrap-table-editable.js
				
					export											-- Folder containing JS scripts for export feature
						bootstrap-table-export.js 					-- JS script to export contents of a bootstrap-table (i.e export to PDF)
						bootstrap-table-export.min.js 				-- Compressed version of bootstrap-table-export.js
				
					print											-- Folder containing JS scripts for print feature
						bootstrap-table-print.js 					-- JS script to print contents of a bootstrap-table

				bootstrap-table.min.js 								-- Main JS script for bootstrap-table library 

			adDatabaseTable.js 										-- JS script for managing database table on admin.html
			jquery.min.js 											-- Library for JS
			logTable.js 											-- JS script for managing log table on log.html
			modalDelete.js 											-- JS script for managing delete window (delete confirmation)
			modalEdit.js 											-- JS script for managing edit window (edit entry) on admin.html
			modalEditStd.js 										-- JS script for managing edit window (edit entry) on index.html
			modalSubmit.js 											-- JS script for managing submit window (submission confirmation)
			stdDatabaseTable.js 									-- JS script for managing database table on index.html

	templates 														-- Folder containing html files
		account.html												-- HTML page for Admin account settings
		admin.html													-- HTML page for Admin version of app
		index.html													-- HTML page for standard version of app
		log.html													-- HTML page for database log
		login.html													-- HTML page for Admin login
		page_not_found.html											-- HTML page for use when a user tries accessing an unknown HTML page

	app.cgi															-- CGI file for use with running the app on a web server (i.e. Apache)
	BASEconfig.py													-- Python file containing configuration settings for the app (i.e. SQL credentials)
	data_insert.py													-- Python script to insert an initial batch of entries from a CSV file
	db.py															-- Python database API for making changes to a MySQL database
	Makefile														-- Makefile for installing needed components when setting app up on a web server
	pairApp.py														-- Python API for the app (main application file)
	requirements.txt												-- Txt file containing a list of needed components for the app (used by Makefile)
	Setup															-- Instructions for installing and running the app