import logging
from collections import Counter
from datetime import datetime

logging.basicConfig(level=logging.INFO)  #Used for logging
logger = logging.getLogger(__name__)


def count_events(events):  # Returns the total events count
    return len(events)


def unique_devices(events):  # Returns the total number of unique devices 
    device_ids = [e.get("device_id") for e in events if e.get("device_id")]
    return len(set(device_ids))


def unique_publishers(events):  # returns the unique publishers 
    publishers = [e.get("publisher") for e in events if e.get("publisher")]
    return list(set(publishers))


def top_cities(events, n):  # Calculates the top cities based on the event count
    cities = [e.get("city") for e in events if e.get("city")]
    return Counter(cities).most_common(n)


def top_publishers(events, n):  # Calculates the top publishers based on the event count
    publishers = [e.get("publisher") for e in events if e.get("publisher")]
    return Counter(publishers).most_common(n)


def top_campaigns(events, n):  # Calculates the top campaigns based on the event count
    campaigns = [e.get("campaign_id") for e in events if e.get("campaign_id")]
    return Counter(campaigns).most_common(n)


def events_by_country(events, country_code):  # Gives the event count of the country code
    return sum(1 for e in events if e.get("country") == country_code.upper())
  
def events_by_device(events):  # Returns the total number of events for each unique device
    devices = [e.get("device_id") for e in events if e.get("device_id")]
    return Counter((devices))

def top_countries(events, n):  # Calculates the top n countries based on the events count
    countries = [e.get("country") for e in events if e.get("country")]
    counter = Counter(countries)
    return counter.most_common(n)


def hourly_distribution(events):  # Calculates the count of events per hour (0-23)
    hours = {}
    skipped = 0
    for e in events:
        raw_ts = e.get("timestamp")
        if raw_ts and isinstance(raw_ts, str):
            try:
                ts = datetime.fromisoformat(raw_ts)
                hour = ts.hour
                hours[hour] = hours.get(hour, 0) + 1
            except ValueError:
                skipped += 1
                continue
    if skipped:
        logger.warning(f"hourly_distribution: skipped {skipped} events with unparsable timestamps")
    return dict(sorted(hours.items()))

def daily_distribution(events):  # Calculates the count of events for each day
    days = {}
    skipped = 0
    for e in events:
        raw_ts = e.get("timestamp")
        if raw_ts and isinstance(raw_ts, str):
            try:
                ts = datetime.fromisoformat(raw_ts)
                date_str = ts.strftime("%Y-%m-%d")
                days[date_str] = days.get(date_str, 0) + 1
            except ValueError:
                skipped += 1
                continue
    if skipped:
        logger.warning(f"daily_distribution: skipped {skipped} events with unparsable timestamps")
    return days

 
def os_split(events):  # Returns the percentage of every unique os device
    os_list = []
    for e in events:
        os_name = e.get("os")
        if os_name is None:
            os_name = "Unknown"
        os_list.append(str(os_name))
    total = len(os_list)
    if total == 0:
        logger.warning("os_split: called with 0 events")
        return {}
    counter = Counter(os_list)
    result = {}
    for os_name, count in counter.items():
        percent = round((count / total) * 100, 2)
        result[os_name] = {"count": count, "percent": percent}
    return result


def average_bid_price(events):  # Calculates the average bid price 
    prices = []
    for e in events:
        if e.get("bid_price") is not None:
            prices.append(e["bid_price"])

    if len(prices) == 0:
        logging.warning("No bid prices found")
        return 0
    return round(sum(prices) / len(prices), 2)


def missing_values(events):  # Calculates the missing values from the data for every field in the event
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
    if missing:
        logger.info(f"missing_values: found missing fields -> {missing}")
    return missing


def get_summary(events): # Returns the summary of the data
    top_country = top_countries(events, 1)
    top_publisher = top_publishers(events, 1)
    top_campaign = top_campaigns(events, 1)
    timestamps = [e.get("timestamp") for e in events if e.get("timestamp")]
    if timestamps:
        min_date = min(timestamps)[:10]
        max_date = max(timestamps)[:10]
        date_range = f"{min_date} to {max_date}" if min_date != max_date else min_date
    return {
        "total_events": count_events(events),
        "unique_devices": unique_devices(events),
        "top_country": top_country[0][0] if top_country else None,
        "top_publisher": top_publisher[0][0] if top_publisher else None,
        "top_campaign": top_campaign[0][0] if top_campaign else None,
        "date_range": date_range 
    }

def peak_hour(events):   # Returns the peak traffic hour/hours based on the event count
    total_hours = hourly_distribution(events)
    top_count = max(total_hours.values())
    hours = [hour[0] for hour in total_hours.items() if hour[1] == top_count]
    peakhour = {}
    for hour in hours:
        peakhour.update({hour:top_count})
    return peakhour


def anomalies(events, threshold: int):
    if threshold < 1:
        logger.warning("Threshold value entered is less than 1")
        return "The threshold value should be greater than 1"
    counts = {}
    for e in events:
        publisher = e.get("publisher")
        raw_ts = e.get("timestamp")
        if publisher and isinstance(raw_ts, str):
            ts = datetime.fromisoformat(raw_ts)
            date_str = ts.strftime("%Y-%m-%d")
            if publisher not in counts:
                counts[publisher] = {}
            counts[publisher][date_str] = counts[publisher].get(date_str, 0) + 1
    flagged = []
    for publisher, daily_data in counts.items():
        dates = sorted(daily_data.keys())
        for i in range(1, len(dates)):
            prev_date, curr_date = dates[i - 1], dates[i]
            prev_cnt, curr_cnt = daily_data[prev_date], daily_data[curr_date]
            increase = curr_cnt - prev_cnt
            if increase >= threshold:
                flagged.append({
                    "publisher": publisher,
                    "previous_date": prev_date,
                    "previous_count": prev_cnt,
                    "current_date": curr_date,
                    "current_count": curr_cnt,
                    "increase": increase
                })
    return flagged