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
    {"apn": "1026131050000", "levy": D("0.00")},
    {"apn": "1026131060000", "levy": D("0.00")},
    {"apn": "1026131070000", "levy": D("0.00")},
    {"apn": "1026131080000", "levy": D("0.00")},
    {"apn": "1026141060000", "levy": D("0.00")},
    {"apn": "1026141070000", "levy": D("0.00")},
    {"apn": "1026141080000", "levy": D("0.00")},
    {"apn": "1026141090000", "levy": D("0.00")},
    {"apn": "1026151010000", "levy": D("1157.70")},
    {"apn": "1026151020000", "levy": D("1447.70")},
]
