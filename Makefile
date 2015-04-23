define run_on_sources =
find expyrimenter tests -name "*.py" -type f \
| grep -v "^./doc/" | grep -v "^./ipython/" | xargs $(1)
endef

dev_pep8:
	$(call run_on_sources,pep8)

dev_flake8:
	$(call run_on_sources,flake8)

dev_yapf:
	$(call run_on_sources,yapf -i)

dev_clean:
	git clean -dxf
