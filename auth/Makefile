.PHONY: test test-e2e test-unit test-coverage clean

# Run all tests
test:
	poetry run pytest -v

# Run only e2e tests
test-e2e:
	poetry run pytest -v -m e2e

# Run only unit tests
test-unit:
	poetry run pytest -v -m unit

# Run tests with coverage report
test-coverage:
	poetry run pytest --cov=src --cov-report=term-missing --cov-report=html

# Clean up test artifacts
clean:
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage