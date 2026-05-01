import json
import logging
import os
import pathlib
import types
from collections.abc import Iterator

logger = logging.getLogger(__name__)


class switch_dir:
    """Context manager for changing to *existing* directory."""

    def __init__(self, path: str | os.PathLike) -> None:
        self.new = pathlib.Path(path)

        if not self.new.is_dir():
            raise (
                NotADirectoryError(f"{self.new} is not a directory")
                if self.new.exists()
                else FileNotFoundError(f"{self.new} does not exist")
            )

    def __enter__(self):
        logger.debug(f"Switching directory to {self.new}")
        self.old = pathlib.Path.cwd()
        os.chdir(self.new)

    def __exit__(self, etype, value, traceback):
        logger.debug(f"Switching directory back to {self.old}")
        try:
            os.chdir(self.old)
        except FileNotFoundError:
            logger.warning(
                f"Original directory '{self.old}' no longer exists. "
                f"Remaining in '{self.new}'."
            )


def _tree(path: pathlib.Path, prefix: str) -> Iterator[str]:
    blank = "   "
    pipe = "│  "
    tee = "├──"
    elbow = "└──"

    contents = sorted(path.iterdir())
    pointers = [tee] * (len(contents) - 1) + [elbow]

    for pointer, path_ in zip(pointers, contents, strict=False):
        yield prefix + pointer + path_.name

        if path_.is_dir():
            extension = pipe if pointer == tee else blank
            yield from _tree(path_, prefix=prefix + extension)


def tree(path: str | os.PathLike) -> str:
    """
    Constructs a tree-like representation of a directory.

    This is primarily for sanity-checking by comparing the output of
    [`MetaConfig.tree`][metaconf.config.MetaConfig.tree] with an actual
    directory.

    Note:
      This is inspired by [GNU `tree`](https://linux.die.net/man/1/tree) and
      is an adaptation of
      [this stackoverflow answer](https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python)
      by Aaron Hall.
    """
    return str(path) + "\n" + "\n".join(list(_tree(pathlib.Path(path), prefix="")))


def dict_to_namespace(dict_: dict) -> types.SimpleNamespace:
    """Converts a `dict` into a `SimpleNamespace` supporting 'dot' access."""
    return json.loads(
        json.dumps(dict_), object_hook=lambda item: types.SimpleNamespace(**item)
    )


def namespace_to_dict(namespace: types.SimpleNamespace) -> dict:
    """Converts a `SimpleNamespace` back to a `dict`."""
    result = {}
    for key, val in vars(namespace).items():
        if isinstance(val, types.SimpleNamespace):
            result[key] = namespace_to_dict(val)
        else:
            result[key] = val
    return result
