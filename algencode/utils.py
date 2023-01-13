"""Algencode node utilities."""
from __future__ import annotations

from contextlib import suppress
from typing import Callable, Type

from .node import Node
from .types import LiteralNode, OpNode, Procs, Reduced, T, Vals


def reduce_node(
    n: LiteralNode | Node,
    vals: Vals | None,
    procs: Procs | None,
    *,
    force_debug: bool = False,
) -> Reduced:
    """Node reduce helper."""
    if isinstance(n, Node):
        return n.reduce(vals, procs, force_debug=force_debug)
    return n


def reduce_node_to(
    n: LiteralNode | Node,
    t: Type[T],
    vals: Vals | None,
    procs: Procs | None,
    *,
    force_debug: bool = False,
) -> T:
    """Node reduce as type helper."""
    if isinstance(n, t):
        return n
    if isinstance(n, Node):
        return n.reduce_to(t, vals, procs, force_debug=force_debug)
    raise TypeError(f"node {n} expected to reduce to {t}, found {type(n)} {n}")


def call_attr_op(
    node: OpNode,
    vals: Vals | None,
    procs: Procs | None = None,
    *,
    force_debug: bool = False,
):
    """Call attribute based operation."""
    del force_debug
    with suppress(AttributeError):
        f: Callable[[Vals | None, Procs | None], LiteralNode] = getattr(
            node, f"_{node.op}"
        )
        return f(vals, procs)
    raise NotImplementedError(str(node))
