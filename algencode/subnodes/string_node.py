"""String node."""
from datetime import date
from typing import Literal

from ..node import Node
from ..types import LiteralNode, Procs, Reduced, Vals
from ..utils import call_attr_op, reduce_node, reduce_node_to
from .base_node import BaseNode

STRING_OP = Literal["slice", "fmt", "rep", "join", "date"]


class StringNode(BaseNode):
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
        procs: Procs | None,
    ) -> str:
        """Slice operation.

        Expects {self.args} to be a list of either:
            - [str, int?] for slice s[:stop]
            - [str, int?, int?] for slice s[start:stop]
            - [str, int?, int?, int?] for slice s[start:stop:step]
        """
        match self.args:
            case [s, stop]:
                _s = reduce_node_to(s, str, vals, procs)
                _stop = reduce_node_to(stop, int | None, vals, procs)
                return _s[:_stop]
            case [s, start, stop]:
                _s = reduce_node_to(s, str, vals, procs)
                _start = reduce_node_to(start, int | None, vals, procs)
                _stop = reduce_node_to(stop, int | None, vals, procs)
                return _s[_start:_stop]  # type: ignore
            case [s, start, stop, step]:
                _s = reduce_node_to(s, str, vals, procs)
                _start = reduce_node_to(start, int | None, vals, procs)
                _stop = reduce_node_to(stop, int | None, vals, procs)
                _step = reduce_node_to(step, int | None, vals, procs)
                return _s[_start:_stop:_step]  # type: ignore
        raise ValueError(f"slice expects 2, 3 or 4 arguments, found {len(self.args)}")

    def _fmt(
        self,
        vals: Vals | None,
        procs: Procs | None,
    ) -> str:
        _fmt = reduce_node_to(self.args[0], str, vals, procs)
        _v = map(lambda n: reduce_node(n, vals, procs), self.args[1:])
        return _fmt.format(*_v)

    def _rep(
        self,
        vals: Vals | None,
        procs: Procs | None,
    ) -> str:
        match self.args:
            case [s, n]:
                _s = reduce_node_to(s, str, vals, procs)
                _n = reduce_node_to(n, int, vals, procs)
                return _s * _n
        raise ValueError("TODO")

    def _join(
        self,
        vals: Vals | None,
        procs: Procs | None,
    ) -> str:
        match self.args:
            case [delim, *args]:
                _delim = reduce_node_to(delim, str, vals, procs)
                _args = [reduce_node_to(a, str, vals, procs) for a in args]
                return _delim.join(_args)
        raise ValueError("TODO")

    def _date(
        self,
        vals: Vals | None,
        procs: Procs | None,
    ) -> str:
        match self.args:
            case [fmt, d]:
                _fmt = reduce_node_to(fmt, str, vals, procs)
                _d = reduce_node_to(d, date, vals, procs)
                return _d.strftime(_fmt)
        raise ValueError("TODO")

    def reduce(
        self,
        vals: Vals | None = None,
        procs: Procs | None = None,
        *,
        force_debug: bool = False,
    ) -> Reduced:
        """Reduce this string operation node."""
        res = call_attr_op(self, vals, procs)
        return super().reduce(
            {**(vals or {}), "_res": res},
            procs,
            force_debug=force_debug,
        )
