# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "f90nml",
#     "marimo",
#     "netcdf4",
#     "numpy",
#     "xarray",
# ]
# ///

import marimo

__generated_with = "0.23.5"
app = marimo.App(app_title="Configuration of the JULES land surface model")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Configuration of the JULES land surface model
    """)
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    JULES (Joint UK Land Environment Simulator) is a community land surface model developed by the UK Centre for Ecology & Hydrology (UKCEH) and the Met Office.
    It simulates the exchange of energy, water, momentum, carbon and other trace gases between the land surface and the atmosphere.[^1] [^2]

    [^1]: Best, M. J., et al. (2011). The Joint UK Land Environment Simulator (JULES), model description – Part 1: Energy and water fluxes, Geosci. Model Dev., 4, 677–699, [10.5194/gmd-4-677-2011](https://doi.org/10.5194/gmd-4-677-2011).

    [^2]: Clark, D. B., et al. (2011). The Joint UK Land Environment Simulator (JULES), model description – Part 2: Carbon fluxes and vegetation dynamics, Geosci. Model Dev., 4, 701–722, [10.5194/gmd-4-701-2011](https://doi.org/10.5194/gmd-4-701-2011).


    Documentation is available at [https://jules-lsm.github.io](https://jules-lsm.github.io).

    !!! note
        This example was developed and tested using version 7.9 of JULES.
        It's possible that the way JULES is configured will change in future.
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

    Fortran namelists are a standard mechanism for passing configuration parameters to a program.
    They consist of named blocks (`&block_name ... /`) containing key-value pairs. JULES uses
    roughly 30 separate namelist files to organize its many parameters by physical process
    (e.g., soil, snow, vegetation) and model component (e.g., output, grid, timesteps).
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
    We will make use of the [`f90nml`](https://f90nml.readthedocs.io/en/latest/) Python package[^3] for reading and writing namelist files.

    [^3]: Marshall Ward. (2019). marshallward/f90nml: Version 1.1.2 (v1.1.2). Zenodo. [10.5281/zenodo.3245482](https://doi.org/10.5281/zenodo.3245482)
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
    namelists_dict = namelists_handler.read("config/namelists")

    list(namelists_dict.keys())
    return (namelists_dict,)


@app.cell
def _(namelists_dict):
    namelists_dict["drive"]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The `drive` namelist shown above controls the meteorological forcing data:
    start and end dates, time step, variable names, and the path to the driving data file.
    """)
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

    In addition to namelist files, JULES requires input data such as meteorological forcing
    ("driving") data, initial conditions, and spatial maps like tile fractions. These are
    typically provided as plain-text ASCII files or in the NetCDF format.

    - **Initial conditions** specify the starting state of soil moisture, temperature, and
      other prognostic variables at each grid point.
    - **Tile fractions** define the fractional coverage of each surface type (e.g., broadleaf
      trees, C3 grass, urban) within a grid cell.
    - **Driving data** contains the time series of meteorological variables (temperature,
      precipitation, radiation, etc.) that force the model.

    We can use `numpy` to read and write floating point ASCII data.
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
            with open(path) as file:
                for line in file:
                    line = line.strip()
                    if line.startswith(("#", "!")):
                        comment_lines.append(line)
                        continue
                    elif line:  # non-comment data line
                        num_lines = num_lines + 1
                        if num_lines > 1:
                            break
            comment = "\n".join(comment_lines)  # join all comment header lines
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
            )
            # NOTE: Unfortunately numpy.loadtxt/savetxt does not correctly round-trip
            # single-row data. We need to catch it here and add an extra dimension.

    return (AsciiFileHandler,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### NetCDF input data

    ASCII files (`.dat`, `.txt`) are simple and human-readable, making them suitable for
    small datasets like initial conditions or tile fraction maps. However, for large
    multidimensional time series such as meteorological driving data, the NetCDF format is
    strongly preferred: it is compact, self-describing, and supports metadata and coordinate
    labels natively.

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

    We have now defined handlers for three file types: namelists (via `f90nml`), ASCII data
    (via `numpy`), and NetCDF (via `xarray`). Before composing them into a unified configuration,
    we register the ASCII and NetCDF handlers with `config_foundry` so they can be selected
    automatically by file extension.

    The `@config_foundry.filter` decorator attaches predicates that determine when a handler
    is applicable (e.g., based on path properties). The `@config_foundry.filter_missing()`
    decorator ensures that missing files are handled gracefully rather than raising an error
    immediately.
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
            "driving_data": {},  # handler resolved by file extension at runtime
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
    With the input file handlers defined, we can now compose the top-level `JulesConfigHandler`.
    Note that the `inputs` node uses a lambda factory function rather than a direct handler
    instance. This defers instantiation of `InputFilesConfig` until the handler is constructed,
    allowing us to bind specific file paths at that time. The `namelists` node, by contrast,
    is fully fixed since all namelist file paths are known in advance.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reading an existing configuration
    """)
    return


@app.cell
def _():
    from config_foundry.utils import tree

    print(tree("./config"))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The directory tree above shows the complete JULES configuration layout: a `namelists/`
    directory with all required `.nml` files, and an `inputs/` directory with the driving
    data, initial conditions, and tile fraction files.
    """)
    return


@app.cell
def _(InputFilesConfig, JulesConfigHandler):
    handler_ascii = JulesConfigHandler(
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

    print(handler_ascii)
    return (handler_ascii,)


@app.cell
def _(handler_ascii):
    config_ascii = handler_ascii.read("./config")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reading with netcdf
    """)
    return


@app.cell
def _(InputFilesConfig, JulesConfigHandler):
    handler_netcdf = JulesConfigHandler(
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
    print(handler_netcdf)
    return (handler_netcdf,)


@app.cell
def _(handler_netcdf):
    config_netcdf = handler_netcdf.read("./config")
    return (config_netcdf,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Writing a new configuration

    We will now demonstrate how to generate a new JULES configuration based on a modification
    of the existing one.

    Here we modify the `output_period` parameter in the output namelist from its default value
    to `3600` seconds, which means JULES will write output every hour. We then write the
    modified configuration to a temporary directory using `tempfile`, which is automatically
    cleaned up on exit. In practice you would use a persistent directory.
    """)
    return


@app.cell
def _(config_netcdf, handler_netcdf):
    import tempfile

    print(
        "current output period: ",
        config_netcdf["namelists"]["output"]["jules_output_profile"]["output_period"],
    )
    config_netcdf["namelists"]["output"]["jules_output_profile"]["output_period"] = 3600
    with tempfile.TemporaryDirectory() as temp_dir:
        handler_netcdf.write(temp_dir, config_netcdf)
    return


if __name__ == "__main__":
    app.run()
