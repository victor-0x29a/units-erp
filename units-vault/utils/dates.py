import datetime


def get_now():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=datetime.timezone.utc)


def from_str_to_date(date: str, format: str = "%d/%m/%Y"):
    return datetime.datetime.strptime(date, format).replace(tzinfo=datetime.timezone.utc)


def from_date_to_str(date: datetime, format: str = "%d/%m/%Y"):
    return date.strftime(format)
