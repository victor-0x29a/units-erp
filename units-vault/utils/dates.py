from datetime import datetime, timezone


def get_now():
    return datetime.now().replace(tzinfo=timezone.utc)


def parse_date(date: str, format: str = "%d/%m/%Y"):
    return datetime.strptime(date, format).replace(tzinfo=timezone.utc)
