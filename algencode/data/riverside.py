# pylama:ignore=D100,D101,D102,D103,D104
from .common import D, FileNameVals, Fmt, SpecialCharge

RIVERSIDE_FMT: Fmt = {
    "aggregation": False,
    "extension": "txt",
    "delim": "",
    "file_name_instructions": None,  # WARN: don't know
    "header_instructions": None,
    "first_line_instructions": None,
    "data_instructions": [
        "      ",
        {"key": "apn"},
        # WARN: much to do
        # CONCAT(
        #     REPEAT(' ', 6),
        #     TRIM(s.apn),
        #     RIGHT(
        #         (LEFT(TRIM(s.apn), 1) * 1)
        #         + (MID(TRIM(s.apn), 2, 1) * 3)
        #         + (MID(TRIM(s.apn), 3, 1) * 7)
        #         + (MID(TRIM(s.apn), 4, 1) * 9)
        #         + (MID(TRIM(s.apn), 5, 1) * 1)
        #         + (MID(TRIM(s.apn), 6, 1) * 3)
        #         + (MID(TRIM(s.apn), 7, 1) * 7)
        #         + (MID(TRIM(s.apn), 8, 1) * 9)
        #         + (RIGHT(s.apn, 1) * 1), 1
        #     ),
        " ",
        {"key": "fundno"},
        "  ",
        {
            "proc": "_round",
            "args": ["", 0, 9, {"key": "levy"}],
        },
    ],
}

RIVERSIDE_FNVALS: FileNameVals = {
    "default": "682174",
    "fundno": "682174",
    "levy_submission_name": None,
}

RIVERSIDE_CHARGES: list[SpecialCharge] = [
    {"apn": "407370001", "levy": D("0.00")},
    {"apn": "407370002", "levy": D("0.00")},
    {"apn": "407370003", "levy": D("644.32")},
    {"apn": "407370004", "levy": D("0.00")},
    {"apn": "407370005", "levy": D("0.00")},
    {"apn": "407370006", "levy": D("0.00")},
    {"apn": "407370007", "levy": D("644.32")},
    {"apn": "407370008", "levy": D("644.32")},
    {"apn": "407370009", "levy": D("644.32")},
    {"apn": "407370010", "levy": D("644.32")},
]
