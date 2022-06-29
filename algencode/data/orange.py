# pylama:ignore=D100,D101,D102,D103,D104
from .common import D, FileNameVals, Fmt, SpecialCharge

ORANGE_FMT: Fmt = {
    "aggregation": False,
    "extension": "csv",
    "delim": "\t",
    "file_name_instructions": None,  # WARN: don't know
    "header_instructions": None,
    "first_line_instructions": None,
    "data_instructions": [
        {
            "op": "fmt",
            "args": [
                '"{}"',
                {
                    "op": "slice",
                    "args": [
                        {"key": "fundno"},
                        None,
                        2,
                    ],
                },
            ],
        },
        {"op": "fmt", "args": ['"{}"', {"key": "apn"}]},
        {"op": "fmt", "args": ["{:.2f}", {"key": "levy"}]},
        {
            "op": "fmt",
            "args": [
                '"{}"',
                {
                    "op": "slice",
                    "args": [
                        {"key": "fundno"},
                        2,
                        None,
                    ],
                },
            ],
        },
    ],
}

ORANGE_FNVALS: FileNameVals = {
    "default": "R5060",
    "fundno": "R5060",
    "levy_submission_name": None,
}

ORANGE_CHARGES: list[SpecialCharge] = [
    {"apn": "69142301", "levy": D("7415.50")},
    {"apn": "69142302", "levy": D("7415.50")},
    {"apn": "69142303", "levy": D("8460.68")},
    {"apn": "69142304", "levy": D("7415.50")},
    {"apn": "69142305", "levy": D("8069.98")},
    {"apn": "69142306", "levy": D("8460.68")},
    {"apn": "69142307", "levy": D("7415.50")},
    {"apn": "69142308", "levy": D("8069.98")},
    {"apn": "69142309", "levy": D("8460.68")},
    {"apn": "69142310", "levy": D("7415.50")},
]
