_:
  @just --list

# Format and lint the package using ruff, and lint the examples using marimo.
lint:
  ruff format
  ruff check --fix
  marimo check examples/101/notebook.py
  marimo check examples/jules/notebook.py

# Check formatting and lint (for CI, doesn't modify files).
lint-check:
  ruff format --check
  ruff check
  marimo check examples/101/notebook.py
  marimo check examples/jules/notebook.py

# Run the test suite using pytest.
test:
  pytest

# Run tests with coverage report (requires pytest-cov).
test-cov:
  pytest --cov=config_foundry --cov-report=term-missing --cov-fail-under=90

# Run static type checker.
typecheck:
  pyright

# Build the documentation.
docs:
  cd examples/101/ && marimo-md-export notebook.py ../../docs/101.md --sandbox
  cd examples/jules/ && marimo-md-export notebook.py ../../docs/jules.md --sandbox
  zensical build
