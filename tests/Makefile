RESOURCES := $(shell find ../expyrimenter -name \*.py)

tests:
	@PYTHONPATH="$$PYTHON_PATH:.." python3 -m unittest

help:
	@echo '     no target: runs tests target'
	@echo '         tests: run all tests in this folder'
	@echo '      coverage: prints coverage report'
	@echo ' coverage-html: generates report in coverage_html/index.html'
	@echo '         clean: deletes coverage data and html report'

coverage: .coverage
	@PREFIX="$$(readlink -e $$(dirname $$(pwd)))/expyrimenter/"; \
	        coverage report \
	        | sed "s|$$PREFIX||" \
	        | sed "s/^-\{$${#PREFIX}\}//" \
	        | sed "s/^Name \{$${#PREFIX}\}/Name/" \
	        | sed "s/^TOTAL \{$${#PREFIX}\}/TOTAL/"

.coverage: test_*.py $(RESOURCES)
	@-rm -f .coverage
	@export PYTHONPATH="$$PYTHON_PATH:.."; \
	for test in test_*.py; do \
		coverage run -a $$test; \
	done

coverage-html: .coverage
	coverage html
	@echo 'Output in coverage_html/index.html'

clean:
	rm -rf coverage_html .coverage __pycache__
