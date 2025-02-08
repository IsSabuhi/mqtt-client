from datetime import datetime as dt

def convert_timestamp_to_datetime(timestamp):
    return dt.fromtimestamp(timestamp)


print(convert_timestamp_to_datetime(1738674600))