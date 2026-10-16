"""
Market data service layer (DC-01, SI-01).

Intended responsibilities (not implemented yet):
    - MarketDataProvider abstraction (DC-04)
    - Symbol validation and normalization (FR-MKT-01, FR-MKT-02)
    - Quote retrieval, Daily Change %, 60s cache (FR-MKT-03, FR-MKT-04, FR-MKT-09)
    - Stale-cache fallback when the provider is down (FR-MKT-07)
    - Batch quote fetch for the dashboard (FR-PORT-08)

DC-01 names this file `market/services.py`. Views must call this module only.
"""
