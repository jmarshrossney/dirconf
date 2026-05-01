# Contributing

Contributions are welcome! Please open a Pull Request against the `main` branch.

Keep in mind that the overarching goal of this project is to be as simple as possible (while still being useful).

## Getting started

This project uses [`uv`](https://docs.astral.sh/uv/). Install the project and development dependencies with

```sh
uv sync
```

Run the tests with

```sh
uv run pytest
```

Check types with

```sh
uv run pyright
```

Lint and format with

```sh
uv run ruff format && uv run ruff check
```

Consider installing [`pre-commit`](https://pre-commit.com/) so that the pre-commit hooks run before each commit.

```sh
uv tool install pre-commit
```

A [`justfile`](justfile) is provided as a convenience for these common tasks.

## Building the documentation

The documentation is built with [MkDocs](https://www.mkdocs.org/). To build and serve it locally:

```sh
uv run --group examples jupytext --set-formats ipynb,md --execute docs/examples/*/*.md
uv run mkdocs serve
```
