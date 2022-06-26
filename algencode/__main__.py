# pylama:ignore=D100,D103
from __future__ import annotations

import json
import logging
from typing import Optional, TypeAlias

import pydantic

from . import Vals, node

logger = logging.Logger(__name__, logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter("[%(levelname)s]%(lineno)d:%(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


# BaseNodeValue: TypeAlias = pydantic.StrictStr | pydantic.StrictInt
#
#
# class BaseNode(pydantic.BaseModel):
#     __root__: Optional[BaseNodeValue] = pydantic.Field(...)
#
#     @staticmethod
#     def _passthrough(v: BaseNodeValue) -> BaseNode | BaseNodeValue:
#         """Deals with Pydantic "bug" not allowing None in nested types."""
#         if v is None:
#             return BaseNode(__root__=None)
#         return v
#
#
# def _none_is_okay(cls):
#     pass
#
#
# class Node(pydantic.BaseModel):
#     nodes: list[BaseNode]
#
#     @pydantic.validator("nodes", pre=True)
#     def none_is_okay(cls, values):
#         return list(map(BaseNode._passthrough, values))
#
#
# # BaseNode.update_forward_refs()
# Node.update_forward_refs()
#
#
# print(0, BaseNode.parse_obj(1))
# print(1, BaseNode.parse_obj(None))
# print(2, Node.parse_obj({"nodes": [1]}))
# print(3, Node.parse_obj({"nodes": [BaseNode(__root__=None)]}))
# print(4, Node.parse_obj({"nodes": [None]}))
# print(5, Node.parse_obj({"nodes": [1, "2", None]}))


def do(_n: object, vals: Vals):
    print(f"{_n=}")
    n = node.Node.parse_obj(_n)
    print(f"{n=}")
    print(f"{vals=}")
    print(n.reduce(vals))


if __name__ == "__main__":
    # raw = {
    #     "op": "slice",
    #     "args": [
    #         "abcde",
    #         {"key": "a"},
    #         {"key": "b"},
    #     ],
    # }
    # raw = {
    #     "op": "mul",
    #     "args": [
    #         {
    #             "op": "add",
    #             "args": [1, {"key": "a"}, {"key": "b"}],
    #         },
    #         2,
    #     ],
    # }
    raw = {
        "op": "slice",
        "args": [
            "abc",
            -1,
            None,
            -1,
        ],
    }
    # raw = {
    #     "op": "slice",
    #     "args": [
    #         {
    #             "op": "rep",
    #             "args": [
    #                 {
    #                     "op": "fmt",
    #                     "args": ['"{:<4}"', 123],
    #                 },
    #                 3,
    #             ],
    #         },
    #         -1,
    #         None,
    #         -1,
    #     ],
    # }
    # raw = 1
    do(
        raw,
        {"a": 2, "b": 3},
    )
