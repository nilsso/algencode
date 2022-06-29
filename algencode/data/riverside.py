# pylama:ignore=D100,D101,D102,D103,D104
from .common import D, FileNameVals, Fmt, SpecialCharge

RIVERSIDE_FMT: Fmt = {
    "aggregation": False,
    "extension": "csv",
    "delim": ",",
    "file_name_instructions": [{"key": "fundno"}],
    "header_instructions": [
        "PIN",
        "SAShortDesc",
        "Amount",
    ],
    "first_line_instructions": None,
    "data_instructions": [
        {"key": "apn"},
        {
            "op": "fmt",
            "args": [
                "{}-{}-FC",
                {
                    "op": "slice",
                    "args": [{"key": "fundno"}, None, 2],
                },
                {
                    "op": "slice",
                    "args": [{"key": "fundno"}, 2, None],
                },
            ],
        },
        {"key": "levy"},
    ],
}

RIVERSIDE_FNVALS: FileNameVals = {
    "default": "682174",
    "fundno": "682174",
    "levy_submission_name": None,
}

RIVERSIDE_CHARGES: list[SpecialCharge] = [
    {"apn": "407370001", "levy": D("644.32")},
    {"apn": "407370002", "levy": D("644.32")},
    {"apn": "407370003", "levy": D("644.32")},
    {"apn": "407370004", "levy": D("644.32")},
    {"apn": "407370005", "levy": D("644.32")},
    {"apn": "407370006", "levy": D("644.32")},
    {"apn": "407370007", "levy": D("644.32")},
    {"apn": "407370008", "levy": D("644.32")},
    {"apn": "407370009", "levy": D("644.32")},
    {"apn": "407370010", "levy": D("644.32")},
]
