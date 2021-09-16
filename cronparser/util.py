from typing import Dict

from cronparser.models.exceptions import BadFormat

_DOW_TO_INT_MAP = {
    "mon": "1",
    "tue": "2",
    "wed": "3",
    "thu": "4",
    "fri": "5",
    "sat": "6",
    "sun": "0"
}


def dow_str_to_int(dow_str: str) -> str:
    lowered = dow_str.lower()
    for k, v in _DOW_TO_INT_MAP.items():
        lowered = lowered.replace(k, v)

    return lowered


def cron_to_dict(data: str) -> Dict[str, str]:
    try:
        minute, hour, dom, month, dow, command = data.split(" ")
        return dict(
            minute=minute,
            hour=hour,
            dom=dom,
            month=month,
            dow=dow_str_to_int(dow),
            command=command
        )
    except ValueError:
        raise BadFormat(f"Cron {data} is not is a valid cron format")