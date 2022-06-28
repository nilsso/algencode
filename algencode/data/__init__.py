# pylama:ignore=D100,D101,D102,D103,D104
import datetime

from .amador import *
from .common import CommonFileNameVals
from .imperial import *
from .orange import *
from .riverside import *
from .san_bernardino import *
from .san_diego import *
from .santa_clara import *
from .yolo import *

COMMON_FNVALS: CommonFileNameVals = {
    "rollyear": 2021,
    "today": datetime.date.today(),
}


PARAMS = [
    {
        "name": "Amador",
        "fmt": AMADOR_FMT,
        "file_name_vals": {**AMADOR_FNVALS, **COMMON_FNVALS},
        "special_charges": AMADOR_CHARGES,
    },
    {
        "name": "Imperial",
        "fmt": IMPERIAL_FMT,
        "file_name_vals": {**IMPERIAL_FNVALS, **COMMON_FNVALS},
        "special_charges": IMPERIAL_CHARGES,
    },
    {
        "name": "Orange",
        "fmt": ORANGE_FMT,
        "file_name_vals": {**ORANGE_FNVALS, **COMMON_FNVALS},
        "special_charges": ORANGE_CHARGES,
    },
    {
        "name": "Riverside",
        "fmt": RIVERSIDE_FMT,
        "file_name_vals": {**RIVERSIDE_FNVALS, **COMMON_FNVALS},
        "special_charges": RIVERSIDE_CHARGES,
    },
    {
        "name": "San Bernardino",
        "fmt": SAN_BERNARDINO_FMT,
        "file_name_vals": {**SAN_BERNARDINO_FNVALS, **COMMON_FNVALS},
        "special_charges": SAN_BERNARDINO_CHARGES,
    },
    {
        "name": "San Diego",
        "fmt": SAN_DIEGO_FMT,
        "file_name_vals": {**SAN_DIEGO_FNVALS, **COMMON_FNVALS},
        "special_charges": SAN_DIEGO_CHARGES,
    },
    {
        "name": "Santa Clara",
        "fmt": SANTA_CLARA_FMT,
        "file_name_vals": {**SANTA_CLARA_FNVALS, **COMMON_FNVALS},
        "special_charges": SANTA_CLARA_CHARGES,
    },
    {
        "name": "Yolo",
        "fmt": YOLO_FMT,
        "file_name_vals": {**YOLO_FNVALS, **COMMON_FNVALS},
        "special_charges": YOLO_CHARGES,
    },
]