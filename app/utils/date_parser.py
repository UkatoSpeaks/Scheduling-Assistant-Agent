from datetime import datetime, timedelta

from dateutil.parser import parse


def normalize_date(date_input: str) -> str:
    """
    Convert natural language dates into YYYY-MM-DD format.

    Examples:
        today
        tomorrow
        day after tomorrow
        2026-07-15
        July 15
        15 July 2026
    """

    text = date_input.strip().lower()
    today = datetime.today()

    if text == "today":
        return today.strftime("%Y-%m-%d")

    if text == "tomorrow":
        return (today + timedelta(days=1)).strftime("%Y-%m-%d")

    if text == "day after tomorrow":
        return (today + timedelta(days=2)).strftime("%Y-%m-%d")

    try:
        parsed = parse(date_input, fuzzy=True)

        # If the year isn't provided, assume the current year.
        if parsed.year == 1900:
            parsed = parsed.replace(year=today.year)

        return parsed.strftime("%Y-%m-%d")

    except Exception:
        raise ValueError(f"Invalid date: {date_input}")