# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "pyyaml",
# ]
# ///

import marimo

__generated_with = "0.23.5"
app = marimo.App(app_title="Usage")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Usage
    """)
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Basic Usage

    #### A simple configuration

    We will demonstrate basic usage of `config-foundry` using a simple configuration containing a [YAML](https://en.wikipedia.org/wiki/YAML) file called `config.yml` and a [CSV](https://en.wikipedia.org/wiki/Comma-separated_values) file called `data.csv`.

    A concrete instance of this configuration already exists in the `./basic` directory.
    """)
    return


@app.cell
def _():
    from config_foundry.utils import tree

    print(tree("./basic"))
    return (tree,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Defining handlers

    We first need to define two handlers that implement `read` and `write` for the two files that make up a configuration.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### YAML handler
    """)
    return


@app.cell
def _():
    from os import PathLike

    import yaml

    class YamlFileHandler:
        def read(self, path: str | PathLike) -> dict:
            with open(path) as file:
                contents = yaml.safe_load(file)
            return contents

        def write(
            self, path: str | PathLike, data: dict, *, overwrite_ok: bool = False
        ) -> None:
            with open(path, mode="w" if overwrite_ok else "x") as file:
                yaml.safe_dump(data, file, sort_keys=False)

    return PathLike, YamlFileHandler


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's quickly test that `read` works:
    """)
    return


@app.cell
def _(YamlFileHandler):
    YamlFileHandler().read("./basic/config.yml")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### CSV handler
    """)
    return


@app.cell
def _(PathLike):
    import csv

    class CsvFileHandler:
        def read(self, path: str | PathLike) -> list[list[float]]:
            data = []
            with open(path) as file:
                reader = csv.reader(file)
                for row in reader:
                    data.append(row)
            return data

        def write(
            self,
            path: str | PathLike,
            data: list[list[float]],
            *,
            overwrite_ok: bool = False,
        ) -> None:
            with open(path, mode="w" if overwrite_ok else "x") as file:
                writer = csv.writer(file)
                for row in data:
                    writer.writerow(row)

    return (CsvFileHandler,)


@app.cell
def _(CsvFileHandler):
    CsvFileHandler().read("./basic/data.csv")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Subclassing `ConfigSchema`

    The next step is to specify a valid configuration in terms of its files and handlers.

    To do this we will use the `make_config_schema` function, which produces a subclass of `ConfigSchema` whose fields correspond to the two required files.
    """)
    return


@app.cell
def _(CsvFileHandler, YamlFileHandler):
    from config_foundry import make_config_schema

    ConfigHandler = make_config_schema(
        cls_name="ConfigHandler",
        spec={
            "config": {"path": "config.yml", "handler": YamlFileHandler},
            "data": {"path": "data.csv", "handler": CsvFileHandler},
        },
    )
    return ConfigHandler, make_config_schema


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Working with instances of `ConfigSchema`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### String representation

    Instances of `ConfigSchema` have a convenient string representation derived from `ConfigSchema.tree`.
    """)
    return


@app.cell
def _(ConfigHandler):
    handler = ConfigHandler()
    print(handler)
    return (handler,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Reading configurations

    Once a `ConfigSchema` is instantiated, configurations are read into a `dict` by passing a path to a configuration directory into the `read` method.
    """)
    return


@app.cell
def _(handler):
    config_dict = handler.read("./basic")
    config_dict
    return (config_dict,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Writing configurations

    In-memory configurations can be written to the filesystem using the `write` method.

    For the purpose of illustration we will modify the configuration, write it to a temporary directory, then read it back in to check that the modified config is as expected.
    """)
    return


@app.cell
def _(config_dict, handler, tree):
    import tempfile

    # Modify the 'a' parameter
    config_dict["config"]["params"]["a"] = -1.0

    # Write to a temporary directory, and check it's worked
    with tempfile.TemporaryDirectory() as _temp_dir:
        handler.write(_temp_dir, config_dict)
        print(tree(_temp_dir))

        reread_config_dict = handler.read(_temp_dir)

    reread_config_dict
    return (tempfile,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Accessing the nodes

    Keep in mind that classes derived from `ConfigSchema` as essentially [dataclasses](https://docs.python.org/3/library/dataclasses.html) whose fields are instances of `Node` (itself a dataclass!).
    As such, the usual way of accessing dataclass fields applies.
    """)
    return


