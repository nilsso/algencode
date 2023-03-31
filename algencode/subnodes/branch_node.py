"""Branching node model."""
from .base_node import BaseNode


class BranchNode(BaseNode):
    """Branching node.

    Node that represents a branch in logic.
    """

    expr: Node
    if_true: int
    if_false: int
