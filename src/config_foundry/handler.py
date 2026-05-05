import importlib
import logging
from abc import abstractmethod
from collections import OrderedDict
from collections.abc import Callable
from os import PathLike
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

logger = logging.getLogger(__name__)


@runtime_checkable
class Handler(Protocol):
    """A Protocol for all valid handlers.

    As with any `Protocol`, it is not necessary to subclass `Handler`. However, any
    valid handler must implement the `read` and `write` methods with signatures
    matching the abstract methods given here.

    """

    @abstractmethod
    def read(self, path: str | PathLike) -> Any:
        """Abstract method for reading data from a file or directory."""
        ...

    @abstractmethod
    def write(self, path: str | PathLike, data: Any, *, overwrite_ok: bool) -> None:
        """Abstract method for writing data to a file or directory."""
        ...


type ReadMethod = Callable[..., Any]
"""Type alias for the `read` method of a handler.

Expected signature: `(self, path: str | PathLike) -> Any`
"""

type WriteMethod = Callable[..., None]
"""Type alias for the `write` method of a handler.

Expected signature:
   `(self, path: str | PathLike, data: Any, *, overwrite_ok: bool) -> None`
Note: `Callable` cannot express keyword-only parameters or `self` binding.
The `overwrite_ok` parameter must be passed as a keyword argument at runtime.
"""

type HandlerFactory = Callable[[], Handler]
"""Type alias for a zero-argument callable that returns a Handler."""

handler_registry: OrderedDict = OrderedDict({})


def register_handler(
    name: str, handler: HandlerFactory, extensions: list[str] | None = None
) -> None:
    """Add a handler factory to the registry."""
    if extensions is None:
        extensions = []

    if name in handler_registry:
        logger.warning(
            f"'{name}' already exists in handler registry, and will be overwritten!"
        )

    if not isinstance(name, str):
        raise TypeError(f"handler name must be a string, got {type(name)}")
    if not isinstance(handler(), Handler):
        raise TypeError(f"handler factory must return a Handler, got {type(handler())}")

    if not all(isinstance(ext, str) for ext in extensions):
        raise TypeError("extensions must be a list of strings")
    if not all(ext.startswith(".") for ext in extensions):
        raise ValueError("extensions must start with '.'")

    handler_registry[name] = {
        "handler": handler,
        "extensions": extensions,
    }


def parse_handler(input: str | HandlerFactory) -> HandlerFactory:
    """Returns a `HandlerFactory` given any valid input."""
    if input in handler_registry:
        handler = handler_registry[input]["handler"]
    elif isinstance(input, str):
        module_name, class_name = input.rsplit(".", 1)
        module = importlib.import_module(module_name)
        handler = getattr(module, class_name)
    elif callable(input) and isinstance(input(), Handler):
        handler = input
    else:
        raise TypeError(f"Invalid handler: '{input}'")

    return handler


def infer_handler_from_path(path: str | PathLike) -> HandlerFactory:
    """Infers the desired HandlerFactory based on the file extension."""
    extension = Path(path).suffix
    compatible_handlers = {
        key: val["handler"]
        for key, val in handler_registry.items()
        if extension in val["extensions"]
    }
    if not compatible_handlers:
        raise ValueError(
            f"No handler found for extension '{extension}' in the handler registry."
        )
    if len(compatible_handlers) > 1:
        handler_names = list(compatible_handlers.keys())
        selected = handler_names[-1]
        logger.warning(
            f"Multiple compatible handlers found for extension '{extension}': "
            f"{handler_names}. Selecting '{selected}'."
        )
    return list(compatible_handlers.values())[-1]
