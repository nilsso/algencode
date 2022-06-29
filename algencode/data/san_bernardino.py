# pylama:ignore=D100,D101,D102,D103,D104
from .common import D, FileNameVals, Fmt, SpecialCharge

SAN_BERNARDINO_FMT: Fmt = {
    "aggregation": False,
    "extension": "txt",
    "delim": "",
    "file_name_instructions": None,
    "header_instructions": None,
    "first_line_instructions": None,
    "data_instructions": [
        "PI320",
        "           ",
        {"op": "date", "args": ["%y%m%d", {"key": "today"}]},
        "            ",
        "D",
        "      ",
        {"key": "fundno"},
        {"op": "mod", "args": [{"key": "rollyear"}, 100]},
        {"key": "apn"},
        "01",
        {
            "proc": "_round",
            "args": ["", 0, 11, {"key": "levy"}],
        },
    ],
}

SAN_BERNARDINO_FNVALS: FileNameVals = {
    "default": "VQ66ST01",
    "fundno": "VQ66ST01",
    "levy_submission_name": "ADAMS AVE LANDSCAPE",
}

SAN_BERNARDINO_CHARGES: list[SpecialCharge] = [
    {"apn": "1026151010000", "levy": D("1157.70")},
    {"apn": "1026151020000", "levy": D("1447.70")},
    {"apn": "1026151030000", "levy": D("1157.70")},
    {"apn": "1026151040000", "levy": D("1157.70")},
    {"apn": "1026151050000", "levy": D("1447.70")},
    {"apn": "1026151060000", "levy": D("1157.70")},
    {"apn": "1026151070000", "levy": D("1447.70")},
    {"apn": "1026151080000", "levy": D("1157.70")},
    {"apn": "1026151090000", "levy": D("1447.70")},
    {"apn": "1026151100000", "levy": D("1157.70")},
]
