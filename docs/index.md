# Home

`dirconf` is a Python tool for declaratively specifying configuration directory structures, and constructing Python `dict` representations of their contents.

I wrote this because I sometimes have to work with quite old scientific models that require various configuration files and data inputs in various formats to be present in various locations.
I was (and remain) concerned about how easy it can be to misconfigure certain models without realising, and how common workflows compromise reproducibility.

`dirconf` helps by

1. Allowing the user to describe the structure of a directory representing a valid configuration using Python [dataclasses](https://docs.python.org/3/library/dataclasses.html), and validate real directories against this description.

2. Providing a scaffold for defining consistent read/write mechanisms through which complex, distributed configurations in legacy formats can be mapped to Python `dict`s.

The ability to represent configurations as `dict`s is very useful indeed.
With no extra effort, we can:

- Validate configurations using excellent tools such as [JSON Schema](https://json-schema.org/) and [Pydantic](https://docs.pydantic.dev/).
- Generate new configurations and metadata programmatically, as opposed to copying and editing files by hand or writing shell scripts.

## Installation

`dirconf` is a Python package and thus can be installed using `pip`, or tools such as `uv` and `poetry` that wrap around `pip`.


=== "uv (recommended)"

    ```sh
    uv add dirconf
    ```

=== "pip"

    ```sh
    pip install dirconf
    ```

Currently Python versions equal to or above 3.12 are supported.


## Overview of usage

There are two essential steps for adapting `dirconf` to a specific use-case.

1. **Define handlers** satisfying the `Handler` protocol for each of the paths (files and directories) present in your configuration.
2. **Define the structure of a valid configuration** in terms of its paths and their respective handlers, by subclassing the `DirConfig` class. This is most easily done using the `make_dirconfig` function.

The custom `DirConfig` subclass can then be used to

1. **Read** a configuration from the filesystem into a Python `dict`. 
2. **Write** a configuration `dict` to the filesystem.

These steps are most easily understood through examples. 
To start with, take a look at the [Usage](101.md) section. 
More realistic examples can be found under the 'examples' heading.

All examples are based on self-contained [marimo](https://marimo.io/) notebooks, which can be found [here](https://github.com/jmarshrossney/dirconf/tree/main/examples/).


## Philosophy

`dirconf` contains ~700 lines of code (including docstrings) and has no dependencies beyond the Standard Library.

This is by design.
I have no intention of developing `dirconf` into a more sophisticated tool than it already is.
The aim is that is works seamlessly alongside other tools and packages for parsing and validation, without ever getting in the way or creating conflicts.

With that out of the way, please feel free to raise an [issue](https://github.com/jmarshrossney/dirconf/issues) or make a [pull request](https://github.com/jmarshrossney/dirconf/pulls) to suggest a change or feature.
