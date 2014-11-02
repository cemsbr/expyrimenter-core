all: pypi sign

upload:
	twine upload *.tar.gz*

pypi: pypi-check
	cd ..; ./setup.py sdist

sign:
	gpg --detach-sign -a expyrimenter*.tar.gz

pypi-check:
	cd ..; ./setup.py check

clean:
	rm -f *.tar.gz*
