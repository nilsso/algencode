# pylama:ignore=D100,D101,D102,D103,D104
from .common import D, FileNameVals, Fmt, SpecialCharge

AMADOR_FMT: Fmt = {
    "aggregation": False,
    "extension": "xlsx",
    "delim": None,
    "file_name_instructions": None,
    "header_instructions": [
        "apn",
        "tax",
        "roll code",
    ],
    "first_line_instructions": None,
    "data_instructions": [
        {
            "proc": "_apn3333",
            "args": [
                {"key": "apn"},
            ],
        },
        {"key": "levy"},
        {"key": "fundno"},
        "CFDF",
    ],
}

AMADOR_FNVALS: FileNameVals = {
    "default": "74000",
    "fundno": "74000",
    "levy_submission_name": None,
}

AMADOR_CHARGES: list[SpecialCharge] = [
    {"apn": "001180027000", "levy": D("1442.56")},
    {"apn": "003420126000", "levy": D("693.54")},
    {"apn": "007070060000", "levy": D("1456.42")},
    {"apn": "007130007000", "levy": D("693.54")},
    {"apn": "008080022000", "levy": D("2774.16")},
    {"apn": "008210028000", "levy": D("3758.98")},
    {"apn": "008210032000", "levy": D("693.54")},
    {"apn": "008210035000", "levy": D("693.54")},
    {"apn": "011100037000", "levy": D("693.54")},
    {"apn": "011320004000", "levy": D("693.54")},
]