@app.cell
def _(handler):
    import dataclasses

    for field in dataclasses.fields(handler):
        node = getattr(handler, field.name)
        print(f"{field.name}:\n\t{type(node)}\n\t{node.path}\n\t{node.handler}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    !!! tip
        In the vast majority of situations (that I an think of) directly manipulating the nodes, paths or handlers after instantiation would be unnecessary.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Advanced Usage
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Nesting configurations within other configurations
    """)
    return


@app.cell
def _(tree):
    print(tree("./nested"))
    return


@app.cell
def _(ConfigHandler, YamlFileHandler, make_config_schema):
    NestedHandler = make_config_schema(
        cls_name="NestedHandler",
        spec={
            "metadata": {"path": "metadata.yml", "handler": YamlFileHandler},
            "inner_config": {"path": "basic", "handler": ConfigHandler},
        },
    )

    nested_handler = NestedHandler()
    print(nested_handler)
    return (nested_handler,)


@app.cell
def _(nested_handler):
    nested_handler.read("./nested")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Variable paths

    Often configurations are flexible regarding paths and file names.

    Here we do not fix the file name for `data` - perhaps it differs between configurations (e.g. based on a path set in `config.yml`).
    """)
    return


@app.cell
def _(CsvFileHandler, YamlFileHandler, make_config_schema):
    UnspecifiedPathHandler = make_config_schema(
        cls_name="UnspecifiedPathHandler",
        spec={
            "config": {"path": "config.yml", "handler": YamlFileHandler},
            "data": {"handler": CsvFileHandler},
        },
    )
    return (UnspecifiedPathHandler,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `UnspecifiedPathHandler` now requires the **relative** path corresponding to `data` to be provided upon instantiation.

    !!! note
        Under the hood, the provided path is transformed into a `Node` in the `__post_init__` dataclass method.
    """)
    return


@app.cell
def _(UnspecifiedPathHandler):
    handler_a = UnspecifiedPathHandler(data="data.csv")
    handler_b = UnspecifiedPathHandler(data="observations.csv")

    print(handler_a)
    print(handler_b)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Variable paths and handlers

    If we can delay specifying a path until instantiation, we may also want to delay the specification of the handler.

    Let's say that the `config` node can be either a YAML or JSON file.

    We first define a JSON handler.
    """)
    return


@app.cell
def _(PathLike):
    import json

    class JsonFileHandler:
        def read(self, path: str | PathLike) -> dict:
            with open(path) as file:
                contents = json.load(file)
            return contents

        def write(
            self, path: str | PathLike, data: dict, *, overwrite_ok: bool = False
        ) -> None:
            with open(path, mode="w" if overwrite_ok else "x") as file:
                json.dump(data, file)

    return (JsonFileHandler,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we construct a `ConfigSchema` subclass that leaves `config` entirely unspecified.
    """)
    return


@app.cell
def _(CsvFileHandler, make_config_schema):
    VariableHandler = make_config_schema(
        cls_name="VariableHandler",
        spec={
            "config": {},
            "data": {"path": "data.csv", "handler": CsvFileHandler},
        },
    )
    return (VariableHandler,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can now instantiate the class by passing a dict containing both the path and the handler.
    """)
    return


@app.cell
def _(JsonFileHandler, VariableHandler):
    variable_handler = VariableHandler(
        config={"path": "config.json", "handler": JsonFileHandler}
    )
    print(variable_handler)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Registering handlers

    To save some typing, we can register handlers to a handler registry.
    """)
    return


@app.cell
def _(JsonFileHandler, YamlFileHandler):
    from config_foundry import register_handler

    register_handler("yaml", YamlFileHandler, extensions=[".yml", ".yaml"])
    register_handler("json", JsonFileHandler, extensions=[".json"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we can refer to handlers by their key in the registry.
    """)
    return


