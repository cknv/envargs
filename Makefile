test:
	pytest

publish:
	python setup.py sdist upload
	python setup.py bdist_wheel upload
	rm -fr build dist .egg envargs.egg-info
