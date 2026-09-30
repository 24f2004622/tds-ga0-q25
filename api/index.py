from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import numpy as np
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok"}

@app.options("/api/latency")
async def options_handler():
    return Response(status_code=200)

# ✏️  PASTE YOUR OWN TELEMETRY JSON HERE (downloaded from exam portal)
TELEMETRY_DATA = json.loads("""
[
  {
    "region": "apac",
    "service": "support",
    "latency_ms": 219.12,
    "uptime_pct": 97.4,
    "timestamp": 20250301
  },
  {
    "region": "apac",
    "service": "checkout",
    "latency_ms": 105.64,
    "uptime_pct": 98.52,
    "timestamp": 20250302
  },
  {
    "region": "apac",
    "service": "catalog",
    "latency_ms": 139.35,
    "uptime_pct": 97.894,
    "timestamp": 20250303
  },
  {
    "region": "apac",
    "service": "recommendations",
    "latency_ms": 164.13,
    "uptime_pct": 99.009,
    "timestamp": 20250304
  },
  {
    "region": "apac",
    "service": "checkout",
    "latency_ms": 170.65,
    "uptime_pct": 97.362,
    "timestamp": 20250305
  },
  {
    "region": "apac",
    "service": "payments",
    "latency_ms": 122,
    "uptime_pct": 97.248,
    "timestamp": 20250306
  },
  {
    "region": "apac",
    "service": "analytics",
    "latency_ms": 208.75,
    "uptime_pct": 98.161,
    "timestamp": 20250307
  },
  {
    "region": "apac",
    "service": "checkout",
    "latency_ms": 183.82,
    "uptime_pct": 98.641,
    "timestamp": 20250308
  },
  {
    "region": "apac",
    "service": "payments",
    "latency_ms": 208.12,
    "uptime_pct": 98.87,
    "timestamp": 20250309
  },
  {
    "region": "apac",
    "service": "analytics",
    "latency_ms": 118.13,
    "uptime_pct": 98.728,
    "timestamp": 20250310
  },
  {
    "region": "apac",
    "service": "support",
    "latency_ms": 160.19,
    "uptime_pct": 99.382,
    "timestamp": 20250311
  },
  {
    "region": "apac",
    "service": "recommendations",
    "latency_ms": 219.92,
    "uptime_pct": 98.891,
    "timestamp": 20250312
  },
  {
    "region": "emea",
    "service": "checkout",
    "latency_ms": 127.76,
    "uptime_pct": 97.442,
    "timestamp": 20250301
  },
  {
    "region": "emea",
    "service": "checkout",
    "latency_ms": 203.13,
    "uptime_pct": 98.437,
    "timestamp": 20250302
  },
  {
    "region": "emea",
    "service": "checkout",
    "latency_ms": 187.17,
    "uptime_pct": 99.442,
    "timestamp": 20250303
  },
  {
    "region": "emea",
    "service": "payments",
    "latency_ms": 193.35,
    "uptime_pct": 97.328,
    "timestamp": 20250304
  },
  {
    "region": "emea",
    "service": "analytics",
    "latency_ms": 215.06,
    "uptime_pct": 99.477,
    "timestamp": 20250305
  },
  {
    "region": "emea",
    "service": "support",
    "latency_ms": 126.73,
    "uptime_pct": 97.536,
    "timestamp": 20250306
  },
  {
    "region": "emea",
    "service": "support",
    "latency_ms": 184.18,
    "uptime_pct": 97.454,
    "timestamp": 20250307
  },
  {
    "region": "emea",
    "service": "analytics",
    "latency_ms": 175.56,
    "uptime_pct": 98.861,
    "timestamp": 20250308
  },
  {
    "region": "emea",
    "service": "support",
    "latency_ms": 108.79,
    "uptime_pct": 99.131,
    "timestamp": 20250309
  },
  {
    "region": "emea",
    "service": "catalog",
    "latency_ms": 156.23,
    "uptime_pct": 98.328,
    "timestamp": 20250310
  },
  {
    "region": "emea",
    "service": "support",
    "latency_ms": 155.1,
    "uptime_pct": 99.023,
    "timestamp": 20250311
  },
  {
    "region": "emea",
    "service": "catalog",
    "latency_ms": 213.11,
    "uptime_pct": 97.594,
    "timestamp": 20250312
  },
  {
    "region": "amer",
    "service": "checkout",
    "latency_ms": 205.95,
    "uptime_pct": 97.325,
    "timestamp": 20250301
  },
  {
    "region": "amer",
    "service": "checkout",
    "latency_ms": 125.9,
    "uptime_pct": 98.147,
    "timestamp": 20250302
  },
  {
    "region": "amer",
    "service": "payments",
    "latency_ms": 180.6,
    "uptime_pct": 97.199,
    "timestamp": 20250303
  },
  {
    "region": "amer",
    "service": "analytics",
    "latency_ms": 109.22,
    "uptime_pct": 98.125,
    "timestamp": 20250304
  },
  {
    "region": "amer",
    "service": "catalog",
    "latency_ms": 181.9,
    "uptime_pct": 97.903,
    "timestamp": 20250305
  },
  {
    "region": "amer",
    "service": "analytics",
    "latency_ms": 197.94,
    "uptime_pct": 99.17,
    "timestamp": 20250306
  },
  {
    "region": "amer",
    "service": "catalog",
    "latency_ms": 198.78,
    "uptime_pct": 97.756,
    "timestamp": 20250307
  },
  {
    "region": "amer",
    "service": "checkout",
    "latency_ms": 220.3,
    "uptime_pct": 98.801,
    "timestamp": 20250308
  },
  {
    "region": "amer",
    "service": "checkout",
    "latency_ms": 192.9,
    "uptime_pct": 98.486,
    "timestamp": 20250309
  },
  {
    "region": "amer",
    "service": "analytics",
    "latency_ms": 190.91,
    "uptime_pct": 97.749,
    "timestamp": 20250310
  },
  {
    "region": "amer",
    "service": "analytics",
    "latency_ms": 176.06,
    "uptime_pct": 97.35,
    "timestamp": 20250311
  },
  {
    "region": "amer",
    "service": "support",
    "latency_ms": 170.07,
    "uptime_pct": 97.38,
    "timestamp": 20250312
  }
]
""")

@app.post("/api/latency")
async def latency_analytics(request: Request):
    body = await request.json()
    regions = body.get("regions", [])
    threshold_ms = body.get("threshold_ms", 180)

    results = []
    for region in regions:
        records   = [r for r in TELEMETRY_DATA if r["region"] == region]
        latencies = [r["latency_ms"] for r in records]
        uptimes   = [r["uptime_pct"]  for r in records]
        results.append({
            "region":      region,
            "avg_latency": round(float(np.mean(latencies)), 2),
            "p95_latency": round(float(np.percentile(latencies, 95)), 2),
            "avg_uptime":  round(float(np.mean(uptimes)), 3),
            "breaches":    int(sum(1 for l in latencies if l > threshold_ms))
        })

    return {"regions": results}