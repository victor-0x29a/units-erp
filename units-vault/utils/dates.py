from datetime import datetime, timezone, UTC


def get_now():
    return datetime.now(UTC).replace(tzinfo=timezone.utc)


def from_str_to_date(date: str, format: str = "%d/%m/%Y"):
    return datetime.strptime(date, format).replace(tzinfo=timezone.utc)


def from_date_to_str(date: datetime, format: str = "%d/%m/%Y"):
    return date.strftime(format)
