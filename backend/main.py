from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / ".env", encoding="utf-8-sig")

from fastapi import FastAPI
from src.trend_fetcher import fetch_trending, fetch_rising

app = FastAPI(title="FAiN API")


@app.get("/trends/trending")
def get_trending(region_code: str = "US", max_results: int = 50):
    return fetch_trending(region_code=region_code, max_results=max_results)


@app.get("/trends/rising")
def get_rising(topic: str, region_code: str = "US", max_results: int = 50):
    return fetch_rising(topic=topic, region_code=region_code, max_results=max_results)
