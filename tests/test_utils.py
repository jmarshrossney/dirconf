import tempfile
from pathlib import Path

import pytest

from metaconf.utils import dict_to_namespace, namespace_to_dict, switch_dir, tree


class TestSwitchDir:
    def test_switch_to_existing_dir(self):
        original = Path.cwd()
        with switch_dir(tempfile.gettempdir()):
            assert Path.cwd() != original
            assert Path.cwd() == Path(tempfile.gettempdir())
        assert Path.cwd() == original

    def test_switch_to_nonexistent_dir_raises(self):
        with pytest.raises(FileNotFoundError):
            switch_dir("/nonexistent/path/xyz")

    def test_switch_to_file_raises(self):
        with tempfile.NamedTemporaryFile() as f:  # noqa: SIM117
            with pytest.raises(NotADirectoryError), switch_dir(f.name):
                pass


class TestTree:
    def test_tree_on_directory(self, tmp_path):
        (tmp_path / "a.txt").write_text("hello")
        (tmp_path / "b.txt").write_text("world")
        result = tree(str(tmp_path))
        assert "a.txt" in result
        assert "b.txt" in result

    def test_tree_nested(self, tmp_path):
        (tmp_path / "sub").mkdir()
        (tmp_path / "sub" / "c.txt").write_text("deep")
        result = tree(str(tmp_path))
        assert "sub" in result
        assert "c.txt" in result


class TestDictToNamespace:
    def test_simple_dict(self):
        ns = dict_to_namespace({"a": 1, "b": "hello"})
        assert ns.a == 1
        assert ns.b == "hello"

    def test_nested_dict(self):
        ns = dict_to_namespace({"outer": {"inner": 42}})
        assert ns.outer.inner == 42


class TestNamespaceToDict:
    def test_round_trip(self):
        original = {"a": 1, "b": "hello", "c": {"d": 42}}
        ns = dict_to_namespace(original)
        result = namespace_to_dict(ns)
        assert result == original
