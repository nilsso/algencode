"""Algorithm encoding module."""
from __future__ import annotations

import logging

from .node import Node, Procs
from .subnodes import NumberNode, ProcNode, StringNode, VariableNode
from .types import Vals

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("algencode")

Node.model_rebuild()

__all__ = [
    "Node",
    "NumberNode",
    "ProcNode",
    "Procs",
    "StringNode",
    "Vals",
    "VariableNode",
]
