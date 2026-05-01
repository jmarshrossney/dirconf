import pytest

from metaconf.handler import (
    handler_registry,
    infer_handler_from_path,
    parse_handler,
    register_handler,
)


class DummyHandler:
    def read(self, path):
        return {}

    def write(self, path, data, *, overwrite_ok=False):
        pass


class AnotherHandler:
    def read(self, path):
        return {}

    def write(self, path, data, *, overwrite_ok=False):
        pass


@pytest.fixture(autouse=True)
def clean_registry():
    original = handler_registry.copy()
    yield
    handler_registry.clear()
    handler_registry.update(original)


class TestRegisterHandler:
    def test_register_handler(self):
        register_handler("dummy", DummyHandler, extensions=[".txt"])
        assert "dummy" in handler_registry

    def test_register_handler_with_extensions(self):
        register_handler("dummy", DummyHandler, extensions=[".txt", ".csv"])
        assert handler_registry["dummy"]["extensions"] == [".txt", ".csv"]

    def test_register_handler_no_extensions(self):
        register_handler("dummy", DummyHandler)
        assert handler_registry["dummy"]["extensions"] == []

    def test_register_handler_overwrites_existing(self):
        register_handler("dummy", DummyHandler)
        register_handler("dummy", DummyHandler)
        assert "dummy" in handler_registry

    def test_register_handler_invalid_name(self):
        with pytest.raises(TypeError):
            register_handler(123, DummyHandler)  # type: ignore[arg-type]

    def test_register_handler_invalid_factory(self):
        with pytest.raises(TypeError):
            register_handler("bad", lambda: "not a handler")  # type: ignore[arg-type]

    def test_register_handler_invalid_extensions_type(self):
        with pytest.raises(TypeError):
            register_handler("bad", DummyHandler, extensions=[".txt", 123])  # type: ignore[arg-type]

    def test_register_handler_invalid_extensions_prefix(self):
        with pytest.raises(ValueError, match="must start with"):
            register_handler("bad", DummyHandler, extensions=["txt"])


class TestParseHandler:
    def test_parse_from_registry(self):
        register_handler("dummy", DummyHandler)
        handler = parse_handler("dummy")
        assert callable(handler)
        assert isinstance(handler(), DummyHandler)

    def test_parse_from_dotted_string(self):
        import sys
        import types

        module = types.ModuleType("test_dotted_module")
        module.DottedHandler = type(  # type: ignore[attr-defined]
            "DottedHandler",
            (),
            {
                "read": lambda self, path: {},
                "write": lambda self, path, data, *, overwrite_ok=False: None,
            },
        )
        sys.modules["test_dotted_module"] = module
        try:
            handler = parse_handler("test_dotted_module.DottedHandler")
            assert callable(handler)
        finally:
            del sys.modules["test_dotted_module"]

    def test_parse_from_callable(self):
        handler = parse_handler(DummyHandler)
        assert callable(handler)
        assert isinstance(handler(), DummyHandler)

    def test_parse_invalid_handler(self):
        with pytest.raises(TypeError):
            parse_handler(123)  # type: ignore[arg-type]


class TestInferHandlerFromPath:
    def test_infer_handler(self):
        register_handler("txt", DummyHandler, extensions=[".txt"])
        handler = infer_handler_from_path("file.txt")
        assert callable(handler)
        assert isinstance(handler(), DummyHandler)

    def test_infer_no_handler_found(self):
        with pytest.raises(ValueError, match="No handler found"):
            infer_handler_from_path("file.xyz")

    def test_infer_multiple_handlers_warns(self, caplog):
        register_handler("txt_a", DummyHandler, extensions=[".txt"])
        register_handler("txt_b", AnotherHandler, extensions=[".txt"])
        import logging

        with caplog.at_level(logging.WARNING):
            infer_handler_from_path("file.txt")
        assert "Multiple compatible handlers" in caplog.text
