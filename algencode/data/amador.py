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
        # {"
    ],
}

AMADOR_FNVALS: FileNameVals = {
    "default": "74000",
    "fundno": "74000",
    "levy_submission_name": "I-CFD04-1",
}

AMADOR_CHARGES: list[SpecialCharge] = [
    {"apn": "001150017000", "levy": D("0.00")},
    {"apn": "001170024000", "levy": D("0.00")},
    {"apn": "001170029000", "levy": D("0.00")},
    {"apn": "001170030000", "levy": D("0.00")},
    {"apn": "001180027000", "levy": D("1442.56")},
    {"apn": "001180028000", "levy": D("0.00")},
    {"apn": "001200012000", "levy": D("0.00")},
    {"apn": "003420126000", "levy": D("693.54")},
    {"apn": "003420127000", "levy": D("0.00")},
    {"apn": "003722018000", "levy": D("0.00")},
]
