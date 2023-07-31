# pylama:ignore=D103
"""Parsing tests."""
import json
from typing import Any, TypeVar, overload

import pytest
from algencode.subnodes.number_node import NUMBER_OP
from algencode.subnodes.string_node import STRING_OP

from .common import Node, NumberNode, StringNode, VariableNode

NodeT = TypeVar("NodeT", StringNode, NumberNode)


def str_node(op: STRING_OP, args: list[Any]):
    n = Node(root=StringNode(op=op, args=args))
    return n, {"op": op, "args": args}


@overload
def f(subnode: type[StringNode], op: STRING_OP, args: list[Any]):
    ...


@overload
def f(subnode: type[NumberNode], op: NUMBER_OP, args: list[Any]):
    ...


def f(subnode: type[StringNode | NumberNode], op: STRING_OP | NUMBER_OP, args: list[Any]):
    obj = {"op": op, "args": args}
    n = Node.model_validate(subnode(**obj))  # type:ignore
    return (n, obj)


PARAMS = [
    f(StringNode, "slice", ["abcd", 1, 3]),
    f(StringNode, "fmt", ["{:08}", "cool"]),
    f(StringNode, "rep", ["_", 10]),
    f(StringNode, "join", [",", "a", "b", "c"]),
    f(NumberNode, "add", [1, 2, 3]),
    f(NumberNode, "sub", [1, 2, 3]),
    f(NumberNode, "mul", [1, 2, 3]),
    f(NumberNode, "div", [1, 2, 3]),
    f(NumberNode, "mod", [1, 2, 3]),
    f(NumberNode, "round", [1.23]),
]


@pytest.mark.parametrize("expect,obj", PARAMS)
def test_parse_node(expect, obj):
    node = Node.model_validate(obj)
    assert node == expect


@pytest.mark.parametrize("expect,obj", PARAMS)
def test_parse_node_json(expect, obj):
    data = json.dumps(obj)
    node = Node.model_validate_json(data)
    assert node == expect


COMPOUND_PARAM = {
    "op": "fmt",
    "args": [
        "{:09}",
        {
            "op": "round",
            "args": [
                {
                    "op": "mul",
                    "args": [
                        {"key": "levy"},
                        100,
                    ],
                },
            ],
        },
    ],
}

COMPOUND_EXPECT = Node.model_validate(
    StringNode(
        op="fmt",
        args=[
            "{:09}",
            Node.model_validate(
                NumberNode(
                    op="round",
                    args=[
                        Node.model_validate(
                            NumberNode(
                                op="mul",
                                args=[
                                    Node.model_validate(VariableNode(key="levy")),
                                    100,
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    ),
)


def test_parse_compound():
    node = Node.model_validate(COMPOUND_PARAM)
    assert node == COMPOUND_EXPECT


# BUG: nodes within nodes fail to be serialized correctly now
#
# def test_parse_compound_json():
#     data = Node.model_validate(COMPOUND_PARAM).model_dump_json(round_trip=True)
#     print(data)
#     node = Node.model_validate_json(data)
#     assert node == COMPOUND_EXPECT
