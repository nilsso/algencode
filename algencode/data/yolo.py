# pylama:ignore=D100,D101,D102,D103,D104
from .common import D, FileNameVals, Fmt, SpecialCharge

YOLO_FMT: Fmt = {
    "aggregation": False,
    "extension": "csv",
    "delim": "\t",
    "file_name_instructions": None,
    "header_instructions": None,
    "first_line_instructions": None,
    "data_instructions": [
        {"key": "apn"},
        {"op": "fmt", "args": ["{:.2f}", {"key": "levy"}]},
        {"key": "fundno"},
        {"op": "fmt", "args": ["{:<10}", {"key": "levy_submission_name"}]},
    ],
}

YOLO_FNVALS: FileNameVals = {
    "default": "52633",
    "fundno": "52633",
    "levy_submission_name": "SL LLD",
}

YOLO_CHARGES: list[SpecialCharge] = [
    {"apn": "041231002000", "levy": D("592.08")},
    {"apn": "041231003000", "levy": D("592.08")},
    {"apn": "041231004000", "levy": D("592.08")},
    {"apn": "041231005000", "levy": D("592.08")},
    {"apn": "041231006000", "levy": D("592.08")},
    {"apn": "041231007000", "levy": D("592.08")},
    {"apn": "041231008000", "levy": D("592.08")},
    {"apn": "041231009000", "levy": D("592.08")},
    {"apn": "041231010000", "levy": D("592.08")},
    {"apn": "041231011000", "levy": D("592.08")},
]
