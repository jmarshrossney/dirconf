from pathlib import Path

import pytest

from metaconf.handler import handler_registry
from metaconf.node import Node, dict_to_node, path_to_node, to_node


class DummyHandler:
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


class TestNode:
    def test_create_node_with_handler_factory(self):
        node = Node(path="test.txt", handler=DummyHandler)
        assert node.path == Path("test.txt")
        assert callable(node.handler)

    def test_create_node_with_relative_path(self):
        node = Node(path="subdir/test.txt", handler=DummyHandler)
        assert node.path == Path("subdir/test.txt")

    def test_create_node_with_pathlib_path(self):
        node = Node(path=Path("test.txt"), handler=DummyHandler)
        assert node.path == Path("test.txt")

    def test_create_node_absolute_path_warns(self):
        with pytest.warns(UserWarning, match="Absolute paths"):
            Node(path="/tmp/test.txt", handler=DummyHandler)

    def test_create_node_with_dots_raises(self):
        with pytest.raises(ValueError, match=r"'..'"):
            Node(path="../etc/passwd", handler=DummyHandler)

    def test_create_node_with_dots_in_parts_raises(self):
        with pytest.raises(ValueError, match=r"'..'"):
            Node(path="subdir/../other", handler=DummyHandler)

    def test_create_node_with_handler_string(self):
        from metaconf.handler import register_handler

        register_handler("dummy", DummyHandler)
        node = Node(path="test.txt", handler="dummy")  # type: ignore[arg-type]
        assert callable(node.handler)

    def test_create_node_with_invalid_handler(self):
        with pytest.raises(TypeError):
            Node(path="test.txt", handler=123)  # type: ignore[arg-type]

    def test_create_node_with_uncallable_handler(self):
        with pytest.raises((TypeError, ValueError)):
            Node(path="test.txt", handler="nonexistent_handler_name_xyz")  # type: ignore[arg-type]


class TestDictToNode:
    def test_dict_to_node(self):
        from metaconf.handler import register_handler

        register_handler("dummy", DummyHandler)
        node = dict_to_node({"path": "test.txt", "handler": "dummy"})
        assert isinstance(node, Node)
        assert node.path == Path("test.txt")


class TestPathToNode:
    def test_path_to_node_with_handler(self):
        transform = path_to_node(handler=DummyHandler)
        node = transform("test.txt")
        assert isinstance(node, Node)
        assert node.path == Path("test.txt")

    def test_path_to_node_infer_handler(self):
        from metaconf.handler import register_handler

        register_handler("txt", DummyHandler, extensions=[".txt"])
        transform = path_to_node()
        node = transform("test.txt")
        assert isinstance(node, Node)

    def test_path_to_node_from_dict(self):
        from metaconf.handler import register_handler

        register_handler("txt", DummyHandler, extensions=[".txt"])
        transform = path_to_node()
        node = transform({"path": "test.txt"})
        assert isinstance(node, Node)
        assert node.path == Path("test.txt")


class TestToNode:
    def test_to_node_from_node(self):
        original = Node(path="test.txt", handler=DummyHandler)
        result = to_node(original)
        assert result is original

    def test_to_node_from_str(self):
        from metaconf.handler import register_handler

        register_handler("txt", DummyHandler, extensions=[".txt"])
        node = to_node("test.txt")
        assert isinstance(node, Node)

    def test_to_node_from_dict_with_handler(self):
        from metaconf.handler import register_handler

        register_handler("dummy", DummyHandler)
        node = to_node({"path": "test.txt", "handler": "dummy"})
        assert isinstance(node, Node)

    def test_to_node_from_dict_without_handler(self):
        from metaconf.handler import register_handler

        register_handler("txt", DummyHandler, extensions=[".txt"])
        node = to_node({"path": "test.txt"})
        assert isinstance(node, Node)

    def test_to_node_invalid_type(self):
        with pytest.raises(TypeError, match="Unable to create Node"):
            to_node(123)  # type: ignore[arg-type]
