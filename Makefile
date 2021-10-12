clean:
	rm -rf build dist
	find . -name '*.pyc' -exec rm \{\} \;

test:
	openfisca_local_test tests
