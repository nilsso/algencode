"""Common types and utilities."""
from __future__ import annotations

from datetime import date  # TODO: consider adding datetime too
from decimal import Decimal
from typing import (
    TYPE_CHECKING,
    Callable,
    Mapping,
    Optional,
    Sequence,
    TypeAlias,
    TypeVar,
    Union,
)

import pydantic

if TYPE_CHECKING:
    from .node import Node
    from .subnodes import NumberNode, ProcNode, StringNode, VariableNode

T = TypeVar("T")

Number: TypeAlias = int | float | Decimal
"""Number types."""

LiteralNode: TypeAlias = Optional[
    Union[
        pydantic.StrictStr,
        pydantic.StrictInt,
        pydantic.StrictFloat,
        pydantic.StrictBool,
        Decimal,
        date,
        int,
    ]
]
"""Literal node."""

Json: TypeAlias = LiteralNode | Sequence["Json"] | Mapping[str, "Json"]
"""Json data."""

Vals: TypeAlias = Mapping[
    str,
    Union[
        LiteralNode,
        Sequence[LiteralNode],
    ],
]
"""Reducer vals argumennt."""

Procs: TypeAlias = Mapping[str, Union["Node", dict[str, Json]]]
"""Reducer procs argument."""

Reduced: TypeAlias = LiteralNode | Sequence[LiteralNode]
"""Reducer return."""

Reducer: TypeAlias = Callable[[T, T], T]
"""Homogeneous typed binary reducer function."""

SubNode: TypeAlias = Union["VariableNode", "StringNode", "NumberNode", "ProcNode"]
"""Subnodes."""

OpNode: TypeAlias = Union["StringNode", "NumberNode"]
"""Operation nodes."""

OpArgs: TypeAlias = Union[list[LiteralNode | "Node"], "VariableNode"]
"""Operation node args."""
