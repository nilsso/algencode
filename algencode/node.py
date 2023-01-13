"""Base node module."""
from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Type

import pydantic
from pydantic import BaseModel

from .types import LiteralNode, Procs, Reduced, SubNode, T, Vals


class Node(BaseModel):
    """Node model."""

    __root__: LiteralNode | SubNode = pydantic.Field(...)

    def reduce(
        self,
        vals: Vals | None = None,
        procs: Procs | None = None,
        *,
        force_debug: bool = False,
    ) -> Reduced:
        """Reduce this node."""
        r = self.__root__
        match r:
            case str() | int() | float() | Decimal() | date() | None:
                return r
            case _ if hasattr(r, "reduce"):
                return r.reduce(vals, procs, force_debug=force_debug)
            case _:
                raise NotImplementedError

    def reduce_to(
        self,
        t: Type[T],
        vals: Vals | None,
        procs: Procs | None,
        *,
        force_debug: bool = False,
    ) -> T:
        """Reduce this node to an expected type."""
        res = self.reduce(vals, procs, force_debug=force_debug)
        if not isinstance(res, t):
            raise TypeError(
                f"node {self} expected to reduce to {t}, found {type(res)} {res}"
            )
        return res
