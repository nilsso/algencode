# pylama:ignore=D100,D101,D102,D103,D104
from .common import D, FileNameVals, Fmt, SpecialCharge

MERCED_FMT: Fmt = {
    "aggregation": False,
    "extension": "xlsx",
    "delim": None,
    "file_name_instructions": None,
    "header_instructions": None,
    "first_line_instructions": None,
    "data_instructions": [
        {"key": "apn"},
        {"key": "levy"},
        {"key": "fundno"},
    ],
}

MERCED_FNVALS: FileNameVals = {
    "default": "51899",
    "fundno": "51899",
    "levy_submission_name": None,
}

MERCED_CHARGES: list[SpecialCharge] = [
    {"apn": "027011017000", "levy": D("504.76")},
    {"apn": "027011018000", "levy": D("504.76")},
    {"apn": "027011019000", "levy": D("504.76")},
    {"apn": "027011020000", "levy": D("504.76")},
    {"apn": "027012013000", "levy": D("504.76")},
    {"apn": "027012014000", "levy": D("504.76")},
    {"apn": "027012015000", "levy": D("504.76")},
    {"apn": "027012016000", "levy": D("504.76")},
    {"apn": "027013011000", "levy": D("504.76")},
    {"apn": "027013012000", "levy": D("504.76")},
]
