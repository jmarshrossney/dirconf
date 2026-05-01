import json
from pathlib import Path

import pytest

from metaconf import Handler, MetaConfig, make_metaconfig, register_handler
from metaconf.config import _str_is_json, _str_is_path
from metaconf.handler import handler_registry
from metaconf.node import Node


class SimpleHandler:
    def __init__(self):
        self.data = {}

    def read(self, path):
        with open(path) as f:
            return json.load(f)

    def write(self, path, data, *, overwrite_ok=False):
        with open(path, "w" if overwrite_ok else "x") as f:
            json.dump(data, f)


@pytest.fixture(autouse=True)
def clean_registry():
    original = handler_registry.copy()
    yield
    handler_registry.clear()
    handler_registry.update(original)


class TestMetaConfig:
    def test_metaconfig_is_handler(self):
        assert isinstance(MetaConfig(), Handler)

    def test_tree_empty(self):
        mc = MetaConfig()
        result = mc.tree()
        assert result == ""

    def test_tree_with_nodes(self):
        register_handler("simple", SimpleHandler, extensions=[".json"])
        config = make_metaconfig(
            "TestConfig",
            {"a": {"path": "a.json", "handler": "simple"}},
        )
        result = config().tree(details=False)
        assert "a" in result

    def test_str(self):
        register_handler("simple", SimpleHandler, extensions=[".json"])
        config = make_metaconfig(
            "TestConfig",
            {"a": {"path": "a.json", "handler": "simple"}},
        )
        result = str(config())
        assert "TestConfig" in result

    def test_nodes(self):
        register_handler("simple", SimpleHandler, extensions=[".json"])
        config = make_metaconfig(
            "TestConfig",
            {
                "a": {"path": "a.json", "handler": "simple"},
                "b": {"path": "b.json", "handler": "simple"},
            },
        )
        nodes = list(config().nodes())
        assert len(nodes) == 2
        assert all(isinstance(n, Node) for n in nodes)

    def test_read(self, tmp_path):
        register_handler("simple", SimpleHandler, extensions=[".json"])
        (tmp_path / "a.json").write_text('{"key": "value"}')

        config = make_metaconfig(
            "TestConfig",
            {"a": {"path": "a.json", "handler": "simple"}},
        )
        data = config().read(tmp_path)
        assert data == {"a": {"key": "value"}}

    def test_write(self, tmp_path):
        register_handler("simple", SimpleHandler, extensions=[".json"])
        config = make_metaconfig(
            "TestConfig",
            {"a": {"path": "a.json", "handler": "simple"}},
        )
        output_dir = tmp_path / "output"
        config().write(output_dir, {"a": {"key": "value"}})
        assert (output_dir / "a.json").exists()

    def test_write_creates_directory(self, tmp_path):
        register_handler("simple", SimpleHandler, extensions=[".json"])
        config = make_metaconfig(
            "TestConfig",
            {"a": {"path": "a.json", "handler": "simple"}},
        )
        output_dir = tmp_path / "new" / "nested" / "dir"
        config().write(output_dir, {"a": {"key": "value"}})
        assert (output_dir / "a.json").exists()

    def test_call(self):
        register_handler("simple", SimpleHandler, extensions=[".json"])
        config = make_metaconfig(
            "TestConfig",
            {"a": {"path": "a.json", "handler": SimpleHandler}},
        )
        instance = config()
        result = instance()
        assert isinstance(result, type(instance))
        assert result.a.path == instance.a.path  # type: ignore[attr-defined]


class TestMakeMetaconfig:
    def test_from_dict(self):
        register_handler("simple", SimpleHandler, extensions=[".json"])
        config = make_metaconfig(
            "TestConfig",
            {"a": {"path": "a.json", "handler": "simple"}},
        )
        assert issubclass(config, MetaConfig)

    def test_from_json_string(self):
        register_handler("simple", SimpleHandler, extensions=[".json"])
        spec = json.dumps({"a": {"path": "a.json", "handler": "simple"}})
        config = make_metaconfig("TestConfig", spec)
        assert issubclass(config, MetaConfig)

    def test_from_json_file(self, tmp_path):
        register_handler("simple", SimpleHandler, extensions=[".json"])
        spec_file = tmp_path / "spec.json"
        spec_file.write_text(json.dumps({"a": {"path": "a.json", "handler": "simple"}}))
        config = make_metaconfig("TestConfig", spec_file)
        assert issubclass(config, MetaConfig)

    def test_from_path_string(self, tmp_path):
        register_handler("simple", SimpleHandler, extensions=[".json"])
        spec_file = tmp_path / "spec.json"
        spec_file.write_text(json.dumps({"a": {"path": "a.json", "handler": "simple"}}))
        config = make_metaconfig("TestConfig", str(spec_file))
        assert issubclass(config, MetaConfig)

    def test_handler_only(self):
        register_handler("simple", SimpleHandler, extensions=[".json"])
        config = make_metaconfig(
            "TestConfig",
            {"a": {"handler": "simple"}},
        )
        instance = config(a="a.json")  # type: ignore[call-arg]
        assert instance.a.path == Path("a.json")  # type: ignore[attr-defined]

    def test_neither_path_nor_handler(self):
        register_handler("simple", SimpleHandler, extensions=[".json"])
        config = make_metaconfig(
            "TestConfig",
            {"a": {}},
        )
        instance = config(a="a.json")  # type: ignore[call-arg]
        assert instance.a.path == Path("a.json")  # type: ignore[attr-defined]

    def test_path_only_raises(self):
        with pytest.raises(NotImplementedError):
            make_metaconfig("TestConfig", {"a": {"path": "a.json"}})

    def test_unsupported_spec_type(self):
        with pytest.raises(TypeError, match="Unsupported type"):
            make_metaconfig("TestConfig", 123)  # type: ignore[arg-type]


class TestStrIsJson:
    def test_valid_json(self):
        assert _str_is_json('{"key": "value"}')

    def test_invalid_json(self):
        assert not _str_is_json("not json")

    def test_json_array(self):
        assert _str_is_json("[1, 2, 3]")


class TestStrIsPath:
    def test_existing_path(self, tmp_path):
        assert _str_is_path(str(tmp_path))

    def test_nonexistent_relative_path(self):
        assert not _str_is_path("configs/my_config.json")

    def test_nonexistent_absolute_path(self):
        assert _str_is_path("/absolute/path.txt")

    def test_invalid_path_characters(self):
        assert not _str_is_path("not_a_path_xyz<<<<")

    def test_random_string(self):
        assert not _str_is_path("not a path at all!!<>?")
