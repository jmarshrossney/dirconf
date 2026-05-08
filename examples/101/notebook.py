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

    We will demonstrate basic usage of `dirconf` using a simple configuration containing a [YAML](https://en.wikipedia.org/wiki/YAML) file called `config.yml` and a [CSV](https://en.wikipedia.org/wiki/Comma-separated_values) file called `data.csv`.

    A concrete instance of this configuration already exists in the `./basic` directory.
    """)
    return


@app.cell
def _():
    from dirconf.utils import tree

    tree("./basic")
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
    ### Subclassing `DirConfig`

    The next step is to specify a valid configuration in terms of its files and handlers.

    To do this we will use the `make_dirconfig` function, which produces a subclass of `DirConfig` whose fields correspond to the two required files.
    """)
    return


@app.cell
def _(CsvFileHandler, YamlFileHandler):
    from dirconf import make_dirconfig

    BasicDirConfig = make_dirconfig(
        cls_name="BasicDirConfig",
        spec={
            "config": {"path": "config.yml", "handler": YamlFileHandler},
            "data": {"path": "data.csv", "handler": CsvFileHandler},
        },
    )
    return BasicDirConfig, make_dirconfig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Working with instances of `DirConfig`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### String representation

    Instances of `DirConfig` have a convenient string representation derived from `DirConfig.tree`.
    """)
    return


@app.cell
def _(BasicDirConfig):
    dirconfig = BasicDirConfig()
    dirconfig
    return (dirconfig,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Validating directories

    Before reading or writing configurations, you can validate that a directory contains the expected file structure using the `validate` method. This checks that all expected files exist and are readable without actually reading their contents.

    The `strict` flag controls the behavior on failure: when `True` (the default), a `ValidationError` is raised; when `False`, a `ValidationResult` is always returned (truthy if valid, falsy if issues found).
    """)
    return


@app.cell
def _(dirconfig):
    dirconfig.validate("./basic")
    return


@app.cell
def _(dirconfig):
    import tempfile as _tempfile

    with _tempfile.TemporaryDirectory() as empty_dir:
        validation_result = dirconfig.validate(empty_dir, strict=False)

    validation_result
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Reading configurations

    Once a `DirConfig` is instantiated, configurations are read into a `dict` by passing a path to a configuration directory into the `read` method.
    """)
    return


@app.cell
def _(dirconfig):
    basic_config = dirconfig.read("./basic")
    basic_config
    return (basic_config,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Writing configurations

    In-memory configurations can be written to the filesystem using the `write` method.

    For the purpose of illustration we will modify the configuration, write it to a temporary directory, then read it back in to check that the modified config is as expected.
    """)
    return


@app.cell
def _(basic_config, dirconfig):
    import tempfile

    # Modify the 'a' parameter
    basic_config["config"]["params"]["a"] = -1.0

    # Write to a temporary directory, and check it's worked
    with tempfile.TemporaryDirectory() as _temp_dir:
        dirconfig.write(_temp_dir, basic_config)
        dirconfig.validate(_temp_dir, strict=False)
        reread_basic_config = dirconfig.read(_temp_dir)

    reread_basic_config
    return (tempfile,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Accessing the nodes

    Keep in mind that classes derived from `DirConfig` are essentially [dataclasses](https://docs.python.org/3/library/dataclasses.html) whose fields are instances of `Node` (itself a dataclass!).
    As such, the usual way of accessing dataclass fields applies.
    """)
    return


@app.cell
def _(dirconfig):
    import dataclasses

    dirconfig_as_dict = {}

    for field in dataclasses.fields(dirconfig):
        node = getattr(dirconfig, field.name)

        node_as_dict = {}

        for node_field in dataclasses.fields(node):
            node_as_dict[node_field.name] = getattr(node, node_field.name)

        dirconfig_as_dict[field.name] = node_as_dict

    dirconfig_as_dict
    return (dataclasses,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Or, using `dataclasses.asdict`:
    """)
    return


@app.cell
def _(dataclasses, dirconfig):
    dataclasses.asdict(dirconfig)
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
    ### Nested configs
    """)
    return


@app.cell
def _(tree):
    tree("./nested")
    return


@app.cell
def _(BasicDirConfig, YamlFileHandler, make_dirconfig):
    NestedDirConfig = make_dirconfig(
        cls_name="NestedDirConfig",
        spec={
            "metadata": {"path": "metadata.yml", "handler": YamlFileHandler},
            "inner_config": {"path": "basic", "handler": BasicDirConfig},
        },
    )

    nested_dirconfig = NestedDirConfig()
    nested_dirconfig
    return (nested_dirconfig,)


@app.cell
def _(nested_dirconfig):
    nested_dirconfig.read("./nested")
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
def _(CsvFileHandler, YamlFileHandler, make_dirconfig):
    FlexiblePathDirConfig = make_dirconfig(
        cls_name="FlexiblePathDirConfig",
        spec={
            "config": {"path": "config.yml", "handler": YamlFileHandler},
            "data": {"handler": CsvFileHandler},
        },
    )
    return (FlexiblePathDirConfig,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `FlexiblePathDirConfig` now requires the **relative** path corresponding to `data` to be provided upon instantiation.

    !!! note
        Under the hood, the provided path is transformed into a `Node` in the `__post_init__` dataclass method.
    """)
    return


