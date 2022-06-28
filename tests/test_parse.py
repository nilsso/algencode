# pylama:ignore=D103
"""Parsing tests."""
import json
import typing

import pytest

from algencode import node

PARAMS = [
    ["abc", "1"],
    1,
    3.14,
    [True, False],
    None,
]


def _test_parse_primitive(v):
    t = node.Node.parse_obj(v)
    e = node.Node(__root__=v)
    if t != e:
        pytest.fail(f'"{t}" != "{e}"')


def _test_parse_primitive_json(v):
    r = json.dumps(v)
    t = node.Node.parse_raw(r)
    e = node.Node(__root__=v)
    if t != e:
        pytest.fail(f'"{t}" != "{e}"')


@pytest.mark.parametrize("v", PARAMS, ids=str)
def test_parse_primitive(v):
    if isinstance(v, list):
        for _v in v:
            _test_parse_primitive(_v)
    else:
        _test_parse_primitive(v)


@pytest.mark.parametrize("v", PARAMS, ids=str)
def test_parse_primitive_json(v):
    if isinstance(v, list):
        for _v in v:
            _test_parse_primitive_json(_v)
    else:
        _test_parse_primitive_json(v)


@pytest.fixture
def var_node():
    v = {"key": "foo"}
    e = node.Node(__root__=node.VariableNode(key="foo"))
    return v, e


def test_parse_var_node(var_node):
    v, e = var_node
    t = node.Node.parse_obj(v)
    assert t == e


def test_parse_var_node_json(var_node):
    v, e = var_node
    r = json.dumps(v)
    print(r)
    t = node.Node.parse_raw(r)
    assert t == e


def lit_node(v: node.LiteralNode):
    return node.Node(__root__=v)


def lit_nodes(v: typing.Iterable[node.LiteralNode]):
    return list(map(lit_node, v))


def op_node_params(op_node: typing.Type[node.OpNode], op, args):
    return (
        {"op": op, "args": args},
        op_node(op=op, args=lit_nodes(args)),
    )


def _test_op_node(v, op_node):
    t = node.Node.parse_obj(v)
    e = node.Node(__root__=op_node)
    assert t == e


def _test_op_node_json(v, op_node):
    r = json.dumps(v)
    t = node.Node.parse_raw(r)
    e = node.Node(__root__=op_node)
    assert t == e


STRING_NODE_PARAMS = [
    op_node_params(node.StringNode, "slice", ["abcd", 1, 3]),
    op_node_params(node.StringNode, "fmt", ["{:08}", "cool"]),
    op_node_params(node.StringNode, "rep", ["_", 10]),
    op_node_params(node.StringNode, "join", [",", "a", "b", "c"]),
]


@pytest.mark.parametrize("v,op_node", STRING_NODE_PARAMS)
def test_parse_string_node(v, op_node):
    _test_op_node(v, op_node)


@pytest.mark.parametrize("v,op_node", STRING_NODE_PARAMS)
def test_parse_string_node_json(v, op_node):
    _test_op_node_json(v, op_node)


NUMBER_NODE_PARAMS = [
    op_node_params(node.NumberNode, "add", [1, 2, 3]),
    op_node_params(node.NumberNode, "sub", [1, 2, 3]),
    op_node_params(node.NumberNode, "mul", [1, 2, 3]),
    op_node_params(node.NumberNode, "div", [1, 2, 3]),
    op_node_params(node.NumberNode, "mod", [1, 2, 3]),
    op_node_params(node.NumberNode, "round", [1.23]),
]


@pytest.mark.parametrize("v,op_node", STRING_NODE_PARAMS)
def test_parse_number_node(v, op_node):
    _test_op_node(v, op_node)


@pytest.mark.parametrize("v,op_node", STRING_NODE_PARAMS)
def test_parse_number_node_json(v, op_node):
    _test_op_node_json(v, op_node)


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
            node.Node(__root__="{:09}"),
            node.Node(
                __root__=node.NumberNode(
                    op="round",
                    args=[
                        node.Node(
                            __root__=node.NumberNode(
                                op="mul",
                                args=[
                                    node.Node(__root__=node.VariableNode(key="levy")),
                                    node.Node(__root__=100),
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
