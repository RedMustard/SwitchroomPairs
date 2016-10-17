PYVENV = pyvenv-3.4

install:
	$(PYVENV) env
	make env/bin/pip
	(. env/bin/activate; pip3.4 install -r requirements.txt)


env/bin/pip:
	echo ""
	(. env/bin/activate; curl https://bootstrap.pypa.io/get-pip.py | python)

dist:
	pip freeze >requirements.txt