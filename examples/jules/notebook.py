# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "f90nml",
#     "marimo",
#     "numpy",
#     "xarray",
# ]
# ///

import marimo

__generated_with = "0.23.5"
app = marimo.App(app_title="Configuration of the JULES land surface model")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Configuration of the JULES land surface model
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Some background about the JULES land surface model.

    Documentation is available at [https://jules-lsm.github.io](https://jules-lsm.github.io).
    """)
    return


@app.cell
def _():
    from os import PathLike
    from pathlib import Path

    import config_foundry

    return Path, PathLike, config_foundry


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Namelists
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The JULES executable is run by passing the path to a directory containing these namelists as its sole positional argument,

    ```sh
    jules.exe /path/to/namelists/
    ```

    where `namelists/` must contain _all_ of the required namelists files,

    ```txt
    namelists/
    ├── ancillaries.nml
    ├── crop_params.nml
    ├── drive.nml
    ├── fire.nml
    ├── imogen.nml
    ├── initial_conditions.nml
    ├── jules_deposition.nml
    ├── jules_hydrology.nml
    ├── jules_irrig.nml
    ├── jules_prnt_control.nml
    ├── jules_radiation.nml
    ├── jules_rivers.nml
    ├── jules_snow.nml
    ├── jules_soil_biogeochem.nml
    ├── jules_soil.nml
    ├── jules_surface.nml
    ├── jules_surface_types.nml
    ├── jules_vegetation.nml
    ├── jules_water_resources.nml
    ├── model_environment.nml
    ├── model_grid.nml
    ├── nveg_params.nml
    ├── output.nml
    ├── pft_params.nml
    ├── prescribed_data.nml
    ├── science_fixes.nml
    ├── timesteps.nml
    ├── triffid_params.nml
    └── urban.nml
    ```

    !!! note
        There is no freedom to use different file names for the namelist files; they must be present exactly as specified above.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We will make use of the [`f90nml`](https://f90nml.readthedocs.io/en/latest/) Python package[^1] for reading and writing namelist files.

    [^1]: Marshall Ward. (2019). marshallward/f90nml: Version 1.1.2 (v1.1.2). Zenodo. [https://doi.org/10.5281/zenodo.3245482](https://doi.org/10.5281/zenodo.3245482)
    """)
    return


@app.cell
def _(PathLike):
    import f90nml

    class NamelistFileHandler:
        def read(self, path: str | PathLike) -> dict:
            """Read a Fortran namelist file and return a dict of its contents."""
            data = f90nml.read(path)
            return data.todict()

        def write(
            self, path: str | PathLike, data: dict, *, overwrite_ok: bool = False
        ) -> None:
            """Write a dict to a Fortran namelist file."""
            f90nml.write(data, path, force=overwrite_ok)

    return (NamelistFileHandler,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We now construct a `MetaConfig`-based Handler for a namelists directory, in which each `Node` corresponds to a single `.nml` file with a fixed path and handler.
    """)
    return


@app.cell
def _(NamelistFileHandler, config_foundry):
    _jules_namelists = [
        "ancillaries",
        "crop_params",
        "drive",
        "fire",
        "imogen",
        "initial_conditions",
        "jules_deposition",
        "jules_hydrology",
        "jules_irrig",
        "jules_prnt_control",
        "jules_radiation",
        "jules_rivers",
        "jules_snow",
        "jules_soil_biogeochem",
        "jules_soil",
        "jules_surface",
        "jules_surface_types",
        "jules_vegetation",
        "jules_water_resources",
        "model_environment",
        "model_grid",
        "nveg_params",
        "output",
        "pft_params",
        "prescribed_data",
        "science_fixes",
        "timesteps",
        "triffid_params",
        "urban",
    ]

    NamelistDirectoryHandler = config_foundry.make_metaconfig(
        cls_name="NamelistDirectoryHandler",
        spec={
            name: {"path": f"{name}.nml", "handler": NamelistFileHandler}
            for name in _jules_namelists
        },
    )
    return (NamelistDirectoryHandler,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This produces a subclass of `MetaConfig` which is instantiated without any arguments.
    """)
    return


@app.cell
def _(NamelistDirectoryHandler):
    # @output: namelists_handler_print
    namelists_handler = NamelistDirectoryHandler()

    print(namelists_handler)
    return (namelists_handler,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can now use this handler to read an entire namelists directory into a Python dict.
    """)
    return


@app.cell
def _(namelists_handler):
    # @output: namelists_keys
    namelists_dict = namelists_handler.read("config/namelists")

    namelists_dict.keys()
    return (namelists_dict,)


@app.cell
def _(namelists_dict):
    # @output: drive_namelist
    namelists_dict["drive"]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Input data
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ascii input data
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    JULES also requires

    We can use `numpy` to read and write floating point ascii data.
    """)
    return


