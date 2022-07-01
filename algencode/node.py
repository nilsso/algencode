"""Nodes module.

Contains all node models definitions: variable, numeric, string and base. Because they are
highly coupled, all definitions need to be within this one module.
"""
# TODO:
# - add underscore reserved val name checks (for proc names)
from __future__ import annotations

import functools
import operator
from contextlib import suppress
from datetime import date
from typing import Callable, Literal, Mapping, Type, TypeAlias, Union, get_args

import pydantic
from pydantic import BaseModel

from .common import LiteralNode, Number, T, Vals

Procs: TypeAlias = Mapping[str, "Node"]
SubNode: TypeAlias = Union["VariableNode", "StringNode", "NumberNode", "ProcNode"]
OpNode: TypeAlias = Union["StringNode", "NumberNode"]


class Node(BaseModel):
    """Node model."""

    __root__: SubNode = pydantic.Field(...)

    def reduce(
        self,
        vals: Vals | None = None,
        procs: Mapping[str, Node] | None = None,
    ) -> LiteralNode:
        """Reduce this node."""
        r = self.__root__
        match r:
            case VariableNode() | NumberNode() | StringNode() | ProcNode():
                return r.reduce(vals, procs)
            case str() | int() | float() | None:
                return r
            case _:
                raise NotImplementedError

    def reduce_to(
        self,
        t: Type[T],
        vals: Vals | None,
        procs: Mapping[str, Node] | None,
    ) -> T:
        """Reduce this node to an expected type."""
        res = self.reduce(vals, procs)
        if not isinstance(res, t):
            raise TypeError(
                f"node {self} expected to reduce to {t}, found {type(res)} {res}"
            )
        return res


def _reduce(
    n: LiteralNode | Node,
    vals: Vals | None,
    procs: Mapping[str, Node] | None,
) -> LiteralNode:
    """Node reduce helper."""
    if isinstance(n, Node):
        return n.reduce(vals, procs)
    return n


def _reduce_to(
    n: LiteralNode | Node,
    t: Type[T],
    vals: Vals | None,
    procs: Mapping[str, Node] | None,
) -> T:
    """Node reduce as type helper."""
    if isinstance(n, t):
        return n
    if isinstance(n, Node):
        return n.reduce_to(t, vals, procs)
    raise TypeError(f"node {n} expected to reduce to {t}, found {type(n)} {n}")


class VariableNode(BaseModel):
    """Variable node.

    Node that represents a literal value via indirection. That is, attempts to lookup
    a value with the node's specified key from a dictionary of values passed to {reduce}.
    """

    key: pydantic.StrictStr

    def reduce(
        self,
        vals: Vals | None,
        _: Mapping[str, Node] | None = None,
    ) -> LiteralNode:
        """Reduce the variable operation node."""
        if not vals:
            raise RuntimeError(
                f"value node with key={self.key} expected dictionary of values"
            )
        with suppress(KeyError):
            return vals[self.key]
        raise KeyError(f"key={self.key} not found in values")


def _call_attr_op(
    node: OpNode,
    vals: Vals | None,
    procs: Mapping[str, Node] | None = None,
):
    with suppress(AttributeError):
        f: Callable[[Vals | None, Procs | None], LiteralNode] = getattr(
            node, f"_{node.op}"
        )
        return f(vals, procs)
    raise NotImplementedError(str(node))


STRING_OP = Literal["slice", "fmt", "rep", "join", "date"]


