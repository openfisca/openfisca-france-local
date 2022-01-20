clean:
	rm -rf build dist
	find . -name '*.pyc' -exec rm \{\} \;

deps:
	pip install --upgrade pip build twine

install-test:
	pip install -e ".[test,excel-reader]"

install: deps
	@# Install OpenFisca-France-Local for development.
	@# `make install` installs the editable version of OpenFisca-France-Local.
	@# This allows contributors to test as they code.
	pip install --editable . --upgrade

build: clean deps
	@# Install OpenFisca-France-Local for deployment and publishing.
	@# `make build` allows us to be be sure tests are run against the packaged version
	@# of OpenFisca-France-Local, the same we put in the hands of users and reusers.
	python -m build
	pip uninstall --yes openfisca-france-local
	find dist -name "*.whl" -exec pip install {} \;

test:
	openfisca_local_test tests
