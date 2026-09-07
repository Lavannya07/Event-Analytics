import streamlit as st
import streamlit.components.v1 as components
import requests
import json

API_URL = "http://localhost:8000/v1"

st.set_page_config(page_title="Event Analytics Dashboard", layout="wide")
st.title("Event Analytics Dashboard")

def get_data(path):
    try:
        res = requests.get(f"{API_URL}/{path}")
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return None

summary = get_data("summary")
bid_data = get_data("bid-price/average") 
peak_data = get_data("peak/hour") 

col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("Total Events", summary.get("total_events", 0))
col2.metric("Unique Devices", summary.get("unique_devices", 0))
col3.metric("Top Country", summary.get("top_country", "N/A"))
col4.metric("Avg Bid Price", bid_data.get("average_bid_price", 0))

if peak_data:
    peak_hours = ", ".join([f"{h}:00" for h in peak_data.keys()])
    col5.metric("Peak Hour", peak_hours)

col6.metric("Date Range", summary.get("date_range"))

st.divider()

st.subheader("Country Search")
country_code = st.text_input("Enter Country Code", value="US").strip().upper()

if country_code:
    country_res = get_data(f"country/{country_code}")
    if country_res and "events" in country_res:
        st.write(f"Events in {country_code}: {country_res['events']}")
    else:
        st.write(f"No events found for country {country_code}")

st.divider()

st.subheader("Top Performers")
col_n1, col_n2, col_n3, col_n4 = st.columns(4)

with col_n1:
    top_n_country = st.number_input("Top N Countries", min_value=1, max_value=50, value=1)
with col_n2:
    top_n_city = st.number_input("Top N Cities", min_value=1, max_value=50, value=1)
with col_n3:
    top_n_campaign = st.number_input("Top N Campaigns", min_value=1, max_value=50, value=1)
with col_n4:
    top_n_publisher = st.number_input("Top N Publishers", min_value=1, max_value=50, value=1)

col_a, col_b, col_c, col_d = st.columns(4)

with col_a:
    countries = get_data(f"countries/top/{top_n_country}")
    if countries:
        st.table(dict(countries))

with col_b:
    cities = get_data(f"cities/top/{top_n_city}")
    if cities:
        st.table(dict(cities))

with col_c:
    campaigns = get_data(f"campaigns/top/{top_n_campaign}")
    if campaigns:
        st.table(dict(campaigns))

with col_d:
    publishers = get_data(f"publishers/top/{top_n_publisher}")
    if publishers:
        st.table(dict(publishers))

st.divider()

col_left , col_right = st.columns(2)

with col_right:
    st.subheader("Events per device")
    st.write("Events Per Device")
    device_events = get_data("events/device")
    if device_events:
            formatted_json = json.dumps(device_events, indent=2)
            components.html(f"""
                <div style="height:250px; overflow-y:auto; background-color:#f8f9fa; border:1px solid #e0e0e0; padding:10px; font-family:monospace; font-size:12px; border-radius:4px;">
                    <pre style="margin:0; white-space:pre-wrap;">{formatted_json}</pre>
                </div>
            """, height=270)
    
with col_left:
    st.subheader("All Unique Publishers")
    all_publishers = get_data("publishers")
    if all_publishers:
        st.write(all_publishers)

st.divider()

st.subheader("Traffic breakdown")
col_left, col_right = st.columns(2)

with col_left:
    st.write("Hourly Distribution")
    hourly = get_data("hourly")
    if hourly:
        st.line_chart(hourly)

with col_right:
    st.write("Daily Distribution")
    daily_data = get_data("daily")
    if daily_data:
        st.line_chart(daily_data)


st.divider()

col_left,col_right = st.columns(2)

with col_left:
    st.subheader("OS Breakdown")
    os_data = get_data("os-split")
    if os_data:
        counts = {os_name: info["count"] for os_name, info in os_data.items()}
        st.bar_chart(counts)

with col_right:
    st.subheader("Missing Values")
    missing_data = get_data("data-quality/missing")
    if missing_data:
        st.table(missing_data)
    else:
        st.write("No missing values found")


st.divider()

st.write("Anomaly Detection")
anomaly_threshold = st.number_input("Enter Threshold", min_value=0, value=0)
anomalies_res = get_data(f"anomalies/{anomaly_threshold}")
if anomalies_res and isinstance(anomalies_res, list):
    st.write(f"Anomalies found: {len(anomalies_res)}")
    formatted_anomalies = json.dumps(anomalies_res, indent=2)
    components.html(f"""
        <div style="height:250px; overflow-y:auto; background-color:#f8f9fa; border:1px solid #e0e0e0; padding:10px; font-family:monospace; font-size:12px; border-radius:4px;">
            <pre style="margin:0; white-space:pre-wrap;">{formatted_anomalies}</pre>
        </div>
    """, height=270)
else:
    st.write("No anomalies found for this threshold")

st.divider()