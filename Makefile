# Makefile for Challenge 05: Production Version

.PHONY: test
test:
	@echo "🧪 Running tests for Challenge 02: Production Version"
	@pytest tests/ -v

.PHONY: test-verbose
test-verbose:
	@pytest tests/ -vv -s

.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make test          - Run tests for this challenge"
	@echo "  make test-verbose  - Run tests with detailed output"
