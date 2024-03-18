# date_util.py
import datetime
import pytz
from dateutil.parser import parse as parse_date

def parse_event_date(date_str):
    """
    Parse event date string into datetime object in UTC timezone.

    Args:
        date_str (str): String representing the event date and time.

    Returns:
        datetime.datetime or None: Parsed datetime object in UTC timezone or None if parsing fails.

    """

    try:
        if "Today" in date_str:
            today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            time_str = date_str.split(' / ')[-1]
            event_time = datetime.datetime.strptime(time_str, '%I:%M %p').time()
            event_datetime = datetime.datetime.combine(today, event_time)
        elif "Tomorrow" in date_str:
            tomorrow = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
            time_str = date_str.split(' / ')[-1]
            event_time = datetime.datetime.strptime(time_str, '%I:%M %p').time()
            event_datetime = datetime.datetime.combine(tomorrow, event_time)
        elif "Starting in" in date_str:
            tokens = date_str.split()
            if "min" in date_str:
                minutes = int(tokens[2])
                event_datetime = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
            elif "hour" in date_str:
                hours = int(tokens[2])
                event_datetime = datetime.datetime.now() + datetime.timedelta(hours=hours)
        else:
            # Fallback to dateutil.parser for other formats
            event_datetime = parse_date(date_str)

        # Convert to US Eastern Time (ET) timezone
        local_timezone = pytz.timezone('US/Eastern')
        event_datetime_local = local_timezone.localize(event_datetime)

        # Convert to UTC timezone
        utc_timezone = pytz.utc
        event_datetime_utc = event_datetime_local.astimezone(utc_timezone)

        return event_datetime_utc
    except ValueError:
        return None