@app.cell
def _(FlexiblePathDirConfig):
    dirconfig_a = FlexiblePathDirConfig(data="data.csv")
    dirconfig_a
    return


@app.cell
def _(FlexiblePathDirConfig):
    dirconfig_b = FlexiblePathDirConfig(data="observations.csv")
    dirconfig_b
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
    Now we construct a `DirConfig` subclass that leaves `config` entirely unspecified.
    """)
    return


@app.cell
def _(CsvFileHandler, make_dirconfig):
    VariableDirConfig = make_dirconfig(
        cls_name="VariableDirConfig",
        spec={
            "config": {},
            "data": {"path": "data.csv", "handler": CsvFileHandler},
        },
    )
    return (VariableDirConfig,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can now instantiate the class by passing a dict containing both the path and the handler.
    """)
    return


@app.cell
def _(JsonFileHandler, VariableDirConfig):
    variable_dirconfig = VariableDirConfig(
        config={"path": "config.json", "handler": JsonFileHandler}
    )
    variable_dirconfig
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
    from dirconf import register_handler

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
def _(VariableDirConfig):
    lazy_variable_dirconfig = VariableDirConfig(
        config={"path": "config.json", "Handler": "json"}
    )
    lazy_variable_dirconfig
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
def _(VariableDirConfig):
    dirconfig_yaml = VariableDirConfig(config="config.yml")
    dirconfig_yaml
    dirconfig_yaml.read("./basic")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we load the same configuration with a `.json` config file.
    """)
    return


@app.cell
def _(VariableDirConfig):
    dirconfig_json = VariableDirConfig(config="config.json")
    dirconfig_json
    dirconfig_json.read("./basic_json")
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
    from dirconf.filter import filter_missing

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
def _(CsvFileHandler, DummyHandler, YamlFileHandler, make_dirconfig):
    DirConfigWithOptional = make_dirconfig(
        cls_name="DirConfigWithOptional",
        spec={
            "config": {"path": "config.yml", "handler": YamlFileHandler},
            "data": {"path": "data.csv", "handler": CsvFileHandler},
            "optional": {"path": "optional.file", "handler": DummyHandler},
        },
    )
    return (DirConfigWithOptional,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's try to read the usual configuration
    """)
    return


