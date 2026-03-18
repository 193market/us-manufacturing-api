from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
from datetime import datetime

app = FastAPI(
    title="US Manufacturing API",
    description="US manufacturing data including industrial production, capacity utilization, factory orders, durable goods, and manufacturing employment. Powered by FRED.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FRED_BASE = "https://api.stlouisfed.org/fred/series/observations"
FRED_API_KEY = os.environ.get("FRED_API_KEY", "")

SERIES = {
    "industrial_prod":   {"id": "INDPRO",    "name": "Industrial Production Index",             "unit": "Index 2017=100",  "frequency": "Monthly"},
    "capacity_util":     {"id": "TCU",       "name": "Capacity Utilization: Total Industry",    "unit": "%",               "frequency": "Monthly"},
    "factory_orders":    {"id": "AMTMNO",    "name": "Manufacturers: New Orders, All Industries","unit": "Millions of USD", "frequency": "Monthly"},
    "durable_goods":     {"id": "DGORDER",   "name": "Durable Goods Orders",                    "unit": "Millions of USD", "frequency": "Monthly"},
    "nondurable_goods":  {"id": "ANDENO",    "name": "Nonfarm Business: Nondurable Goods",      "unit": "Millions of USD", "frequency": "Monthly"},
    "mfg_employment":    {"id": "MANEMP",    "name": "Manufacturing Employment",                "unit": "Thousands",       "frequency": "Monthly"},
    "mfg_payroll":       {"id": "CES3000000008","name":"Manufacturing Avg Hourly Earnings",      "unit": "USD per Hour",    "frequency": "Monthly"},
    "pmi_ism":           {"id": "NAPM",      "name": "ISM Manufacturing PMI",                   "unit": "Index",           "frequency": "Monthly"},
    "unfilled_orders":   {"id": "AMDMUONS",  "name": "Unfilled Orders: Manufacturing",          "unit": "Millions of USD", "frequency": "Monthly"},
    "inventories":       {"id": "AMTMTI",    "name": "Manufacturing & Trade Inventories",       "unit": "Millions of USD", "frequency": "Monthly"},
}


async def fetch_fred(series_id: str, limit: int = 24):
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "sort_order": "desc",
        "limit": limit,
    }
    async with httpx.AsyncClient(timeout=15) as client:
        res = await client.get(FRED_BASE, params=params)
        data = res.json()
    obs = data.get("observations", [])
    return [
        {"date": o["date"], "value": float(o["value"]) if o["value"] != "." else None}
        for o in obs
        if o.get("value") != "."
    ]


@app.get("/")
def root():
    return {
        "api": "US Manufacturing API",
        "version": "1.0.0",
        "provider": "GlobalData Store",
        "source": "FRED - Federal Reserve Bank of St. Louis",
        "endpoints": ["/summary", "/industrial-production", "/capacity-utilization", "/factory-orders", "/durable-goods", "/nondurable-goods", "/employment", "/pmi", "/inventories", "/unfilled-orders"],
        "updated_at": datetime.utcnow().isoformat() + "Z",
    }


@app.get("/summary")
async def summary(limit: int = Query(default=12, ge=1, le=60)):
    """All manufacturing indicators snapshot"""
    results = {}
    for key, meta in SERIES.items():
        results[key] = await fetch_fred(meta["id"], limit)
    formatted = {
        key: {
            "name": SERIES[key]["name"],
            "unit": SERIES[key]["unit"],
            "frequency": SERIES[key]["frequency"],
            "data": results[key],
        }
        for key in SERIES
    }
    return {
        "country": "United States",
        "source": "FRED - Federal Reserve Bank of St. Louis",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "indicators": formatted,
    }


