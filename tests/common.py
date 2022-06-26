"""Common test utilities."""
# pylama:ignore=D103
import pytest

from algencode import Node, Vals
from algencode.common import Json


def node_test(n: Json, v: Vals, e: str | int):
    __tracebackhide__ = True
    t = Node.parse_obj(n).reduce(v)
    if t != e:
        pytest.fail(f'"{t}" != "{e}"')