@app.cell
def _(DirConfigWithOptional):
    dirconfig_with_optional = DirConfigWithOptional()
    config_with_optional = dirconfig_with_optional.read("./basic")
    return config_with_optional, dirconfig_with_optional


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
def _(config_with_optional, dirconfig_with_optional, tempfile):
    with tempfile.TemporaryDirectory() as _temp_dir:
        dirconfig_with_optional.write(_temp_dir, config_with_optional)
        _val_result = dirconfig_with_optional.validate(_temp_dir, strict=False)

    _val_result
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
    from dirconf.filter import filter_read

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
def _(PotentiallyLargeFileHandler, make_dirconfig, tree):
    DirConfigWithLarge = make_dirconfig(
        cls_name="DirConfigWithLarge",
        spec={
            "a": {"handler": PotentiallyLargeFileHandler},
            "b": {"handler": PotentiallyLargeFileHandler},
            "c": {"handler": PotentiallyLargeFileHandler},
        },
    )
    tree("./sizes")
    dirconfig_with_large = DirConfigWithLarge(a="small.csv", b="big.csv", c="huge.csv")
    config_with_large = dirconfig_with_large.read("./sizes")
    config_with_large
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Skipping absolute paths
    """)
    return


@app.cell
def _(CsvFileHandler, YamlFileHandler, make_dirconfig):
    from dirconf.filter import filter

    @filter(
        read=lambda path: not path.is_absolute(),
        write=lambda path, data, **_: not path.is_absolute(),
    )
    class SaferCsvFileHandler(CsvFileHandler):
        pass

    DirConfigWithAbsPath = make_dirconfig(
        cls_name="DirConfigWithAbsPath",
        spec={
            "config": {"path": "config.yml", "handler": YamlFileHandler},
            "data": {"path": "data.csv", "handler": SaferCsvFileHandler},
            "big_data": {
                "path": "/path/to/shared/data.csv",
                "handler": SaferCsvFileHandler,
            },
        },
    )
    dirconfig_with_abs_path = DirConfigWithAbsPath()
    dirconfig_with_abs_path
    return (dirconfig_with_abs_path,)


@app.cell
def _(dirconfig_with_abs_path):
    config_with_abs_path = dirconfig_with_abs_path.read("./basic/")
    config_with_abs_path
    return (config_with_abs_path,)


@app.cell
def _(config_with_abs_path, dirconfig_with_abs_path, tempfile):
    with tempfile.TemporaryDirectory() as _temp_dir:
        dirconfig_with_abs_path.write(_temp_dir, config_with_abs_path)
        _val_result = dirconfig_with_abs_path.validate(_temp_dir, strict=False)

    _val_result
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Generating metadata

    In this example, we will read an incomplete configuration from `./basic`, and only upon `write` will we inject metadata into the configuration.
    """)
    return


@app.cell
def _(CsvFileHandler, YamlFileHandler, filter_missing, make_dirconfig):
    DirConfigWithMeta = make_dirconfig(
        cls_name="DirConfigWithMeta",
        spec={
            "config": {"path": "config.yml", "handler": YamlFileHandler},
            "data": {"path": "data.csv", "handler": CsvFileHandler},
            "metadata": {
                "path": "metadata.csv",
                "handler": filter_missing()(CsvFileHandler),
            },
        },
    )
    dirconfig_with_meta = DirConfigWithMeta()
    config_with_meta = dirconfig_with_meta.read("./basic")
    config_with_meta
    return config_with_meta, dirconfig_with_meta


@app.cell
def _(config_with_meta, dirconfig_with_meta, tempfile):
    config_with_meta["metadata"] = [
        ["created_at", "2024-01-01"],
        ["version", "1.0"],
        ["source", "notebook"],
    ]

    with tempfile.TemporaryDirectory() as _temp_dir:
        dirconfig_with_meta.write(_temp_dir, config_with_meta)
        dirconfig_with_meta.validate(_temp_dir, strict=False)
        complete_config = dirconfig_with_meta.read(_temp_dir)

    complete_config["metadata"]
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
    ## Config Validation

    A primary motivation for reading file-based configurations into Python dicts is to enable validation using Python tooling.

    Here we demonstrate how to validate the configuration dict returned by `read` using [Pydantic](https://docs.pydantic.dev/).
    """)
    return


@app.cell
def _():
    from pydantic import BaseModel

    class ParamsModel(BaseModel):
        a: float
        b: float
        c: float

    class ConfigModel(BaseModel):
        id: str
        params: ParamsModel
        init_state: list[float]
        switch: bool

    return (ConfigModel,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can now validate the 'basic' configuration from earlier:
    """)
    return


@app.cell
def _(basic_config):
    basic_config
    return


@app.cell
def _(ConfigModel, basic_config):
    validated_config = ConfigModel(**basic_config["config"])
    validated_config
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If the configuration contains invalid data, Pydantic will raise a clear validation error:
    """)
    return


@app.cell
def _(ConfigModel):
    from pydantic import ValidationError

    try:
        ConfigModel(
            id=123,
            params={"a": "not a float", "b": 2.0, "c": 3.0},
            init_state=[0, 0, 0],
            switch=True,
        )
        msg = "Success"
    except ValidationError as e:
        msg = e

    msg
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    !!! tip
        You can integrate validation directly into your workflow by wrapping the `read` method:

        ```python
        def read_validated(dirconfig_instance, path):
            dirconfig_dict = dirconfig_instance.read(path)
            dirconfig_dict["config"] = ConfigModel(**dirconfig_dict["config"]).model_dump()
            return dirconfig_dict
        ```

        This ensures that every time you load a configuration, it is automatically validated against your Pydantic model.
    """)
    return


if __name__ == "__main__":
    app.run()
