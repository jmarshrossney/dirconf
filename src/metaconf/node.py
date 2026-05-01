import dataclasses
import warnings
from collections.abc import Callable
from os import PathLike
from pathlib import Path

from .handler import HandlerFactory, infer_handler_from_path, parse_handler


@dataclasses.dataclass
class Node:
    """A dataclass representing a file or directory."""

    path: str | PathLike
    """A path corresponding to a file or directory."""
    handler: HandlerFactory
    """A [`HandlerFactory`][metaconf.handler.HandlerFactory] that produces valid
       handlers with `read` and `write` methods for the file or directory."""

    def __post_init__(self) -> None:
        # Parsing + validation of path
        if self.path is None:
            raise ValueError("`path` must not be None")
        path = Path(self.path)
        # Do not allow absolute paths or paths include '..'
        if path.expanduser().is_absolute():
            warnings.warn(
                "Absolute paths are not recommended and may not be "
                "supported in future "
                "(https://github.com/jmarshrossney/metaconf/issues/13). "
                "Did you mean to do this?",
                stacklevel=2,
            )
        elif ".." in path.parts:
            raise ValueError("`path` should not include '..'")

        self.path = path
        self.handler = parse_handler(self.handler)


def dict_to_node(path_and_handler: dict) -> Node:
    """Converts a valid dict to a [`Node`][metaconf.node.Node]."""
    return Node(**path_and_handler)


def path_to_node(
    handler: HandlerFactory | None = None,
) -> Callable[[str | PathLike | dict[str, str | PathLike]], Node]:
    """Returns a transform that attempts to construct a Node from a path only."""

    def transform(path: str | PathLike | dict[str, str | PathLike]) -> Node:
        # Might pass argument as single-element dict {"path": path}
        if isinstance(path, dict):
            path_str: str | PathLike = path["path"]
        else:
            path_str = path

        return Node(path=path_str, handler=handler or infer_handler_from_path(path_str))

    return transform


def to_node(input: Node | dict | str | PathLike) -> Node:
    """A catch-all transform that produces a Node."""
    if isinstance(input, Node):
        return input
    if isinstance(input, dict) and "handler" in input:
        return dict_to_node(input)
    if isinstance(input, str | PathLike):
        return path_to_node()(input)
    if isinstance(input, dict):
        return path_to_node()(input)

    raise TypeError(f"Unable to create Node object from input of type {type(input)}")
