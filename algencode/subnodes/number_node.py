"""Number node."""
from __future__ import annotations

import operator
from functools import partial, reduce
from typing import Literal, Sequence, get_args

from ..node import Node
from ..types import LiteralNode, Number, OpArgs, Procs, Reduced, Reducer, Vals
from ..utils import call_attr_op, reduce_node_to
from .base_node import BaseNode
from .variable_node import VariableNode


def sequence_args(
    args: OpArgs,
    vals: Vals | None,
    procs: Procs | None,
) -> Sequence[LiteralNode | Node]:
    """Map and/or validate args as node sequence."""
    _args = args
    if isinstance(_args, VariableNode):
        _args = _args.reduce(vals, procs)
    assert isinstance(_args, list) or isinstance(_args, tuple)
    return _args


NUMBER_OP_BUILTIN = Literal[
    "add",
    "sub",
    "mul",
    "mod",
    "div",
    "min",
    "max",
]
NUMBER_OP = Literal[
    NUMBER_OP_BUILTIN,
    "round",
    "len",
    "mean",
]

NUMBER_OP_BUILTINreduce_nodeRS: dict[str, Reducer] = dict(
    zip(
        get_args(NUMBER_OP_BUILTIN),
        [
            operator.add,
            operator.sub,
            operator.mul,
            operator.mod,
            operator.truediv,
            min,
            max,
        ],
    )
)


class NumberNode(BaseNode):
    """Numeric operation node."""

    op: NUMBER_OP
    args: OpArgs

    def _round(
        self,
        vals: Vals | None,
        procs: Procs | None,
    ) -> Number:
        args = sequence_args(self.args, vals, procs)
        match args:
            case [n]:
                _n = reduce_node_to(n, Number, vals, procs)
                return round(_n)
            case [n, ndigits]:
                _n = reduce_node_to(n, Number, vals, procs)
                _ndigits = reduce_node_to(ndigits, int | None, vals, procs)
                return round(_n, _ndigits)
        raise ValueError(f"round expects 1 or 2 arguments, given: {args}")

    def _len(
        self,
        vals: Vals | None,
        procs: Procs | None,
    ) -> Number:
        return len(sequence_args(self.args, vals, procs))

    def _mean(
        self,
        vals: Vals | None,
        procs: Procs | None,
    ) -> Number:
        args = sequence_args(self.args, vals, procs)
        args = list(map(lambda n: reduce_node_to(n, Number, vals, procs), args))
        return sum(args) / len(args)

    def reduce(
        self,
        vals: Vals | None = None,
        procs: Procs | None = None,
        *,
        force_debug: bool = False,
    ) -> Reduced:
        """Reduce this numeric operation node."""
        args = sequence_args(self.args, vals, procs)
        f = partial(
            reduce_node_to,
            t=Number,
            vals=vals,
            procs=procs,
            force_debug=force_debug,
        )
        args = map(f, args)
        if binaryreduce_noder := NUMBER_OP_BUILTINreduce_nodeRS.get(self.op):
            res = reduce(binaryreduce_noder, args)
        else:
            res = call_attr_op(self, vals)
        return super().reduce(
            {**(vals or {}), "_res": res},
            procs,
            force_debug=force_debug,
        )
