import json
from collections import Counter
from datetime import datetime


def load_events():
    with open("data.json", "r") as file:
        return json.load(file)


def count_events(events):
    return len(events)


def unique_devices(events):
    device_ids = [e.get("device_id") for e in events if e.get("device_id")]
    return len(set(device_ids))

#extra
def unique_publishers(events):
    publishers = [e.get("publisher") for e in events if e.get("publisher")]
    return list(set(publishers))

#extra
def top_cities(events, n):
    cities = [e.get("city") for e in events if e.get("city")]
    return Counter(cities).most_common(n)


def top_publishers(events, n):
    publishers = [e.get("publisher") for e in events if e.get("publisher")]
    return Counter(publishers).most_common(n)


def top_campaigns(events, n):
    campaigns = [e.get("campaign_id") for e in events if e.get("campaign_id")]
    return Counter(campaigns).most_common(n)

#extra
def events_by_country(events, country_code):
    return sum(1 for e in events if e.get("country") == country_code)


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
                ts = datetime.fromisoformat(raw_ts.replace("Z", "+00:00"))
                hour = ts.hour
                hours[hour] = hours.get(hour, 0) + 1
            except ValueError:
                continue
    return hours

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
if __name__ == "__main__":
    events = load_events()

    print("Total events:", count_events(events))
    print("Unique devices:", unique_devices(events))
    print("Unique publishers:", unique_publishers(events))
    print("Top countries:", top_countries(events))
    print("Top cities:", top_cities(events))
    print("Top campaigns:", top_campaigns(events))
    print("Hourly distribution:", hourly_distribution(events))
    print("OS split:", os_split(events))
    print("Average bid price:", average_bid_price(events))
    print("Missing values:", missing_values(events))
    print("Summary:", get_summary(events))












#extra
def os_split(events):
    os_list = []
    for e in events:
        os_list.append(e["os"])
    counter = Counter(os_list)
    total = len(os_list)

    result = {}
    for os_name, count in counter.items():
        percent = round(count / total * 100, 2)
        result[os_name] = {"count": count, "percent": percent}
    return result

#extra
def average_bid_price(events):
    prices = []
    for e in events:
        if e.get("bid_price") is not None:
            prices.append(e["bid_price"])

    if len(prices) == 0:
        return 0
    return round(sum(prices) / len(prices), 2)

#extra
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


