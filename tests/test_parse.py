# pylama:ignore=D103
"""Parsing tests."""
import json
import typing

import pytest

from algencode import node


def f(t, op, args):
    n = node.Node(__root__=t(op=op, args=args))
    obj = {
        "op": op,
        "args": args,
    }
    return (n, obj)


PARAMS = [
    f(
        node.StringNode,
        "slice",
        ["abcd", 1, 3],
    ),
    f(
        node.StringNode,
        "fmt",
        ["{:08}", "cool"],
    ),
    f(
        node.StringNode,
        "rep",
        ["_", 10],
    ),
    f(
        node.StringNode,
        "join",
        [",", "a", "b", "c"],
    ),
    f(
        node.NumberNode,
        "add",
        [1, 2, 3],
    ),
    f(
        node.NumberNode,
        "sub",
        [1, 2, 3],
    ),
    f(
        node.NumberNode,
        "mul",
        [1, 2, 3],
    ),
    f(
        node.NumberNode,
        "div",
        [1, 2, 3],
    ),
    f(
        node.NumberNode,
        "mod",
        [1, 2, 3],
    ),
    f(
        node.NumberNode,
        "round",
        [1.23],
    ),
]


@pytest.mark.parametrize("n,obj", PARAMS)
def test_parse_node(n, obj):
    assert n == node.Node.parse_obj(obj)


@pytest.mark.parametrize("n,obj", PARAMS)
def test_parse_node_json(n, obj):
    r = json.dumps(obj)
    assert n == node.Node.parse_raw(r)


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

COMPOUND_EXPECT = node.Node(
    __root__=node.StringNode(
        op="fmt",
        args=[
            "{:09}",
            node.Node(
                __root__=node.NumberNode(
                    op="round",
                    args=[
                        node.Node(
                            __root__=node.NumberNode(
                                op="mul",
                                args=[
                                    node.Node(__root__=node.VariableNode(key="levy")),
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
    t = node.Node.parse_obj(COMPOUND_PARAM)
    assert t == COMPOUND_EXPECT
