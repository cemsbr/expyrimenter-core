dev_pep8:
	@find expyrimenter tests -name "*.py" -type f \
	    | grep -v "^./doc/" | grep -v "^./ipython/" | xargs pep8

dev_flake8:
	@find expyrimenter tests -name "*.py" -type f \
	    | grep -v "^./doc/" | grep -v "^./ipython/" | xargs flake8

dev_clean:
	git clean -dxf
