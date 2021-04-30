clean:
	rm -rf build dist
	find . -name '*.pyc' -exec rm \{\} \;

test:
	openfisca-run-test tests --country-package openfisca_france --extensions openfisca_france_local