@app.cell
def _(VariableHandler):
    lazy_variable_handler = VariableHandler(
        config={"path": "config.json", "Handler": "json"}
    )
    print(lazy_variable_handler)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Handler inference

    More usefully, we leave the handler to be inferred by the file extension.

    We first load the original 'basic' configuration.
    """)
    return


@app.cell
def _(VariableHandler):
    yaml_handler = VariableHandler(config="config.yml")
    print(yaml_handler)
    yaml_handler.read("./basic")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we load the same configuration with a `.json` config file.
    """)
    return


@app.cell
def _(VariableHandler):
    json_handler = VariableHandler(config="config.json")
    print(json_handler)
    json_handler.read("./basic_json")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Handling missing files

    Up to this point, attempting to call `read` on a missing file or directory will result in an error being thrown.

    In some situations we might want to handle missing data differently. Sometimes certain files are optional, and one is simply happy to skip over them if they do not exist.

    Another use-case would be reading from a 'template' configuration that is incomplete, requiring additional data which we will merge into the Python `dict` before writing the complete configuration to a new location.
    """)
    return


@app.cell
def _(PathLike):
    from config_foundry.filter import filter_missing

    @filter_missing(warn=True)
    class DummyHandler:
        def read(self, path: str | PathLike) -> None:
            print("`read` has been called.")

        def write(
            self, path: str | PathLike, data: None, *, overwrite_existing: bool = False
        ) -> None:
            print("`write` has been called.")

    return DummyHandler, filter_missing


@app.cell
def _(CsvFileHandler, DummyHandler, YamlFileHandler, make_config_schema):
    ConfigHandlerWithOptional = make_config_schema(
        cls_name="ConfigHandlerWithOptional",
        spec={
            "config": {"path": "config.yml", "handler": YamlFileHandler},
            "data": {"path": "data.csv", "handler": CsvFileHandler},
            "optional": {"path": "optional.file", "handler": DummyHandler},
        },
    )
    return (ConfigHandlerWithOptional,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's try to read the usual configuration
    """)
    return


@app.cell
def _(ConfigHandlerWithOptional):
    handler_with_optional = ConfigHandlerWithOptional()
    config_with_optional = handler_with_optional.read("./basic")
    return config_with_optional, handler_with_optional


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We see that `DummyHandler.read` was never called, and instead we are shown a warning that `read('optional.file')` was filtered out by a test (which we are shown the code for). Note that this warning can be disabled by setting `warn=False` (the default) in `filter_missing`.

    The configuration `dict` contains an entry corresponding to the `optional` node, but it has a special _sentinel_ value, `MISSING`.
    """)
    return


@app.cell
def _(config_with_optional):

    config_with_optional
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now let's see what happens when we try to write the incomplete configuration.
    """)
    return


@app.cell
def _(config_with_optional, handler_with_optional, tempfile, tree):
    with tempfile.TemporaryDirectory() as _temp_dir:
        handler_with_optional.write(_temp_dir, config_with_optional)
        print(tree(_temp_dir))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Once again we are shown a warning, which explains both what was filtered out and why, and `DummyHandler.write` was never called.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Filtering

    The `filter_missing` decorator is a special case of a more general `filter` class decorator, which allows the user to specify tests which trigger the 'missingness' behaviour if they fail.

    We will now briefly run through some illustrative examples where filtering comes in useful.

    #### Skipping large files

    As an example, we will consider a situation where one or more of the files in a configuration is very large, and we want to avoid loading them into memory.

    This is easy to achieve by combining the already-familiar `filter_missing` with a custom filter applied to the `read` method, using `filter_read`.

    We will demonstrate this by creating a subclass of `CsvFileHandler` from earlier.
    """)
    return


@app.cell
def _(CsvFileHandler, PathLike, filter_missing):
    from config_foundry.filter import filter_read

    @filter_missing()
    class PotentiallyLargeFileHandler(CsvFileHandler):
        @filter_read(
            test=lambda path: str(path) not in ["big.csv", "huge.csv"],
            label="skip large files",
        )
        def read(self, path: str | PathLike) -> None:
            return super().read(path)

        def write(
            self, path: str | PathLike, data: None, *, overwrite_existing: bool = False
        ) -> None:
            return super().write(path, data, overwrite_existing=overwrite_existing)

    return (PotentiallyLargeFileHandler,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It should not be difficult to see why this works, but the following demonstrates it explicitly.
    """)
    return


