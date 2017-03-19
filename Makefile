VERBOSITY?=-vv
PYTYPE?=python
PYVER?=2.7
PYBIN_WITH_VER?=python2.7
VENV=. _venv/bin/activate;
INSTALL_VENV=pip --quiet install virtualenv
CLEANER_CMD=rm -rf _venv/ __pycache__/ *.pyc  *.pyo  *.pyd

.PHONY: setupdev test test2 test3 coverage shippable_test package clean

setupdev: clean
	- if ! $(INSTALL_VENV); then sudo $(INSTALL_VENV); fi
	- $(PYBIN_WITH_VER) -m virtualenv _venv
	- $(VENV) pip install unittest-xml-reporting coverage
	mkdir -p ./shippable/testresults
	mkdir -p ./shippable/codecoverage

test:
	@ echo
	@ $(PYBIN_WITH_VER) --version
	@ echo
	$(VENV) $(PYBIN_WITH_VER) ./run_tests.py $(VERBOSITY)

local_test:
	docker run -it --rm \
		--env="PYBIN_WITH_VER=$(PYBIN_WITH_VER)" \
		-v "$(PWD)":/usr/src/myapp \
		-w /usr/src/myapp \
		"$(PYTYPE):$(PYVER)" make shippable_test

coverage:
	- $(VENV) $(PYBIN_WITH_VER) -m coverage run --timid --branch --omit="_venv/*" ./run_tests.py $(VERBOSITY)
	$(VENV) $(PYBIN_WITH_VER) -m coverage xml -o ./shippable/codecoverage/coverage.xml ./run_tests.py

shippable_test: setupdev coverage test

racket_test: clean
	cd racket && raco pkg install --deps search-auto --link pcsu > /dev/null
	raco test -x -p pcsu

package:
	@ echo "Not implemented yet..."
	@ exit 1

clean:
	- raco pkg remove pcsu > /dev/null
	- rm -rf racket/pcsu/compiled racket/pcsu/doc
