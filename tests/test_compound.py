# pylama:ignore=D103
"""More complex (compound) node tests."""
import pytest

from .common import Json, Node, Vals


@pytest.mark.parametrize(
    "v,e",
    [
        ({"a": 2, "b": 3}, 12),
        ({"a": 4, "b": 6}, 22),
        ({"a": 24, "b": 25}, 100),
    ],
    ids=str,
)
def test_compound_01(v: Vals, e: int):
    n: Json = {
        "op": "mul",
        "args": [
            {
                "op": "add",
                "args": [1, {"key": "a"}, {"key": "b"}],
            },
            2,
        ],
    }
    assert Node.model_validate(n).reduce(v) == e


def test_compound_02():
    n: Json = {
        "op": "slice",
        "args": [
            {
                "op": "fmt",
                "args": [
                    "{:>07}",
                    {
                        "op": "mul",
                        "args": [
                            2,
                            2,
                            2,
                            2,
                            2,
                            2,
                            1929,
                        ],
                    },
                ],
            },
            None,
            None,
            -1,
        ],
    }

    assert Node.model_validate(n).reduce() == "6543210"
