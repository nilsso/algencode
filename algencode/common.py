"""Common types and utilities."""
from __future__ import annotations

from datetime import date  # TODO: consider adding datetime too
from decimal import Decimal
from typing import Callable, Mapping, Optional, Sequence, TypeAlias, TypeVar, Union

import pydantic

T = TypeVar("T")

Number: TypeAlias = int | float | Decimal
LiteralNode: TypeAlias = Optional[
    Union[
        pydantic.StrictStr,
        pydantic.StrictInt,
        pydantic.StrictFloat,
        pydantic.StrictBool,
        date,
        Decimal,
    ]
]
Vals: TypeAlias = Mapping[str, LiteralNode]
Json: TypeAlias = LiteralNode | Sequence["Json"] | Mapping[str, "Json"]
Reducer: TypeAlias = Callable[[T, T], T]
