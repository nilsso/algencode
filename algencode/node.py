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
from typing import Callable, Iterable, Literal, Mapping, Type, TypeAlias, Union, cast

import pydantic
from pydantic import BaseModel, validator

from .common import LiteralNode, Number, T, Vals

Procs: TypeAlias = Mapping[str, "Node"]
SubNode: TypeAlias = Union["VariableNode", "StringNode", "NumberNode", "ProcNode"]
OpNode: TypeAlias = Union["StringNode", "NumberNode"]


class Node(BaseModel):
    """Node model."""

    __root__: SubNode | LiteralNode | None = pydantic.Field(...)

    @staticmethod
    def _passthrough(values: Iterable[LiteralNode]) -> list[Node | LiteralNode]:
        def _helper(v: LiteralNode) -> Node | LiteralNode:
            if v is None:
                return Node(__root__=None)
            return v

        return list(map(_helper, values))

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
        vals: Vals | None = None,
        procs: Mapping[str, Node] | None = None,
    ) -> T:
        """Reduce this node to an expected type."""
        res = self.reduce(vals, procs)
        if not isinstance(res, t):
            raise ValueError(f"format node did not reduce to string: {self}")
        return res

    def _type(
        self,
        t: Type[T],
        vals: Vals | None,
        procs: Mapping[str, Node] | None,
    ) -> T:
        """Validate node literal type.

        Returns:
            The node literal as specified type if it is that type.

        Raises:
            ValueError: If not of specified type.
        """
        res = self.reduce(vals, procs)
        if isinstance(res, t):
            return res
        raise ValueError(f"expected {t}, found {type(res)} {res}")


class VariableNode(BaseModel):
    """Variable node.

    Node that represents a literal value via indirection. That is, attempts to lookup
    a value with the node's specified key from a dictionary of values passed to {reduce}.

    Raises:
        ValueError: if no value dictionary was provided.
        KeyError: if the specified key was not found.
    """

    key: pydantic.StrictStr

    def reduce(
        self,
        vals: Vals | None = None,
        _: Mapping[str, Node] | None = None,
    ) -> LiteralNode:
        """Reduce the variable operation node."""
        if not vals:
            raise ValueError(
                f"value node with key={self.key} expected dictionary of values"
            )
        try:
            return vals[self.key]
        except KeyError:
            raise ValueError(f"key={self.key} not found in values")


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

    op: Literal["slice", "fmt", "rep", "join", "date"]
    args: list[Node]

    @validator("args", pre=True)
    def none_is_okay(cls, values):
        """Allow Nones in args list."""
        return Node._passthrough(values)

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

        Raises:
            ValueError: If invalid number of arguments
                or invalid argument types (as thrown by Node._type).
        """
        match self.args:
            case [s, stop]:
                _s = s._type(str, vals, procs)
                _stop = stop._type(int | None, vals, procs)
                return _s[:_stop]
            case [s, start, stop]:
                _s = s._type(str, vals, procs)
                _start = start._type(int | None, vals, procs)
                _stop = stop._type(int | None, vals, procs)
                return _s[_start:_stop]  # type: ignore
            case [s, start, stop, step]:
                _s = s._type(str, vals, procs)
                _start = start._type(int | None, vals, procs)
                _stop = stop._type(int | None, vals, procs)
                _step = step._type(int | None, vals, procs)
                return _s[_start:_stop:_step]  # type: ignore
        raise ValueError(f"slice expects 2, 3 or 4 arguments, found {len(self.args)}")

    def _fmt(
        self,
        vals: Vals | None,
        procs: Mapping[str, Node] | None,
    ) -> str:
        _fmt = self.args[0]._type(str, vals, procs)
        _v = map(lambda n: Node.reduce(n, vals, procs), self.args[1:])
        return _fmt.format(*_v)

    def _rep(
        self,
        vals: Vals | None,
        procs: Mapping[str, Node] | None,
    ) -> str:
        match self.args:
            case [s, n]:
                _s = s._type(str, vals, procs)
                _n = n._type(int, vals, procs)
                return _s * _n
        raise ValueError

    def _join(
        self,
        vals: Vals | None,
        procs: Mapping[str, Node] | None,
    ) -> str:
        match self.args:
            case [delim, *args]:
                _delim = delim._type(str, vals, procs)
                _args = [a._type(str, vals, procs) for a in args]
                return _delim.join(_args)
        raise ValueError

    def _date(
        self,
        vals: Vals | None,
        procs: Mapping[str, Node] | None,
    ) -> str:
        match self.args:
            case [fmt, d]:
                _fmt = fmt._type(str, vals, procs)
                _d = d._type(date, vals, procs)
                return _d.strftime(_fmt)
        raise ValueError

    def reduce(
        self,
        vals: Vals | None = None,
        procs: Mapping[str, Node] | None = None,
    ) -> LiteralNode:
        """Reduce this string operation node."""
        return _call_attr_op(self, vals, procs)


Reducer: TypeAlias = Callable[[T, T], T]

NUM_BINARY_OPS = Literal["add", "sub", "mul", "mod", "div"]
NUM_OPS = Literal[NUM_BINARY_OPS, "round"]
NUM_BINARY_REDUCERS: dict[str, Reducer] = dict(
    zip(
        cast(tuple[str], NUM_BINARY_OPS.__args__),  # type: ignore
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

    op: NUM_OPS
    args: list[Node]

    @validator("args", pre=True)
    def none_is_okay(cls, values):
        """Allow Nones in args list."""
        return Node._passthrough(values)

    def _round(
        self,
        vals: Vals | None,
        procs: Mapping[str, Node] | None,
    ) -> Number:
        match self.args:
            case [n]:
                _n = n._type(Number, vals, procs)
                return round(_n)
            case [n, ndigits]:
                _n = n._type(Number, vals, procs)
                _ndigits = ndigits._type(int | None, vals, procs)
                return round(_n, _ndigits)
        raise ValueError(f"round expects 1 or 2 arguments, found {len(self.args)}")

    def reduce(
        self,
        vals: Vals | None = None,
        procs: Mapping[str, Node] | None = None,
    ) -> LiteralNode:
        """Reduce this numeric operation node."""
        args = map(lambda n: n._type(Number, vals, procs), self.args)
        if binary_reducer := NUM_BINARY_REDUCERS.get(self.op):
            return functools.reduce(binary_reducer, args)
        return _call_attr_op(self, vals)


class ProcNode(BaseModel):
    """Stored procedure node."""

    proc: pydantic.StrictStr
    args: list[Node]

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
            raise ValueError("expected proc map, found None")
        if n := procs.get(self.proc):
            proc_vals = dict(zip(self._proc_keys, [a.reduce(vals) for a in self.args]))
            return n.reduce(proc_vals)
        raise ValueError(f'failed to find proc node "{self.proc}"')


MODEL_TYPES = [
    Node,
    VariableNode,
    NumberNode,
    StringNode,
]

for model in MODEL_TYPES:
    model.update_forward_refs()
