# pylama:ignore=D103
"""Parsing tests."""
import json

import pytest

from .common import *


def f(t, op, args):
    n = Node(__root__=t(op=op, args=args))
    obj = {
        "op": op,
        "args": args,
    }
    return (n, obj)


PARAMS = [
    f(
        StringNode,
        "slice",
        ["abcd", 1, 3],
    ),
    f(
        StringNode,
        "fmt",
        ["{:08}", "cool"],
    ),
    f(
        StringNode,
        "rep",
        ["_", 10],
    ),
    f(
        StringNode,
        "join",
        [",", "a", "b", "c"],
    ),
    f(
        NumberNode,
        "add",
        [1, 2, 3],
    ),
    f(
        NumberNode,
        "sub",
        [1, 2, 3],
    ),
    f(
        NumberNode,
        "mul",
        [1, 2, 3],
    ),
    f(
        NumberNode,
        "div",
        [1, 2, 3],
    ),
    f(
        NumberNode,
        "mod",
        [1, 2, 3],
    ),
    f(
        NumberNode,
        "round",
        [1.23],
    ),
]


@pytest.mark.parametrize("n,obj", PARAMS)
def test_parse_node(n, obj):
    assert n == Node.parse_obj(obj)


@pytest.mark.parametrize("n,obj", PARAMS)
def test_parse_node_json(n, obj):
    r = json.dumps(obj)
    assert n == Node.parse_raw(r)


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

COMPOUND_EXPECT = Node(
    __root__=StringNode(
        op="fmt",
        args=[
            "{:09}",
            Node(
                __root__=NumberNode(
                    op="round",
                    args=[
                        Node(
                            __root__=NumberNode(
                                op="mul",
                                args=[
                                    Node(__root__=VariableNode(key="levy")),
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
    t = Node.parse_obj(COMPOUND_PARAM)
    assert t == COMPOUND_EXPECT
