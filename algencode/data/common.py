# pylama:ignore=D100,D101,D102,D103,D104
import datetime
import decimal
import typing

from algencode.common import Json

D = decimal.Decimal


class Fmt(typing.TypedDict):
    aggregation: bool
    extension: typing.Literal["csv", "txt", "xlsx"]
    delim: str | None
    file_name_instructions: Json | None
    header_instructions: Json | None
    first_line_instructions: Json | None
    data_instructions: Json


class SpecialCharge(typing.TypedDict):
    apn: str
    levy: decimal.Decimal


class CommonFileNameVals(typing.TypedDict):
    rollyear: int
    today: datetime.date


class FileNameVals(typing.TypedDict):
    default: str
    fundno: str
    levy_submission_name: str | None
