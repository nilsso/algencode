"""General node type."""
from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Type

from pydantic import RootModel

from .base_node import BaseNode
from .types import LiteralNode, Procs, Reduced, SubNode, T, Vals


class Node(RootModel):
    """General node type."""

    root: LiteralNode | SubNode

    def reduce(
        self,
        vals: Vals | None = None,
        procs: Procs | None = None,
        *,
        force_debug: bool = False,
    ) -> Reduced:
        """Reduce this node."""
        r = self.root
        match r:
            case str() | int() | float() | Decimal() | date() | bool() | None:
                return r
            case BaseNode():
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
