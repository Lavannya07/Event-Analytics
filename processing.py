import json
from collections import Counter
from datetime import datetime


def load_events(data):
    return json.load(open("sample_data.json"))


def count_events(events):
    return len(events)


def unique_devices(events):
    device_ids = []
    for e in events:
        device_ids.append(e["device_id"])
    return len(set(device_ids))


def unique_publishers(events):
    publishers = []
    for e in events:
        publishers.append(e["publisher"])
    return list(set(publishers))


def top_countries(events, n=10):
    countries = []
    for e in events:
        countries.append(e["country"])
    counter = Counter(countries)
    return counter.most_common(n)


def top_cities(events, n=10):
    cities = []
    for e in events:
        cities.append(e["city"])
    counter = Counter(cities)
    return counter.most_common(n)


def top_publishers(events, n=10):
    publishers = []
    for e in events:
        publishers.append(e["publisher"])
    counter = Counter(publishers)
    return counter.most_common(n)


def top_campaigns(events, n=10):
    campaigns = []
    for e in events:
        campaigns.append(e["campaign_id"])
    counter = Counter(campaigns)
    return counter.most_common(n)


def events_by_country(events, country_code):
    count = 0
    for e in events:
        if e["country"] == country_code:
            count += 1
    return count


def hourly_distribution(events):
    hours = {}
    for e in events:
        ts = datetime.fromisoformat(e["timestamp"].replace("Z", "+00:00"))
        hour = ts.hour
        if hour not in hours:
            hours[hour] = 0
        hours[hour] += 1
    return hours


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