@app.cell
def _(PotentiallyLargeFileHandler, make_config_schema, tree):
    ConfigHandlerWithLarge = make_config_schema(
        cls_name="ConfigHandlerWithLarge",
        spec={
            "a": {"handler": PotentiallyLargeFileHandler},
            "b": {"handler": PotentiallyLargeFileHandler},
            "c": {"handler": PotentiallyLargeFileHandler},
        },
    )
    print(tree("./sizes"))
    handler_with_large = ConfigHandlerWithLarge(
        a="small.csv", b="big.csv", c="huge.csv"
    )
    config_with_large = handler_with_large.read("./sizes")
    config_with_large
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Skipping absolute paths
    """)
    return


@app.cell
def _(CsvFileHandler, YamlFileHandler, make_config_schema):
    from config_foundry.filter import filter

    @filter(
        read=lambda path: not path.is_absolute(),
        write=lambda path, data, **_: not path.is_absolute(),
    )
    class SaferCsvFileHandler(CsvFileHandler):
        pass

    ConfigHandlerWithAbsPath = make_config_schema(
        cls_name="ConfigHandlerWithAbsPath",
        spec={
            "config": {"path": "config.yml", "handler": YamlFileHandler},
            "data": {"path": "data.csv", "handler": SaferCsvFileHandler},
            "big_data": {
                "path": "/path/to/shared/data.csv",
                "handler": SaferCsvFileHandler,
            },
        },
    )
    handler_with_abs_path = ConfigHandlerWithAbsPath()
    print(handler_with_abs_path)
    return (handler_with_abs_path,)


@app.cell
def _(handler_with_abs_path):
    config_with_abs_path = handler_with_abs_path.read("./basic/")
    config_with_abs_path
    return (config_with_abs_path,)


@app.cell
def _(config_with_abs_path, handler_with_abs_path, tempfile, tree):
    with tempfile.TemporaryDirectory() as _temp_dir:
        handler_with_abs_path.write(_temp_dir, config_with_abs_path)
        print(tree(_temp_dir))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Generating metadata

    In this example, we will read an incomplete configuration from `./basic`, and only upon `write` will we inject metadata into the configuration.
    """)
    return


@app.cell
def _(CsvFileHandler, YamlFileHandler, filter_missing, make_config_schema):
    ConfigHandlerWithMeta = make_config_schema(
        cls_name="ConfigHandlerWithMeta",
        spec={
            "config": {"path": "config.yml", "handler": YamlFileHandler},
            "data": {"path": "data.csv", "handler": CsvFileHandler},
            "metadata": {
                "path": "metadata.csv",
                "handler": filter_missing()(CsvFileHandler),
            },
        },
    )
    handler_with_meta = ConfigHandlerWithMeta()
    config_with_meta = handler_with_meta.read("./basic")
    config_with_meta
    return config_with_meta, handler_with_meta


@app.cell
def _(config_with_meta, handler_with_meta, tempfile, tree):
    config_with_meta["metadata"] = [
        ["created_at", "2024-01-01"],
        ["version", "1.0"],
        ["source", "notebook"],
    ]

    with tempfile.TemporaryDirectory() as _temp_dir:
        handler_with_meta.write(_temp_dir, config_with_meta)
        print(tree(_temp_dir))

        reread_config = handler_with_meta.read(_temp_dir)

    reread_config["metadata"]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We replaced the `MISSING` sentinel with actual metadata before calling `write`, so the `filter_missing` test (`data is not MISSING`) passed and the CSV was written normally.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Strategies for validation

    *To do.*
    """)
    return


if __name__ == "__main__":
    app.run()
