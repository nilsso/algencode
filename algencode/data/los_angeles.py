# pylama:ignore=D100,D101,D102,D103,D104
from .common import D, FileNameVals, Fmt, SpecialCharge

LOS_ANGELES_FMT: Fmt = {
    "aggregation": False,
    "extension": "xlsx",
    "delim": None,
    "file_name_instructions": None,
    "header_instructions": None,
    "first_line_instructions": [
        {
            "op": "fmt",
            "args": [
                "{}.{}",
                {"op": "slice", "args": [{"key": "fundno"}, -2, None]},
                {"op": "slice", "args": [{"key": "fundno"}, None, -2]},
            ],
        },
    ],
    "data_instructions": [
        {"key": "apn"},
        {"key": "levy"},
    ],
}

LOS_ANGELES_FNVALS: FileNameVals = {
    "default": "44062",
    "fundno": "44062",
    "levy_submission_name": None,
}

LOS_ANGELES_CHARGES: list[SpecialCharge] = [
    {"apn": "3247045033", "levy": D("913.86")},
    {"apn": "3247045034", "levy": D("913.86")},
    {"apn": "3247045035", "levy": D("913.86")},
    {"apn": "3247045036", "levy": D("913.86")},
    {"apn": "3247045037", "levy": D("913.86")},
    {"apn": "3247045038", "levy": D("913.86")},
    {"apn": "3247045039", "levy": D("913.86")},
    {"apn": "3247045040", "levy": D("913.86")},
    {"apn": "3247045041", "levy": D("913.86")},
    {"apn": "3247045042", "levy": D("913.86")},
]
