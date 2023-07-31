"""Subnode base type (subclassed by subnodes, used by Node)."""
from __future__ import annotations

import logging
from abc import ABC
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from .types import Procs, Reduced, Vals

if TYPE_CHECKING:
    from .node import Node

logger = logging.getLogger("algencode.subnodes.base_node")


class BaseNode(BaseModel, ABC):
    """Subnode base type."""

    debug: Node | None = Field(default=None, repr=False)

    def reduce(
        self,
        vals: Vals | None = None,
        procs: Procs | None = None,
        *,
        force_debug: bool = False,
    ) -> Reduced:
        """Reduce this base node.

        Doesn't actually do anything other than return the value indexed by "_res_rhs".
        For providing debug functionality, and should only be used by subclasses.

        Raises:
            AssertionError: If vals is None.
            KeyError: If "_res_lhs" or "_res_rhs" not present in vals.
        """
        assert vals is not None
        res = vals["_res"]
        if force_debug or (self.debug is not None and self.debug.root is not False):
            if self.debug is None or self.debug.root is True:
                logger.debug(f"{repr(self)} -> {res}")
            else:
                logger.debug(self.debug.reduce(vals, procs))
        return res
