"""Algorithm encoding module."""
import logging

from .common import Vals
from .node import Node

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("algencode")

__all__ = [
    "Node",
    "Vals",
]
