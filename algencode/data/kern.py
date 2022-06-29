# pylama:ignore=D100,D101,D102,D103,D104
from .common import D, FileNameVals, Fmt, SpecialCharge

KERN_FMT: Fmt = {
    "aggregation": False,
    "extension": "xlsx",
    "delim": None,
    "file_name_instructions": None,
    "header_instructions": [
        "FUND",
        "ATN",
        "ACTION CODE",
        "RATE CODE",
        "MULTIPLIER",
        "AMOUNT",
    ],
    "first_line_instructions": None,
    "data_instructions": [
        {"key": "fundno"},
        {"key": "apn"},
        "C",
        "00",
        None,
        {"key": "levy"},
    ],
}

KERN_FNVALS: FileNameVals = {
    "default": "78024",
    "fundno": "78024",
    "levy_submission_name": None,
}

KERN_CHARGES: list[SpecialCharge] = [
    {"apn": "51648102003", "levy": D("1873")},
    {"apn": "51648103006", "levy": D("1873")},
    {"apn": "51648104009", "levy": D("1873")},
    {"apn": "51648105002", "levy": D("1873")},
    {"apn": "51648106005", "levy": D("1873")},
    {"apn": "51648107008", "levy": D("1873")},
    {"apn": "51648108001", "levy": D("1873")},
    {"apn": "51648109004", "levy": D("1873")},
    {"apn": "51648110006", "levy": D("1873")},
    {"apn": "51648111009", "levy": D("1873")},
]
