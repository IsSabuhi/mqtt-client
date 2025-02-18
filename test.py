from datetime import datetime as dt
import pytz

def convert_timestamp_to_datetime(ts, tz):
    timestamp = ts
    timezone = pytz.timezone(tz)
    dt_object = dt.fromtimestamp(timestamp, tz=timezone)
    return f"{dt_object.date()} {dt_object.time()}"



print(convert_timestamp_to_datetime(1739268000,'UTC'))
