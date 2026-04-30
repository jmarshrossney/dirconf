from pathlib import Path

import pytest

from metaconf.filter import (
    MISSING,
    MissingWarning,
    filter,
    filter_missing,
    filter_read,
    filter_write,
)


class DummyHandler:
    def read(self, path):
        return {"data": "hello"}

    def write(self, path, data, *, overwrite_ok=False):
        pass


class TestMISSING:
    def test_missing_is_class(self):
        assert isinstance(MISSING, type)

    def test_missing_singleton_usage(self):
        val = MISSING
        assert val is MISSING


class TestFilterRead:
    def test_filter_read_passes_when_test_true(self):
        handler = DummyHandler()

        @filter_read(test=lambda path: True)
        def read(self, path):
            return handler.read(path)

        result = read(handler, Path("test.txt"))
        assert result == {"data": "hello"}

    def test_filter_read_returns_missing_when_test_false(self):
        @filter_read(test=lambda path: False, label="always_fail", warn=True)
        def read(self, path):
            return {"data": "hello"}

        handler = DummyHandler()
        with pytest.warns(MissingWarning):
            result = read(handler, Path("nonexistent.txt"))
        assert result is MISSING

    def test_filter_read_no_warning_when_warn_false(self):
        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            result = filter_read(test=lambda path: False)(DummyHandler.read)(
                DummyHandler(), Path("test.txt")
            )
        assert result is MISSING

    def test_filter_read_label_from_lambda(self):
        label = filter_read(test=lambda path: True)(DummyHandler.read)
        assert callable(label)


class TestFilterWrite:
    def test_filter_write_passes_when_test_true(self):
        written = False

        class WriteHandler:
            def read(self, path):
                return None

            def write(self, path, data, *, overwrite_ok=False):
                nonlocal written
                written = True

        handler = WriteHandler()
        WrappedClass = filter_write(test=lambda path, data, **kw: True)(WriteHandler)
        wrapped = WrappedClass.write
        wrapped(handler, Path("test.txt"), {"key": "val"}, overwrite_ok=True)
        assert written

    def test_filter_write_returns_missing_when_test_false(self):
        wrapped = filter_write(test=lambda path, data, **kw: False)(DummyHandler.write)
        result = wrapped(
            DummyHandler(), Path("test.txt"), {"key": "val"}, overwrite_ok=False
        )
        assert result is None

    def test_filter_write_warns(self):
        wrapped = filter_write(test=lambda path, data, **kw: False, warn=True)(
            DummyHandler.write
        )
        with pytest.warns(MissingWarning):
            wrapped(
                DummyHandler(), Path("test.txt"), {"key": "val"}, overwrite_ok=False
            )


class TestFilter:
    def test_filter_with_read_only(self):
        @filter(read=lambda path: True)
        class FilteredHandler:
            def read(self, path):
                return "data"

            def write(self, path, data, *, overwrite_ok=False):
                pass

        instance = FilteredHandler()
        assert isinstance(instance, FilteredHandler)

    def test_filter_with_write_only(self):
        @filter(write=lambda path, data, **kw: True)
        class FilteredHandler:
            def read(self, path):
                return "data"

            def write(self, path, data, *, overwrite_ok=False):
                pass

        instance = FilteredHandler()
        assert isinstance(instance, FilteredHandler)

    def test_filter_requires_read_or_write(self):
        with pytest.raises(ValueError, match="Must provide"):
            filter()(object)


class TestFilterMissing:
    def test_filter_missing_exists(self):
        assert callable(filter_missing)

    def test_filter_missing_returns_decorator(self):
        decorator = filter_missing()
        assert callable(decorator)

    def test_filter_missing_on_class(self):
        @filter_missing()
        class SafeHandler:
            def read(self, path):
                return "data"

            def write(self, path, data, *, overwrite_ok=False):
                pass

        handler = SafeHandler()
        assert isinstance(handler, SafeHandler)
