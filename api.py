import json
import logging

logging.basicConfig(level=logging.INFO)  #Used for logging
logger = logging.getLogger(__name__)

import aws
from fastapi import FastAPI, HTTPException
import data_processing

data = json.loads(aws.file_content)
app = FastAPI()

@app.get("/v1/events/count")
def events_count():
    return {"count": data_processing.count_events(data)}


@app.get("/v1/publishers")
def publishers():
    return data_processing.unique_publishers(data)


@app.get("/v1/country/{code}")
def country(code: str):
    count = data_processing.events_by_country(data, code)
    if count == 0:
        logger.warning(f"Country not found: {code}")
        raise HTTPException(status_code=404, detail="Country not found")
    return {"country": code, "events": count}


@app.get("/v1/campaigns/top/{n}")
def campaigns_top(n: int):
    if n <= 0:
        raise HTTPException(
            status_code=400, detail="Number must be greater than 0"
        )
    return data_processing.top_campaigns(data, n)


@app.get("/v1/countries/top/{n}")
def countries_top(n: int):
    if n <= 0:
        logger.warning(f"Invalid n: {n}")
        raise HTTPException(
            status_code=400, detail="Number must be greater than 0"
        )
    return data_processing.top_countries(data, n)

@app.get("/v1/devices/unique")
def devices_unique():
    return {"unique_devices": data_processing.unique_devices(data)}


@app.get("/v1/hourly")
def hourly():
    return data_processing.hourly_distribution(data)

@app.get("/v1/summary")
def summary():
    return data_processing.get_summary(data)

@app.get("/v1/cities/top/{n}")
def cities_top(n: int):
    if n <= 0:
        logger.warning(f"Invalid n: {n}")
        raise HTTPException(
            status_code=400, detail="Number must be greater than 0"
        )
    return data_processing.top_cities(data, n)

@app.get("/v1/publishers/top/{n}")
def top_publishers(n:int):
    if n < 1:
        logger.warning(f"Invalid n: {n}")
        raise HTTPException(
            status_code=400, detail="The number must be greater than 0"       
        )
    return data_processing.top_publishers(data,n)

@app.get("/v1/daily")
def daily():
    return data_processing.daily_distribution(data)


@app.get("/v1/os-split")
def os_split():
    return data_processing.os_split(data)


@app.get("/v1/bid-price/average")
def bid_price_average():
    return {"average_bid_price": data_processing.average_bid_price(data)}


@app.get("/v1/data-quality/missing")
def data_quality_missing():
    return data_processing.missing_values(data)


@app.get("/v1/peak/hour")
def peakhour():
    return data_processing.peak_hour(data)

@app.get("/v1/events/device")
def events_per_device():
    return data_processing.events_by_device(data)

@app.get("/v1/anomalies/{threshold}")
def anomalies(threshold : int):
    return data_processing.anomalies(data,threshold)