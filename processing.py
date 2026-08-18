from collections import Counter
from datetime import datetime


def count_events(events):
    return len(events)


def unique_devices(events):
    device_ids = [e.get("device_id") for e in events if e.get("device_id")]
    return len(set(device_ids))


def unique_publishers(events):
    publishers = [e.get("publisher") for e in events if e.get("publisher")]
    return list(set(publishers))


def top_cities(events, n):
    cities = [e.get("city") for e in events if e.get("city")]
    return Counter(cities).most_common(n)


def top_publishers(events, n):
    publishers = [e.get("publisher") for e in events if e.get("publisher")]
    return Counter(publishers).most_common(n)


def top_campaigns(events, n):
    campaigns = [e.get("campaign_id") for e in events if e.get("campaign_id")]
    return Counter(campaigns).most_common(n)


def events_by_country(events, country_code):
    return sum(1 for e in events if e.get("country") == country_code.upper())


def top_countries(events, n):
    countries = [e.get("country") for e in events if e.get("country")]
    counter = Counter(countries)
    return counter.most_common(n)


def hourly_distribution(events):
    hours = {}
    for e in events:
        raw_ts = e.get("timestamp")
        if raw_ts and isinstance(raw_ts, str):
            try:
                ts = datetime.fromisoformat(raw_ts)
                hour = ts.hour
                hours[hour] = hours.get(hour, 0) + 1
            except ValueError:
                continue
    return hours 

def daily_distribution(events):
    days = {}
    for e in events:
        raw_ts = e.get("timestamp")
        if raw_ts and isinstance(raw_ts, str):
            try:
                ts = datetime.fromisoformat(raw_ts)
                date_str = ts.strftime("%Y-%m-%d") #formats the date to that form
                days[date_str] = days.get(date_str, 0) + 1
            except ValueError:
                continue
    return days


def os_split(events):
    os_list = []
    for e in events:
        os_name = e.get("os")
        if os_name is None:
            os_name = "Unknown"
        os_list.append(str(os_name))
    total = len(os_list)
    if total == 0:
        return {}
    counter = Counter(os_list)
    result = {}
    for os_name, count in counter.items():
        percent = round((count / total) * 100, 2)
        result[os_name] = {"count": count, "percent": percent}
    return result


def average_bid_price(events):
    prices = []
    for e in events:
        if e.get("bid_price") is not None:
            prices.append(e["bid_price"])

    if len(prices) == 0:
        return 0
    return round(sum(prices) / len(prices), 2)


def missing_values(events):
    all_keys = ["timestamp", "device_id", "publisher", "country", "city",
                "ad_id", "campaign_id", "event_type", "bid_price", "os"]

    missing = {}
    for key in all_keys:
        count = 0
        for e in events:
            if e.get(key) is None:
                count += 1
        if count > 0:
            missing[key] = count
    return missing


def get_summary(events):
    top_country = top_countries(events, 1)
    top_publisher = top_publishers(events, 1)
    top_campaign = top_campaigns(events, 1)

    return {
        "total_events": count_events(events),
        "unique_devices": unique_devices(events),
        "top_country": top_country[0][0] if top_country else None,
        "top_publisher": top_publisher[0][0] if top_publisher else None,
        "top_campaign": top_campaign[0][0] if top_campaign else None,
    }