class StringNode(BaseModel):
    """String node.

    Node that supports a variety of string operations:
        - slicing {slice}
        - formatting {fmt}
        - repeating {rep}
        - joining {join}
        - date formatting {date}

    TODO: (More) documentation on operations and their arguments
    """

    op: STRING_OP
    args: list[LiteralNode | Node]

    def _slice(
        self,
        vals: Vals | None,
        procs: Mapping[str, Node] | None,
    ) -> str:
        """Slice operation.

        Expects {self.args} to be a list of either:
            - [str, int?] for slice s[:stop]
            - [str, int?, int?] for slice s[start:stop]
            - [str, int?, int?, int?] for slice s[start:stop:step]
        """
        match self.args:
            case [s, stop]:
                _s = _reduce_to(s, str, vals, procs)
                _stop = _reduce_to(stop, int | None, vals, procs)
                return _s[:_stop]
            case [s, start, stop]:
                _s = _reduce_to(s, str, vals, procs)
                _start = _reduce_to(start, int | None, vals, procs)
                _stop = _reduce_to(stop, int | None, vals, procs)
                return _s[_start:_stop]  # type: ignore
            case [s, start, stop, step]:
                _s = _reduce_to(s, str, vals, procs)
                _start = _reduce_to(start, int | None, vals, procs)
                _stop = _reduce_to(stop, int | None, vals, procs)
                _step = _reduce_to(step, int | None, vals, procs)
                return _s[_start:_stop:_step]  # type: ignore
        raise ValueError(f"slice expects 2, 3 or 4 arguments, found {len(self.args)}")

    def _fmt(
        self,
        vals: Vals | None,
        procs: Mapping[str, Node] | None,
    ) -> str:
        _fmt = _reduce_to(self.args[0], str, vals, procs)
        _v = map(lambda n: _reduce(n, vals, procs), self.args[1:])
        return _fmt.format(*_v)

    def _rep(
        self,
        vals: Vals | None,
        procs: Mapping[str, Node] | None,
    ) -> str:
        match self.args:
            case [s, n]:
                _s = _reduce_to(s, str, vals, procs)
                _n = _reduce_to(n, int, vals, procs)
                return _s * _n
        raise ValueError("TODO")

    def _join(
        self,
        vals: Vals | None,
        procs: Mapping[str, Node] | None,
    ) -> str:
        match self.args:
            case [delim, *args]:
                _delim = _reduce_to(delim, str, vals, procs)
                _args = [_reduce_to(a, str, vals, procs) for a in args]
                return _delim.join(_args)
        raise ValueError("TODO")

    def _date(
        self,
        vals: Vals | None,
        procs: Mapping[str, Node] | None,
    ) -> str:
        match self.args:
            case [fmt, d]:
                _fmt = _reduce_to(fmt, str, vals, procs)
                _d = _reduce_to(d, date, vals, procs)
                return _d.strftime(_fmt)
        raise ValueError("TODO")

    def reduce(
        self,
        vals: Vals | None = None,
        procs: Mapping[str, Node] | None = None,
    ) -> LiteralNode:
        """Reduce this string operation node."""
        return _call_attr_op(self, vals, procs)


Reducer: TypeAlias = Callable[[T, T], T]

NUMBER_BINARY_OP = Literal["add", "sub", "mul", "mod", "div"]
NUMBER_OP = Literal[NUMBER_BINARY_OP, "round"]

NUMBER_BINARY_REDUCERS: dict[str, Reducer] = dict(
    zip(
        get_args(NUMBER_BINARY_OP),
        [
            operator.add,
            operator.sub,
            operator.mul,
            operator.mod,
            operator.truediv,
        ],
    )
)


class NumberNode(BaseModel):
    """Numeric operation node.

    TODO: Documentation on operations and their arguments
    """

    op: NUMBER_OP
    args: list[LiteralNode | Node]

    def _round(
        self,
        vals: Vals | None,
        procs: Mapping[str, Node] | None,
    ) -> Number:
        match self.args:
            case [n]:
                _n = _reduce_to(n, Number, vals, procs)
                return round(_n)
            case [n, ndigits]:
                _n = _reduce_to(n, Number, vals, procs)
                _ndigits = _reduce_to(ndigits, int | None, vals, procs)
                return round(_n, _ndigits)
        raise ValueError(f"round expects 1 or 2 arguments, found {len(self.args)}")

    def reduce(
        self,
        vals: Vals | None = None,
        procs: Mapping[str, Node] | None = None,
    ) -> LiteralNode:
        """Reduce this numeric operation node."""
        args = map(lambda n: _reduce_to(n, Number, vals, procs), self.args)
        if binary_reducer := NUMBER_BINARY_REDUCERS.get(self.op):
            return functools.reduce(binary_reducer, args)
        return _call_attr_op(self, vals)


class ProcNode(BaseModel):
    """Stored procedure node."""

    proc: pydantic.StrictStr
    args: list[LiteralNode | Node]

    @property
    def _proc_keys(self):
        return [f"_{i}" for i in range(len(self.args))]

    def reduce(
        self,
        vals: Vals | None = None,
        procs: Mapping[str, Node] | None = None,
    ) -> LiteralNode:
        """Reduce this stored proceedure node."""
        if procs is None:
            raise RuntimeError("expected proc map, found None")
        if n := procs.get(self.proc):
            proc_vals = dict(
                zip(
                    self._proc_keys,
                    [_reduce(a, vals, procs) for a in self.args],
                )
            )
            return n.reduce(proc_vals)
        raise KeyError(f'failed to find proc node "{self.proc}"')


MODEL_TYPES = [
    Node,
    VariableNode,
    NumberNode,
    StringNode,
]

for model in MODEL_TYPES:
    model.update_forward_refs()
