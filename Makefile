
default: test

coverage: chmod_quick
	# Run the test suite with coverage enabled
	nosetests -v --with-coverage --cover-package creo --cover-inclusive --cover-branches

test: chmod_quick
	# Run the test suite
	nosetests

test_quick: chmod_quick
	# Run a quick test suite with coverage enabled
	nosetests -v --stop

chmod:
	# Set the correct permissions for all files
	find . -type d -exec chmod 755 {} \;
	find . -type f -exec chmod 644 {} \;

chmod_quick:
	chmod 644 tests/*

clean: chmod
	# Delete any generated files
	@find . -name "*.py?" | xargs rm -f
	@rm -rf tmp_*

.PHONY: coverage test test_quick chmod chmod_quick clean
