# pylama:ignore=D100,D101,D102,D103,D104
from .common import D, FileNameVals, Fmt, SpecialCharge

SAN_DIEGO_FMT: Fmt = {
    "aggregation": True,
    "extension": "txt",
    "delim": "",
    "file_name_instructions": None,
    "header_instructions": None,
    "first_line_instructions": None,
    "data_instructions": [
        "1",
        {"key": "apn"},
        {"key": "fundno"},
        {
            "op": "fmt",
            "args": [
                "{:<20}",
                {"key": "levy_submission_name"},
            ],
        },
        {
            "proc": "_round",
            "args": ["", 0, 9, {"key": "levy"}],
        },
        "1",
        "                                 ",
    ],
}

SAN_DIEGO_FNVALS: FileNameVals = {
    "default": "608594",
    "fundno": "608594",
    "levy_submission_name": "ADAMS AVE LANDSCAPE",
}

SAN_DIEGO_CHARGES: list[SpecialCharge] = [
    {"apn": "4382400300", "levy": D("446.02")},
    {"apn": "4382512300", "levy": D("312.20")},
    {"apn": "4382512400", "levy": D("312.20")},
    {"apn": "4382521400", "levy": D("401.42")},
    {"apn": "4382521500", "levy": D("214.08")},
    {"apn": "4382521600", "levy": D("223.00")},
    {"apn": "4382521700", "levy": D("267.60")},
    {"apn": "4382521800", "levy": D("133.80")},
    {"apn": "4382601300", "levy": D("178.40")},
    {"apn": "4382601600", "levy": D("178.40")},
]
