"""Variable node model."""
from __future__ import annotations

from contextlib import suppress

from pydantic import StrictStr

from ..types import Procs, Reduced, Vals
from ..base_node import BaseNode


class VariableNode(BaseNode):
    """Variable node.

    Node that represents a literal value via indirection. That is, attempts to lookup
    a value with the node's specified key from a dictionary of values passed to {reduce}.
    """

    key: StrictStr

    def reduce(
        self,
        vals: Vals | None,
        procs: Procs | None = None,
        *,
        force_debug: bool = False,
    ) -> Reduced:
        """Reduce the variable operation node."""
        if vals is None:
            raise RuntimeError(
                f"value node with key={self.key} expected dictionary of values"
            )
        with suppress(KeyError):
            res = vals[self.key]
            return super().reduce(
                {**(vals or {}), "_res": res},
                procs,
                force_debug=force_debug,
            )
        raise KeyError(f"key={self.key} not found in values")
