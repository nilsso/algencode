"""Proc (stored procedure) node."""
from __future__ import annotations

from pydantic import StrictStr

from ..node import Node
from ..types import LiteralNode, Procs, Reduced, Vals
from ..utils import reduce_node
from ..base_node import BaseNode


class ProcNode(BaseNode):
    """Stored procedure node."""

    proc: StrictStr
    args: list[LiteralNode | Node] | None = None

    def reduce(
        self,
        vals: Vals | None = None,
        procs: Procs | None = None,
        *,
        force_debug: bool = False,
    ) -> Reduced:
        """Reduce this stored proceedure node."""
        if procs is None:
            raise RuntimeError("expected proc map, found None")
        if n := procs.get(self.proc):
            if isinstance(n, dict):
                n = Node.model_validate(n)
            if self.args:
                proc_keys = [f"_{i}" for i in range(len(self.args))]
                proc_vals = dict(
                    zip(
                        proc_keys,
                        [reduce_node(a, vals, procs) for a in self.args],
                    )
                )
                res = n.reduce(proc_vals, force_debug=force_debug)
            else:
                res = n.reduce(vals, procs, force_debug=force_debug)
            return super().reduce(
                {**(vals or {}), "_res": res},
                procs,
                force_debug=force_debug,
            )
        raise KeyError(f'failed to find proc node "{self.proc}"')