@app.get("/industrial-production")
async def industrial_production(limit: int = Query(default=24, ge=1, le=120)):
    """Industrial Production Index (2017=100)"""
    data = await fetch_fred("INDPRO", limit)
    return {"indicator": "Industrial Production Index", "series_id": "INDPRO", "unit": "Index 2017=100", "frequency": "Monthly", "source": "FRED", "updated_at": datetime.utcnow().isoformat() + "Z", "data": data}


@app.get("/capacity-utilization")
async def capacity_utilization(limit: int = Query(default=24, ge=1, le=120)):
    """Capacity utilization: total industry (%)"""
    data = await fetch_fred("TCU", limit)
    return {"indicator": "Capacity Utilization: Total Industry", "series_id": "TCU", "unit": "%", "frequency": "Monthly", "source": "FRED", "updated_at": datetime.utcnow().isoformat() + "Z", "data": data}


@app.get("/factory-orders")
async def factory_orders(limit: int = Query(default=24, ge=1, le=120)):
    """Manufacturers new orders: all manufacturing industries"""
    data = await fetch_fred("AMTMNO", limit)
    return {"indicator": "Manufacturers: New Orders, All Industries", "series_id": "AMTMNO", "unit": "Millions of USD", "frequency": "Monthly", "source": "FRED", "updated_at": datetime.utcnow().isoformat() + "Z", "data": data}


@app.get("/durable-goods")
async def durable_goods(limit: int = Query(default=24, ge=1, le=120)):
    """Durable goods orders (millions USD)"""
    data = await fetch_fred("DGORDER", limit)
    return {"indicator": "Durable Goods Orders", "series_id": "DGORDER", "unit": "Millions of USD", "frequency": "Monthly", "source": "FRED", "updated_at": datetime.utcnow().isoformat() + "Z", "data": data}


@app.get("/nondurable-goods")
async def nondurable_goods(limit: int = Query(default=24, ge=1, le=120)):
    """Nondurable goods orders"""
    data = await fetch_fred("ANDENO", limit)
    return {"indicator": "Nondurable Goods Orders", "series_id": "ANDENO", "unit": "Millions of USD", "frequency": "Monthly", "source": "FRED", "updated_at": datetime.utcnow().isoformat() + "Z", "data": data}


@app.get("/employment")
async def employment(limit: int = Query(default=24, ge=1, le=120)):
    """Manufacturing employment (thousands of persons)"""
    data = await fetch_fred("MANEMP", limit)
    return {"indicator": "Manufacturing Employment", "series_id": "MANEMP", "unit": "Thousands", "frequency": "Monthly", "source": "FRED", "updated_at": datetime.utcnow().isoformat() + "Z", "data": data}


@app.get("/pmi")
async def pmi(limit: int = Query(default=24, ge=1, le=120)):
    """ISM Manufacturing Purchasing Managers Index"""
    data = await fetch_fred("NAPM", limit)
    return {"indicator": "ISM Manufacturing PMI", "series_id": "NAPM", "unit": "Index (>50=expansion)", "frequency": "Monthly", "source": "FRED", "updated_at": datetime.utcnow().isoformat() + "Z", "data": data}


@app.get("/inventories")
async def inventories(limit: int = Query(default=24, ge=1, le=120)):
    """Manufacturing and trade inventories"""
    data = await fetch_fred("AMTMTI", limit)
    return {"indicator": "Manufacturing & Trade Inventories", "series_id": "AMTMTI", "unit": "Millions of USD", "frequency": "Monthly", "source": "FRED", "updated_at": datetime.utcnow().isoformat() + "Z", "data": data}


@app.get("/unfilled-orders")
async def unfilled_orders(limit: int = Query(default=24, ge=1, le=120)):
    """Unfilled orders for manufacturing industries"""
    data = await fetch_fred("AMDMUONS", limit)
    return {"indicator": "Unfilled Orders: Manufacturing", "series_id": "AMDMUONS", "unit": "Millions of USD", "frequency": "Monthly", "source": "FRED", "updated_at": datetime.utcnow().isoformat() + "Z", "data": data}
