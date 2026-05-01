# Metaconf

[![PyPI Version](https://img.shields.io/pypi/v/metaconf)](https://pypi.org/project/metaconf/)
[![Python Version](https://img.shields.io/pypi/pyversions/metaconf)](https://pypi.org/project/metaconf/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://img.shields.io/github/actions/workflow/status/jmarshrossney/metaconf/ci.yml?branch=main&label=CI)](https://github.com/jmarshrossney/metaconf/actions)

---

`metaconf` is a simple tool for the meta-configuration of collections of configuration files, leaning heavily on Python [dataclasses](https://docs.python.org/3/library/dataclasses.html).

I wrote this because I sometimes have to work with quite old scientific models that require various configuration files and data inputs in various formats to be present in various locations.

I was (and remain) concerned about how easy it can be to misconfigure certain models without realising, and how common workflows compromise reproducibility.

`metaconf` helps by

1. Allowing the user to describe the structure of a directory representing a valid configuration, and validate real directories against this description.

2. Facilitating the generation of new configurations and metadata programmatically, in Python, as opposed to copying and editing files by hand or writing shell scripts.

3. Providing a consistent mechanism through which complex, distributed configurations in legacy formats can be validated using excellent tools such as [JSON Schema](https://json-schema.org/) and [Pydantic](https://docs.pydantic.dev/).

For user documentation and examples please visit [https://jmarshrossney.github.io/metaconf/](https://jmarshrossney.github.io/metaconf/).

---

## Installation

Either

```sh
pip install metaconf
```

or

```sh
uv add metaconf
```

or the equivalent command for other package managers (poetry etc).

## Development

Contributions are welcome!

Please open a Pull Request against the `main` branch.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for full details.

