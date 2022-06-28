# pylama:ignore=D100,D101,D102,D103,D104
from __future__ import annotations

import abc
import typing

import pydantic

from algencode import node

from .data import PARAMS

DEFAULT_NAME_INSTRUCTIONS = pydantic.parse_obj_as(
    list[node.Node],
    [
        {"key": "default"},
        "_FY_",
        {"key": "rollyear"},
        "_",
        {"op": "add", "args": [1, {"key": "rollyear"}]},
    ],
)


def _apn_proc(*mid_points: int):
    """Construct a new APN format proceedure."""

    def _slice(a: int | None, b: int | None):
        return {
            "op": "slice",
            "args": [{"key": "_0"}, a, b],
        }

    res = node.Node.parse_obj(
        {
            "op": "fmt",
            "args": [
                "-".join(["{}"] * (1 + len(mid_points))),
                _slice(None, mid_points[0]),
                *[
                    _slice(mid_points[i - 1], mid_points[i])
                    for i in range(1, len(mid_points))
                ],
                _slice(mid_points[-1], None),
            ],
        }
    )
    return res


PROCS = {
    # hyphenated APN formats
    "_apn3332": _apn_proc(3, 6, 9),  # 012-345-678-901
    "_apn3333": _apn_proc(3, 6, 9),
    "_apn332": _apn_proc(3, 6, 8),
    # multiply value by 100, round, and format to specifications
    "_round": node.Node.parse_obj(
        {
            "op": "fmt",
            "args": [
                {
                    "op": "fmt",
                    "args": [
                        "{{:{}{}{}}}",
                        {"key": "_0"},  # allignment (< | > | "")
                        {"key": "_1"},  # padding string (e.g. "0", " ", "")
                        {"key": "_2"},  # width
                    ],
                },
                {
                    "op": "round",
                    "args": [
                        {
                            "op": "mul",
                            "args": [
                                100,
                                {"key": "_3"},  # number to format (e.g. "levy")
                            ],
                        }
                    ],
                },
            ],
        }
    ),
}


def _do(nodes: list[node.Node], vals: node.Vals) -> list[str]:
    return [str(n.reduce(vals, PROCS)) for n in nodes]


class FormatBase(pydantic.BaseModel):
    extension: typing.Literal["txt", "csv", "xlsx"]
    file_name_instructions: list[node.Node] | None
    header_instructions: list[node.Node] | None
    first_line_instructions: list[node.Node] | None
    data_instructions: list[node.Node]

    @abc.abstractmethod
    def _do(self, nodes: list[node.Node], vals: node.Vals) -> str | list[str]:
        ...

    def do(self, vals: node.Vals) -> str | list[str]:
        return self._do(self.data_instructions, vals)

    def do_contents(self, vals: typing.Iterable[node.Vals]) -> list[str | list[str]]:
        it = iter(vals)
        rows = []

        if self.header_instructions:
            rows.append(self._do(self.header_instructions, {}))
        if self.first_line_instructions:
            nodes = self.data_instructions + self.first_line_instructions
            rows.append(self._do(nodes, next(it)))
        rows.extend(map(self.do, it))
        return rows

    def do_file_name(self, vals: node.Vals) -> str | None:
        nodes = self.file_name_instructions or DEFAULT_NAME_INSTRUCTIONS
        name = "".join(_do(nodes, vals))
        return f"{name}.{self.extension}"


class FormatCSV(FormatBase):
    extension: typing.Literal["csv"]
    delim: pydantic.StrictStr

    def _do(self, nodes: list[node.Node], vals: node.Vals) -> str:
        return self.delim.join(_do(nodes, vals))


class FormatTXT(FormatCSV):
    extension: typing.Literal["txt"]
    delim: pydantic.StrictStr = pydantic.Field("", const=True)


class FormatXLSX(FormatBase):
    extension: typing.Literal["xlsx"]

    def _do(self, nodes: list[node.Node], vals: node.Vals) -> list[str]:
        return _do(nodes, vals)


class Format(pydantic.BaseModel):
    __root__: FormatTXT | FormatCSV | FormatXLSX

    def do(self, vals: node.Vals) -> str | list[str]:
        return self.__root__.do(vals)

    def do_contents(self, vals: typing.Iterable[node.Vals]) -> list[str | list[str]]:
        return self.__root__.do_contents(vals)

    def do_file_name(self, vals: node.Vals) -> str | None:
        return self.__root__.do_file_name(vals)


# TODO:
# AMADOR  # Excel
# FRESNO
# KERN
# LOS_ANGELES
# MADERA
# MERCED

if __name__ == "__main__":
    pass
    for params in PARAMS:
        print("-" * 50)
        print(params["name"])
        fmt = Format.parse_obj(params["fmt"])
        fnvals = typing.cast(node.Vals, params["file_name_vals"])

        print(fmt.do_file_name(fnvals))
        print(fmt.do_contents(params["special_charges"]))
        # for _vals in params["special_charges"]:
        #     vals = typing.cast(node.Vals, {**_vals, **file_name_vals})
        #     print(fmt.do(vals))
