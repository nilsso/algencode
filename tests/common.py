"""Common test utilities."""
# pylama:ignore=D103
import pytest

from algencode import Node, Vals
from algencode.subnodes import NumberNode, ProcNode, StringNode, VariableNode
from algencode.types import Json, LiteralNode


def node_test(n: Json, v: Vals, e: str | int):
    __tracebackhide__ = True
    t = Node.parse_obj(n).reduce(v)
    if t != e:
        pytest.fail(f'"{t}" != "{e}"')


__all__ = [
    "Json",
    "LiteralNode",
    "Node",
    "NumberNode",
    "ProcNode",
    "StringNode",
    "Vals",
    "VariableNode",
    "node_test",
]
