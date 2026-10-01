from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
from typing import List
import json

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = Path(__file__).parent / "q-vercel-latency.json"

with open(DATA_FILE, encoding="utf-8") as f:
    telemetry_data = json.load(f)


class AnalyticsRequest(BaseModel):
    regions: List[str]
    threshold_ms: int


@app.get("/")
def read_root():
    return {"status": "ok"}


@app.post("/api/latency")
def analyze_latency(request: AnalyticsRequest):
    results = {}

    for region in request.regions:
        rows = [
            r for r in telemetry_data
            if r.get("region") == region
        ]

        if not rows:
            results[region] = {
                "avg_latency": 0,
                "p95_latency": 0,
                "avg_uptime": 0,
                "breaches": 0
            }
            continue

        latencies = sorted(
            [r["latency_ms"] for r in rows]
        )

        uptimes = [
            r["uptime_pct"] for r in rows
        ]

        n = len(latencies)

        idx = (n - 1) * 0.95
        lo = int(idx)

        p95 = (
            latencies[lo]
            + (idx - lo) * (latencies[lo + 1] - latencies[lo])
            if lo + 1 < n
            else latencies[lo]
        )

        results[region] = {
            "avg_latency": round(sum(latencies) / n, 2),
            "p95_latency": round(p95, 2),
            "avg_uptime": round(
                sum(uptimes) / len(uptimes), 3
            ),
            "breaches": sum(
                1
                for lat in latencies
                if lat > request.threshold_ms
            ),
        }

    return {"regions": results}