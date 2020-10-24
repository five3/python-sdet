from datetime import datetime, date


def warp_date_field(data):
    for item in data:
        for k, v in item.items():
            if isinstance(v, date):
                item[k] = v.strftime("%Y-%m-%d")
            if isinstance(v, datetime):
                item[k] = v.strftime("%Y-%m-%d %H:%M:%S")
    return data
