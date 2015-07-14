
default: coverage

coverage: clean chmod_quick integration
	# Run the test suite with coverage enabled
	nosetests --with-id --with-coverage --cover-inclusive--cover-package creo --cover-branches

test: chmod_quick
	# Run the test suite
	PYTHONWARNINGS=error nosetests

integration:
	PYTHONWARNINGS=error PYTHONPATH=. coverage run -a --branch examples/example_1.py

test_quick: chmod_quick
	# Run a quick test suite with coverage enabled
	nosetests -v --stop

coverage_erase:
	@echo "Deleting previous coverage data"
	@coverage erase

coverage_report:
	coverage report  --omit "*__init__*,tests/*" -m | tee coverage_report_detail.txt
	coverage report  --omit "*__init__*,tests/*" | tee coverage_report_summary.txt

coverage: coverage_erase test integration coverage_report
	@echo "Completed coverage run"

coverage_check:
	coverage report  --omit "*__init__*,tests/*" --fail-under 90

install:
	pip install -r requirements.txt --upgrade
	pip list -o

run:
	cd server; python -Wall manage.py runserver 0.0.0.0:8083

chmod: chmod_quick
	# Set the correct permissions for all files
	# find . -type d -exec chmod 755 {} \;
	# find . -type f -exec chmod 644 {} \;

chmod_quick:
	chmod 644 tests/*

clean: chmod
	# Delete any generated files
	@rm -rf tmp_* step*.txt mark.txt .coverage
	# @find . -name "*.py?" | xargs rm -f


.PHONY: coverage test test_quick chmod chmod_quick clean integration
