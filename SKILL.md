---
name: groundtruth-oracle
description: "GroundTruth Autonomous Oracle — query physical-world real estate due diligence, NC road abandonment risk, FEMA flood zones, and live municipal building permits, settled via x402 on Base Mainnet."
homepage: https://unlisted-cabbage-swaddling.ngrok-free.dev
---

# 🌍 GroundTruth Autonomous Cadastral & Municipal Oracle

An open-source Action Provider and client SDK for querying real-world property risk and municipal permits, gated by automated Base USDC x402 micro-settlements.

## Endpoints
* **Tax Auction Triage ($0.50):** `/v1/sniper/triage`
* **FEMA Flood Clearance ($1.50):** `/v1/environmental/flood-zone`
* **CMA Valuation Comps ($2.00):** `/v1/valuation/cma`
* **NC Rural Legal Risk ($5.00):** `/api/v1/rural-risk`
* **Municipal Permits (Free):** `/v1/civic/permits/{city}/{query}`

## Quickstart
```python
from groundtruth_agentkit import GroundTruthActionProvider

oracle = GroundTruthActionProvider()
permits = oracle.get_municipal_permits("chicago", query="commercial", limit=1)
print(permits)
```
