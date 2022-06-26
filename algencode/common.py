"""Common types and utilities."""
from __future__ import annotations

from typing import Callable, Mapping, Sequence, TypeAlias, TypeVar

import pydantic

T = TypeVar("T")

LiteralNode: TypeAlias = pydantic.StrictStr | pydantic.StrictInt | None
Vals: TypeAlias = Mapping[str, LiteralNode]
Json: TypeAlias = LiteralNode | Sequence["Json"] | Mapping[str, "Json"]
Reducer: TypeAlias = Callable[[T, T], T]
