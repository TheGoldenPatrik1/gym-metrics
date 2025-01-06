# Set up default variables
DEFAULT_FILE_PATH=$(wildcard *.json)
ARGS = $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))
CMD = panel serve src/main.py --dev --args -i

# Define the default target
default: run

# Default target: handle arguments and start the web server
run:
	@if [ -n "$(ARGS)" ]; then \
		FILE_PATH=$$(find . -name $(ARGS) | head -n 1); \
		if [ -z "$$FILE_PATH" ]; then \
			echo "Error: file '$(ARGS)' not found!"; \
			exit 1; \
		else \
			echo "Running on '$$FILE_PATH'..."; \
			$(CMD) $$FILE_PATH; \
		fi \
	else \
		FILE_PATH=$$(find . -name *.json | head -n 1); \
		if [ -z "$$FILE_PATH" ]; then \
			echo "No JSON files found!"; \
			exit 1; \
		else \
			echo "Running on '$$FILE_PATH'..."; \
			$(CMD) "$$FILE_PATH"; \
		fi \
	fi

# Allow passing command-line arguments to the Makefile
.PHONY: run

# Prevent make from interpreting arguments as targets
%:
	@:
