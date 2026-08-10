import json
import boto3
from fastapi import FastAPI, HTTPException
import processing

s3 = boto3.client("s3")
bucket_name = "257288818923-engg-internship"
key = "sample_data.json"

response = s3.get_object(Bucket=bucket_name, Key=key)
data = json.load(response["Body"])

app = FastAPI()


@app.get("/events/count")
def events_count():
    return {"count": processing.count_events(data)}


@app.get("/publishers")
def publishers():
    return processing.unique_publishers(data)


@app.get("/country/{code}")
def country(code: str):
    count = processing.events_by_country(data, code)
    if count == 0:
        raise HTTPException(status_code=404, detail="Country not found")
    return {"country": code, "events": count}


@app.get("/campaigns/top")
def campaigns_top(n: int = 10):
    return processing.top_campaigns(data, n)


@app.get("/countries/top")
def countries_top(n: int = 10):
    return processing.top_countries(data, n)


@app.get("/cities/top")
def cities_top(n: int = 10):
    return processing.top_cities(data, n)


@app.get("/devices/unique")
def devices_unique():
    return {"unique_devices": processing.unique_devices(data)}


@app.get("/hourly")
def hourly():
    return processing.hourly_distribution(data)


@app.get("/os-split")
def os_split():
    return processing.os_split(data)


@app.get("/bid-price/average")
def bid_price_average():
    return {"average_bid_price": processing.average_bid_price(data)}


@app.get("/data-quality/missing")
def data_quality_missing():
    return processing.missing_values(data)


@app.get("/summary")
def summary():
    return processing.get_summary(data)