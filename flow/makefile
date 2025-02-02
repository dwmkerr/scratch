SHELL:=/bin/bash

default: help

.PHONY: help
help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

.PHONY: run
run: # Run the flow command.
	@./flow.py

.PHONY: test
test: # Run the flow tests.
	python3 ./flow_test.py

.PHONY: install
install: # Install the flow command.
	sudo ln -s -f $$(pwd)/flow.py /usr/local/bin/flow

install-debug: # Install the flow command in debug mode.
	ln -s X X
