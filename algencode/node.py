"""Nodes module.

Contains all node models definitions: variable, numeric, string and base. Because they are
highly coupled, all definitions need to be within this one module.
"""
from __future__ import annotations

import functools
import operator
from contextlib import suppress
from typing import Any, Callable, Literal, Optional, Protocol, Type, TypeAlias, Union

import pydantic
from pydantic import BaseModel, validator

from .common import LiteralNode, T, Vals

SubNode: TypeAlias = Union["VariableNode", "StringNode", "NumberNode"]


class Node(BaseModel):
    """Node model."""

    __root__: Optional[LiteralNode | SubNode] = pydantic.Field(...)

    @staticmethod
    def _passthrough(v: LiteralNode) -> Node | LiteralNode:
        """Deals with Pydantic "bug" not allowing None in nested types."""
        if v is None:
            return Node(__root__=None)
        return v

    def reduce(self, vals: Vals | None = None) -> LiteralNode:
        """Reduce this node."""
        r = self.__root__
        match r:
            case VariableNode() | NumberNode() | StringNode():
                return r.reduce(vals)
            case int() | str() | None:
                return r
            case _:
                raise NotImplementedError

    @staticmethod
    def _type(n: LiteralNode, t: Type[T]) -> T:
        """Validate node literal type.

        Returns:
            The node literal as specified type if it is that type.

        Raises:
            ValueError: If not of specified type.
        """
        if isinstance(n, t):
            return n
        raise ValueError(f"expected {t}, found {type(n)}")

    def _int(self, vals: Vals | None) -> int:
        """Validate integer literal node."""
        return Node._type(self.reduce(vals), int)

    def _opt_int(self, vals: Vals | None) -> int | None:
        return Node._type(self.reduce(vals), int | None)

    def _str(self, vals: Vals | None) -> str:
        """Validate string literal node."""
        return Node._type(self.reduce(vals), str)


class VariableNode(BaseModel):
    """Variable node.

    Node that represents a literal value via indirection. That is, attempts to lookup
    a value with the node's specified key from a dictionary of values passed to {reduce}.

    Raises:
        ValueError: if no value dictionary was provided.
        KeyError: if the specified key was not found.
    """

    key: pydantic.StrictStr

    def reduce(self, vals: Vals | None = None) -> LiteralNode:
        """Reduce the variable operation node."""
        if not vals:
            raise ValueError("value node expected dictionary of values")
        return vals[self.key]


class StringNode(BaseModel):
    """String node.

    Node that supports a variety of string operations:
        - slicing {slice}
        - formatting {fmt}
        - repeating {rep}
        - joining {join}
    """

    op: Literal["slice", "fmt", "rep", "join"]
    args: list[Node]

    @validator("args", pre=True)
    def none_is_okay(cls, values):
        return list(map(Node._passthrough, values))

    def _slice(self, vals: Vals | None) -> str:
        """Slice operation.

        Expects {self.args} to be a list of either:
            - [str, int] for slice s[:stop]
            - [str, int, int] for slice s[start:stop]
            - [str, int, int, int] for slice s[start:stop:step]

        Raises:
            ValueError: If invalid number of arguments
                or invalid argument types (as thrown by Node._type).
        """
        match self.args:
            case [s, stop]:
                (_s, _stop) = (
                    s._str(vals),
                    stop._opt_int(vals),
                )
                return _s[:_stop]
            case [s, start, stop]:
                (_s, _start, _stop) = (
                    s._str(vals),
                    start._opt_int(vals),
                    stop._opt_int(vals),
                )
                return _s[_start:_stop]  # type: ignore
            case [s, start, stop, step]:
                (_s, _start, _stop, _step,) = (
                    s._str(vals),
                    start._opt_int(vals),
                    stop._opt_int(vals),
                    step._opt_int(vals),
                )
                return _s[_start:_stop:_step]  # type: ignore
        raise ValueError(f"slice expects 2, 3 or 4 arguments but found {len(self.args)}")

    def _fmt(self, vals: Vals | None) -> str:
        match self.args:
            case [fmt, v]:
                _fmt = fmt._str(vals)
                return _fmt.format(v.reduce(vals))
        raise ValueError

    def _rep(self, vals: Vals | None) -> str:
        match self.args:
            case [s, n]:
                _s = s._str(vals)
                _n = n._int(vals)
                return _s * _n
        raise ValueError

    def _join(self, vals: Vals | None) -> str:
        match self.args:
            case [delim, *args]:
                _delim = delim._str(vals)
                _args = [a._str(vals) for a in args]
                return _delim.join(_args)
        raise ValueError

    def reduce(self, vals: Vals | None = None) -> LiteralNode:
        """Reduce the string operation node."""
        with suppress(AttributeError):
            f: Callable[[Vals | None], LiteralNode] = getattr(self, f"_{self.op}")
            return f(vals)
        raise NotImplementedError


Reducer: TypeAlias = Callable[[T, T], T]

NUM_REDUCERS: dict[str, Reducer] = dict(
    zip(
        ["add", "sub", "mul", "mod"],
        [
            operator.add,
            operator.sub,
            operator.mul,
            operator.mod,
        ],
    )
)


class NumberNode(BaseModel):
    """Numeric operation node."""

    op: Literal["add", "sub", "mul", "div", "mod"]
    args: list[Node]

    def reduce(self, vals: Vals | None = None) -> LiteralNode:
        """Reduce the numeric operation node."""
        args = map(lambda n: Node.reduce(n, vals), self.args)
        return functools.reduce(NUM_REDUCERS[self.op], args)


class _Model(Protocol):
    @classmethod
    def update_forward_refs(cls, **localns: Any):
        ...


MODEL_TYPES: list[_Model] = [
    Node,
    VariableNode,
    NumberNode,
    StringNode,
]

for model in MODEL_TYPES:
    model.update_forward_refs()
