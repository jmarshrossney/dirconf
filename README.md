# Config-Foundry

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://img.shields.io/github/actions/workflow/status/jmarshrossney/config-foundry/ci.yml?branch=main&label=CI)](https://github.com/jmarshrossney/config-foundry/actions)
---

`config-foundry` is a Python tool for declaratively specifying what a valid configuration directory looks like.

I wrote this because I sometimes have to work with quite old scientific models that require various configuration files and data inputs in various formats to be present in various locations.
I was (and remain) concerned about how easy it can be to misconfigure certain models without realising, and how common workflows compromise reproducibility.

`config-foundry` helps by

1. Allowing the user to describe the structure of a directory representing a valid configuration, and validate real directories against this description.

2. Facilitating the generation of new configurations and metadata programmatically, in Python, as opposed to copying and editing files by hand or writing shell scripts.

3. Providing a consistent mechanism through which complex, distributed configurations in legacy formats can be validated using excellent tools such as [JSON Schema](https://json-schema.org/) and [Pydantic](https://docs.pydantic.dev/).

Configurations are specified using Python [dataclasses](https://docs.python.org/3/library/dataclasses.html); `config-foundry` has no dependencies beyond the standard library.

For user documentation and examples please visit [https://jmarshrossney.github.io/config-foundry/](https://jmarshrossney.github.io/config-foundry/).

## Installation

```sh
pip install git+https://github.com/jmarshrossney/config-foundry.git
```

or with `uv`:

```sh
uv add git+https://github.com/jmarshrossney/config-foundry.git
```

or the equivalent command for other package managers (poetry etc).

`config-foundry` is not yet on PyPI; install from GitHub for now. Once published, the installation method below will be replaced with `pip install config-foundry`.

## Updating

```sh
pip install --upgrade git+https://github.com/jmarshrossney/config-foundry.git
```

or

```sh
uv sync --upgrade-package config-foundry
```

## Development

Contributions are welcome!

Please open a Pull Request against the `main` branch.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for full details.

## Why `config-foundry`?

A foundry casts objects from moulds.
Similarly, `config-foundry` lets you declare a *mould* — in the form of a dataclass — that describes the shape of a valid configuration directory.
That mould can then be used to capture configurations from the filesystem or cast new ones from data in Python.

This project was originally called `metaconf` ("configuration of configurations"), but the name was taken on PyPI..

