# US Manufacturing API

US manufacturing data including industrial production index, capacity utilization, factory orders, durable goods, PMI, manufacturing employment, and inventories. Powered by FRED.

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | API info and available endpoints |
| `GET /summary` | All manufacturing indicators snapshot |
| `GET /industrial-production` | Industrial Production Index (2017=100) |
| `GET /capacity-utilization` | Capacity utilization (%) |
| `GET /factory-orders` | New factory orders |
| `GET /durable-goods` | Durable goods orders |
| `GET /nondurable-goods` | Nondurable goods orders |
| `GET /employment` | Manufacturing employment |
| `GET /pmi` | ISM Manufacturing PMI |
| `GET /inventories` | Manufacturing & trade inventories |
| `GET /unfilled-orders` | Unfilled manufacturing orders |

## Data Source

FRED — Federal Reserve Bank of St. Louis
https://fred.stlouisfed.org

## Authentication

Requires `X-RapidAPI-Key` header via RapidAPI.
