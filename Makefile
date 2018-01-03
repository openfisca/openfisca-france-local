clean:
	rm -rf build dist
	find . -name '*.pyc' -exec rm \{\} \;

test:
	openfisca-run-test openfisca_brestmetropole/tests --country-package openfisca_france --extensions openfisca_brestmetropole
