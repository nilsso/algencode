# pylama:ignore=D100,D101,D102,D103,D104
from .common import D, FileNameVals, Fmt, SpecialCharge

MADERA_FMT: Fmt = {
    "aggregation": False,
    "extension": "xlsx",
    "delim": None,
    "file_name_instructions": None,
    "header_instructions": [
        "Assessment #",
        "Tax",
        "Tax Code",
    ],
    "first_line_instructions": None,
    "data_instructions": [
        {"key": "apn"},
        {"key": "levy"},
        {"key": "fundno"},
    ],
}

MADERA_FNVALS: FileNameVals = {
    "default": "83300",
    "fundno": "83300",
    "levy_submission_name": None,
}

MADERA_CHARGES: list[SpecialCharge] = [
    {"apn": "080021001000", "levy": D("369.20")},
    {"apn": "080021002000", "levy": D("473.40")},
    {"apn": "080021003000", "levy": D("569.60")},
    {"apn": "080021004000", "levy": D("319.60")},
    {"apn": "080021005000", "levy": D("436.00")},
    {"apn": "080021006000", "levy": D("364.80")},
    {"apn": "080021007000", "levy": D("531.60")},
    {"apn": "080021008000", "levy": D("473.40")},
    {"apn": "080021009000", "levy": D("319.60")},
    {"apn": "080021010000", "levy": D("436.00")},
]
