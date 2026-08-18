# Event Analytics API

A RESTful API built with FastAPI that ingests adtech event-level JSON data from AWS S3, processes aggregations in memory, and exposes query endpoints along with real-time analytics.

---

## Project Overview

This service simulates an AdTech data engineering platform pipeline:
- **Ingestion:** Fetches raw event logs in JSON format directly from Amazon S3.
- **Processing:** Performs in-memory aggregations and metrics calculations (e.g., event counting, unique device tracking, hourly distributions).
- **Serving:** Exposes RESTful API endpoints for downstream querying and reporting.

---

## Architecture

[ AWS S3 ] ---> [ Python Loader ] ---> [ In-Memory Aggregations ] ---> [ FastAPI ] ---> [ REST API / Postman ]

---

## Key Assumptions

- **In-Memory Storage:** To maximize throughput and simplify operations, no database is used; event logs are ingested and stored entirely in memory using standard Python data structures .
- **Data Quality & Fallbacks:** Unset or missing JSON fields (e.g., `city` or `bid_price`) fall back safely (`"UNKNOWN"`, `0.0`) without dropping event records.
- **Timestamp Format:** All event timestamps are parsed assuming **UTC ISO 8601** format (e.g., `2026-07-25T10:15:00Z`).

---

## How to Run

### 1. Local Setup

```bash
# Clone the repository
git clone [https://github.com/your-username/event-analytics-api.git]
cd event-analytics-api

# Create & activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install uvicorn fastapi boto3

# Start the FastAPI server
uvicorn main:app --reload

# If FastAPI server already running then kill it
lsof -i:[Portnumber]  # Enter the port number in the URL
kill -9 [PID]  # Enter the PID value returned
 
# Configure AWS environment variables
export AWS_ACCESS_KEY_ID="your_access_key"
export AWS_SECRET_ACCESS_KEY="your_secret_key"
export S3_BUCKET_NAME="your_bucket_name"