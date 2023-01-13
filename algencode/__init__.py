"""Algorithm encoding module."""
import logging

from .node import Node, Procs
from .subnodes import *
from .types import Vals

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("algencode")

MODEL_TYPES = [
    Node,
    VariableNode,
    NumberNode,
    StringNode,
    ProcNode,
]
refs = {m.__name__: m for m in MODEL_TYPES}
for model in MODEL_TYPES:
    model.update_forward_refs(**refs)

__all__ = [
    "Node",
    "Vals",
    "Procs",
]
