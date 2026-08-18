import streamlit as st
import requests
import plotly.express as px

# 1. Dashboard Title
st.title("📊 Event Analytics & Anomaly Dashboard")

# Base URL for your running FastAPI backend
API_BASE_URL = "http://127.0.0.1:8000"

# 2. Fetch and Display Summary Metrics
st.header("Overall Summary")
if st.button("Fetch Metrics"):
    response = requests.get(f"{API_BASE_URL}/summary")
    
    if response.status_code == 200:
        data = response.json()
        
        # Create columns for quick metric display
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Events", data.get("total_events", 0))
        col2.metric("Unique Devices", data.get("unique_devices", 0))
        col3.metric("Top Country", data.get("top_country", "N/A"))
    else:
        st.error("Failed to fetch summary from API backend!")

# 3. Interactive Search Section
st.header("Country Event Lookup")
country_code = st.text_input("Enter 2-letter Country Code (e.g. US, SG):", "US")

if country_code:
    res = requests.get(f"{API_BASE_URL}/country/{country_code}")
    if res.status_code == 200:
        st.success(f"Events in {country_code}: {res.json().get('events')}")
    else:
        st.warning("No data found for this country.")