@app.cell
def _(PathLike, config_foundry):
    from typing import TypedDict
    import numpy

    @config_foundry.filter(write=lambda path, data, **_: not path.is_absolute())
    @config_foundry.filter_missing()
    class AsciiFileHandler:
        class AsciiData(TypedDict):
            values: numpy.ndarray
            comment: str

        def read(self, path: str | PathLike) -> AsciiData:
            comment_lines = []
            num_lines = 0
            with open(path, "r") as file:
                for line in file:
                    line = line.strip()
                    if line.startswith(("#", "!")):
                        comment_lines.append(line)
                        continue
                    elif line:  # comment line
                        num_lines = num_lines + 1
                        if num_lines > 1:
                            break
            comment = "\n".join(comment_lines)  # non-empty line
            values = numpy.loadtxt(str(path), comments=("#", "!"))
            if num_lines == 1:
                assert values.ndim == 1  # we just need to know if it's >1
                values = values.reshape(1, -1)
            return self.AsciiData(values=values, comment=comment)

        def write(
            self, path: str | PathLike, data: AsciiData, *, overwrite_ok: bool = False
        ) -> None:
            numpy.savetxt(
                str(path),
                data["values"],
                fmt="%.5f",
                header=data["comment"],
                comments="#",
            )  # NOTE: Unfortunately numpy.loadtxt/savetxt does not correctly round-trip  # single-row data. We need to catch it here and add an extra dimension.

    return (AsciiFileHandler,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### NetCDF input data
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We will use `xarray` to read and write input data in the `netCDF` format.
    """)
    return


@app.cell
def _(Path, PathLike, config_foundry):
    import xarray

    @config_foundry.filter(
        read=lambda path: not path.is_absolute(),
        write=lambda path, data, **_: not path.is_absolute(),
    )
    @config_foundry.filter_missing()
    class NetcdfFileHandler:
        def read(self, path: str | PathLike) -> xarray.Dataset:
            dataset = xarray.load_dataset(path)
            return dataset

        def write(
            self,
            path: str | PathLike,
            data: xarray.Dataset,
            *,
            overwrite_ok: bool = False,
        ) -> None:
            if not overwrite_ok and Path(path).is_file():
                raise FileExistsError(f"There is already a file at '{path}'")
            data.to_netcdf(path)

    return (NetcdfFileHandler,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Putting it together
    """)
    return


@app.cell
def _(AsciiFileHandler, NetcdfFileHandler, config_foundry):
    config_foundry.register_handler("ascii", AsciiFileHandler, [".txt", ".dat", ".asc"])
    config_foundry.register_handler("netcdf", NetcdfFileHandler, [".nc", ".cdf"])
    return


@app.cell
def _(AsciiFileHandler, config_foundry):
    InputFilesConfig = config_foundry.make_metaconfig(
        cls_name="InputFilesConfig",
        spec={
            "initial_conditions": {
                "handler": AsciiFileHandler,
            },
            "tile_fractions": {
                "handler": AsciiFileHandler,
            },
            "driving_data": {},
        },
    )
    return (InputFilesConfig,)


@app.cell
def _(NamelistDirectoryHandler, config_foundry):
    JulesConfigHandler = config_foundry.make_metaconfig(
        cls_name="JulesConfigHandler",
        spec={
            "inputs": {},  # we will fix this upon instantiation
            "namelists": {"handler": NamelistDirectoryHandler},  # fully fixed
        },
    )
    return (JulesConfigHandler,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reading an existing configuration
    """)
    return


@app.cell
def _():
    # @output: tree_config
    from config_foundry.utils import tree

    print(tree("./config"))
    return (tree,)


@app.cell
def _(InputFilesConfig, JulesConfigHandler):
    # @output: handler_print
    handler = JulesConfigHandler(
        namelists="namelists",
        inputs={
            "path": "inputs",
            "handler": lambda: InputFilesConfig(
                initial_conditions="initial_conditions.dat",
                tile_fractions="tile_fractions.dat",
                driving_data="Loobos_1997.dat",
            ),
        },
    )

    print(handler)
    return (handler,)


@app.cell
def _(handler):
    # @output: config_keys
    config = handler.read("./config")

    config.keys()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reading with netcdf
    """)
    return


@app.cell
def _(InputFilesConfig, JulesConfigHandler):
    # @output: netcdf_handler_print
    handler_1 = JulesConfigHandler(
        namelists="namelists",
        inputs={
            "path": "inputs",
            "handler": lambda: InputFilesConfig(
                initial_conditions="initial_conditions.dat",
                tile_fractions="tile_fractions.dat",
                driving_data="Loobos_1997.nc",
            ),
        },
    )
    print(handler_1)
    return (handler_1,)


@app.cell
def _(handler_1):
    # @output: netcdf_config_keys
    config_1 = handler_1.read("./config")
    config_1.keys()
    return (config_1,)


@app.cell
def _(config_1):
    # @output: driving_data_display
    config_1["inputs"]["driving_data"]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Writing a new configuration
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We will now demonstrate how to generate a new JULES configuration based on a modification of the existing one.

    Here we will use `tempfile` to write to a temporary directory that is automatically deleted upon exit from the context handler. In practice one would create a persistent directory.
    """)
    return


@app.cell
def _(handler_1, tree):
    # @output: write_new_config
    import tempfile

    config_2 = handler_1.read("./config")
    print(
        "current output period: ",
        config_2["namelists"]["output"]["jules_output_profile"]["output_period"],
    )
    config_2["namelists"]["output"]["jules_output_profile"]["output_period"] = 3600
    with tempfile.TemporaryDirectory() as temp_dir:
        handler_1.write(temp_dir, config_2)
        print(tree(temp_dir))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""

    """)
    return


if __name__ == "__main__":
    app.run()
