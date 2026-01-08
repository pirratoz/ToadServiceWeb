from datetime import timedelta
import re


def parse_interval(interval_str: str) -> timedelta:
    # interval_str = 1 week 3 days 1 hours 1 minutes 1 sec
    kwargs = {"weeks": 0, "days": 0, "hours": 0, "minutes": 0, "seconds": 0}

    pattern = r"(\d+)\s*(week|weeks|day|days|hour|hours|minute|minutes|min|second|seconds|sec|secs)"
    matches = re.findall(pattern, interval_str, flags=re.IGNORECASE)

    for value, unit in matches:
        value = int(value)
        unit = unit.lower()
        if unit.startswith("week"):
            kwargs["weeks"] += value
        elif unit.startswith("day"):
            kwargs["days"] += value
        elif unit.startswith("hour"):
            kwargs["hours"] += value
        elif unit.startswith("minute") or unit.startswith("min"):
            kwargs["minutes"] += value
        elif unit.startswith("second") or unit.startswith("sec"):
            kwargs["seconds"] += value

    return timedelta(**kwargs)
