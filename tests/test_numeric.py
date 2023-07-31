# pylama:ignore=D103
"""Numeric tests."""
from itertools import count
from typing import Iterable, Iterator, TypeAlias, cast

import pytest

from .common import Json, LiteralNode, Vals, node_test

BaseInput: TypeAlias = list[int]
BaseExpect: TypeAlias = tuple[int, int, int, int]  # (+,-,*,%)


def _make_lit_params(
    base_params: list[tuple[BaseInput, BaseExpect]],
) -> tuple[list[tuple[BaseInput, int]], ...]:
    inputs, expecteds = cast(
        tuple[
            tuple[BaseInput, ...],
            tuple[BaseExpect, ...],
        ],
        zip(*base_params),
    )
    groups: Iterator[tuple[int, ...]] = zip(*expecteds)
    return tuple(map(lambda e: list(zip(inputs, e)), groups))


def _make_params(
    params: tuple[str, Iterable[tuple[list[int], int]]],
):
    op, lit_params = params
    for p in lit_params:
        inputs, expects = p
        node: Json = {
            "op": op,
            "args": inputs,
        }
        yield node, expects


def _make_val_params(
    params: tuple[Json, int],
) -> tuple[Json, int, dict[str, LiteralNode]]:
    node, expects = params
    vals: dict[str, LiteralNode] = {}
    i = count()

    def _swap(v: LiteralNode) -> Json:
        key = chr(ord("a") + next(i))
        vals[key] = v
        return {"key": key}

    def _map_arg(arg: Json) -> Json:
        match arg:
            case int() | str():
                return _swap(arg)
            case _:
                return arg

    def _map_item(item: tuple[str, Json]) -> tuple[str, Json]:
        k, v = item
        match v:
            case list() if k == "args":
                return k, list(map(_map_arg, v))
            case _:
                return k, v

    def _map_node(node: Json) -> Json:
        match node:
            case int() | str():
                return _swap(node)
            case dict():
                return dict(map(_map_item, node.items()))
            case list():
                return [_map_node(v) for v in node]
            case _:
                raise Exception(f"{type(node)} {node}")

    new_node = _map_node(node)
    return new_node, expects, vals


# fmt: off
BASE_PARAMS = [  # noqa
    (
        [1, 2, 3],
        (
             6,  # add
            -4,  # sub
             6,  # mul
             1,  # mod
             2,  # mean
             3,  # len
        ),
    ),
    (
        [2, 3, 4],
        (
             9,  # add
            -5,  # sub
            24,  # mul
             2,  # mod
             3,  # mean
             3,  # len
        ),
    ),
    (
        [25, 5],
        (
             30,  # add
             20,  # sub
            125,  # mul
              0,  # mod
             15,  # mean
              2,  # len
        ),
    ),
]
# fmt: on

OPS = ["add", "sub", "mul", "mod", "mean", "len"]

op_lit_params = zip(OPS, _make_lit_params(BASE_PARAMS))

(
    add_params,
    sub_params,
    mul_params,
    mod_params,
    mean_params,
    len_params,
) = params = tuple(map(tuple, map(_make_params, op_lit_params)))

(
    add_val_params,
    sub_val_params,
    mul_val_params,
    mod_val_params,
    mean_val_params,
    len_val_params,
) = map(lambda p: map(_make_val_params, p), params)


@pytest.mark.parametrize("node,expects", add_params)
def test_number_add(node: Json, expects: int):
    node_test(node, {}, expects)


@pytest.mark.parametrize("node,expects", sub_params)
def test_number_sub(node: Json, expects: int):
    node_test(node, {}, expects)


@pytest.mark.parametrize("node,expects", mul_params)
def test_number_mul(node: Json, expects: int):
    node_test(node, {}, expects)


@pytest.mark.parametrize("node,expects", mod_params)
def test_number_mod(node: Json, expects: int):
    node_test(node, {}, expects)


@pytest.mark.parametrize("node,expects", mean_params)
def test_number_len(node: Json, expects: int):
    node_test(node, {}, expects)


@pytest.mark.parametrize("node,expects", len_params)
def test_number_mean(node: Json, expects: int):
    node_test(node, {}, expects)


@pytest.mark.parametrize("node,expects,vals", add_val_params)
def test_number_add_vals(node: Json, expects: int, vals: Vals):
    node_test(node, vals, expects)


@pytest.mark.parametrize("node,expects,vals", sub_val_params)
def test_number_sub_vals(node: Json, expects: int, vals: Vals):
    node_test(node, vals, expects)


@pytest.mark.parametrize("node,expects,vals", mul_val_params)
def test_number_mul_vals(node: Json, expects: int, vals: Vals):
    node_test(node, vals, expects)


@pytest.mark.parametrize("node,expects,vals", mod_val_params)
def test_number_mod_vals(node: Json, expects: int, vals: Vals):
    node_test(node, vals, expects)


@pytest.mark.parametrize("node,expects,vals", mean_val_params)
def test_number_mean_vals(node: Json, expects: int, vals: Vals):
    node_test(node, vals, expects)


@pytest.mark.parametrize("node,expects,vals", len_val_params)
def test_number_len_vals(node: Json, expects: int, vals: Vals):
    node_test(node, vals, expects)
