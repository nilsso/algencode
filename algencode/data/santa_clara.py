# pylama:ignore=D100,D101,D102,D103,D104
from .common import D, FileNameVals, Fmt, SpecialCharge

SANTA_CLARA_FMT: Fmt = {
    "aggregation": False,
    "extension": "txt",
    "delim": "",
    "file_name_instructions": [
        "SA_",
        {
            "op": "date",
            "args": ["%Y%m%d", {"key": "today"}],
        },
        "_",
        {"key": "fundno"},
    ],
    "header_instructions": None,
    "first_line_instructions": None,
    "data_instructions": [
        {"key": "apn"},
        {"op": "fmt", "args": ["{:>04}", {"key": "fundno"}]},
        {
            "proc": "_round",
            "args": ["", 0, 8, {"key": "levy"}],
        },
    ],
}

SANTA_CLARA_FNVALS: FileNameVals = {
    "default": "821",
    "fundno": "821",
    "levy_submission_name": None,
}

SANTA_CLARA_CHARGES: list[SpecialCharge] = [
    {"apn": "36605023", "levy": D("262.64")},
    {"apn": "36605024", "levy": D("262.64")},
    {"apn": "36605025", "levy": D("262.64")},
    {"apn": "36605026", "levy": D("262.64")},
    {"apn": "36605027", "levy": D("262.64")},
    {"apn": "36605028", "levy": D("262.64")},
    {"apn": "36605029", "levy": D("262.64")},
    {"apn": "36605030", "levy": D("262.64")},
    {"apn": "36605031", "levy": D("262.64")},
    {"apn": "36605032", "levy": D("262.64")},
]
