# pylama:ignore=D100,D101,D102,D103,D104
from .common import D, FileNameVals, Fmt, SpecialCharge

IMPERIAL_FMT: Fmt = {
    "aggregation": False,
    "extension": "csv",
    "delim": ",",
    "file_name_instructions": None,  # WARN: don't know
    "header_instructions": None,
    "first_line_instructions": None,
    "data_instructions": [
        {"op": "fmt", "args": ['"{}"', {"key": "apn"}]},
        {"op": "fmt", "args": ['"{:.2f}"', {"key": "levy"}]},
        {"op": "fmt", "args": ['"{}"', {"key": "fundno"}]},
        {"op": "fmt", "args": ['"{}"', {"key": "levy_submission_name"}]},
    ],
}

IMPERIAL_FNVALS: FileNameVals = {
    "default": "91750",
    "fundno": "91750",
    "levy_submission_name": "I-CFD04-1",
}

IMPERIAL_CHARGES: list[SpecialCharge] = [
    {"apn": "044220087000", "levy": D("0.00")},
    {"apn": "044220088000", "levy": D("0.00")},
    {"apn": "044651001000", "levy": D("1610.00")},
    {"apn": "044651002000", "levy": D("1610.00")},
    {"apn": "044651003000", "levy": D("1610.00")},
    {"apn": "044651004000", "levy": D("1610.00")},
    {"apn": "044651005000", "levy": D("1610.00")},
    {"apn": "044651006000", "levy": D("1610.00")},
    {"apn": "044651007000", "levy": D("1610.00")},
    {"apn": "044651008000", "levy": D("1610.00")},
]
