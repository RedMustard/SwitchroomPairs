#
#  Compile web-site assets
#
#  Largely this means concatenating and 'minifying' some javascript and css 
#  assets to reduce browser load time (fewer http requests). 
#

# Configuration options
#
# Edit to use most recent version of Pyvenv on platform  
# PYVENV = pyvenv-3.4


# A locally installed copy of browserify
# BROWSERIFY=static/js/node_modules/browserify/bin/cmd.js

#
#  The files we generate at build-time
# 
# DERIVED = static/js/*.min.js


SOURCES = db.py pairApp.py config.py

env:
	$(PYVENV)  env
	(.  env/bin/activate; pip install -r requirements.txt)


run:
	$(SOURCES) env
	( . env/bin/activate; python3 pairApp.py )

# all:
# 	(cd static/js; make all)

##
## Install in a new environment:
##     We need to rebuild the Python environment to match
##     Everything is straightforward EXCEPT that we need 
##     to work around an ubuntu bug in pyvenv on ix
##     
# install:
# 	$(PYVENV)  env
# 	(.  env/bin/activate; pip install -r requirements.txt)
	# (cd static/js ; npm install)
	# $(BROWSERIFY) static/js/adDatabaseTable.js >static/js/adDatabaseTable.min.js
	# $(BROWSERIFY) static/js/logTable.js >static/js/logTable.min.js
	# $(BROWSERIFY) static/js/modalDelete.js >static/js/modalDelete.min.js
	# $(BROWSERIFY) static/js/modalEdit.js >static/js/modalEdit.min.js
	# $(BROWSERIFY) static/js/modalEditStd.js >static/js/modalEditStd.min.js
	# $(BROWSERIFY) static/js/modalSubmit.js >static/js/modalSubmit.min.js
	# $(BROWSERIFY) static/js/stdDatabaseTable.js >static/js/stdDatabaseTable.min.js
	# $(BROWSERIFY) static/js/bootstrap-table/extras/export/bootstrap-table-export.js >static/js/bootstrap-table/extras/export/bootstrap-table-export.min.js
	# $(BROWSERIFY) static/js/bootstrap-table/extras/print/bootstrap-table-print.js >static/js/bootstrap-table/extras/print/bootstrap-table-print.min.js

# env/bin/pip: env/bin/activate
# 	echo ""
# 	(. env/bin/activate; curl https://bootstrap.pypa.io/get-pip.py | python)


dist:
	pip freeze >requirements.txt

##
## Make a clean start 
##
clean:	
	rm -rf *.pyc
	rm -rf __pycache__

##
## Recipes for components 
## 

## Combine and minify javascript files with browserify
%.min.js:	%.js
	$(BROWSERIFY) $< > $@
