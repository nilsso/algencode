# pylama:ignore=D103
"""String node tests."""
from .common import node_test


def test_string_slice():
    node_test(
        {
            "op": "slice",
            "args": [
                "Only take a through z.",
                {"key": "start"},
                {"key": "stop"},
            ],
        },
        {
            "start": 10,
            "stop": 21,
        },
        "a through z",
    )


def test_string_fmt():
    node_test(
        {
            "op": "fmt",
            "args": [
                {"key": "fmt"},
                1234567,
            ],
        },
        {
            "fmt": "{:+015,.3f}",
        },
        "+01,234,567.000",
    )


def test_string_rep():
    node_test(
        {
            "op": "rep",
            "args": [
                "ha",
                {"key": "n"},
            ],
        },
        {
            "n": 5,
        },
        "hahahahaha",
    )


def test_string_join():
    node_test(
        {
            "op": "join",
            "args": [
                " ",
                "I",
                "drink",
                {"key": "drink"},
                "every",
                {"key": "time"},
            ],
        },
        {
            "drink": "coffee",
            "time": "morning",
        },
        "I drink coffee every morning",
    )


def test_string_compound():
    node_test(
        {
            "op": "rep",
            "args": [
                {
                    "op": "join",
                    "args": [
                        "-",
                        {
                            "op": "fmt",
                            "args": [
                                "{:>8}",
                                {
                                    "op": "slice",
                                    "args": [{"key": "msg"}, 1, 8],
                                },
                            ],
                        },
                        {
                            "op": "fmt",
                            "args": [
                                "{:<8}",
                                {
                                    "op": "slice",
                                    "args": [
                                        {
                                            "op": "slice",
                                            "args": [{"key": "msg"}, 1, 8],
                                        },
                                        None,
                                        None,
                                        -1,
                                    ],
                                },
                            ],
                        },
                    ],
                },
                2,
            ],
        },
        {"msg": "hello world"},
        " ello wo-ow olle  ello wo-ow olle ",
    )
