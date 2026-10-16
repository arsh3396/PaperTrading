"""
Market data is not persisted as a domain entity.

Quotes are served from the Django cache (key `quote:{SYMBOL}`, TTL 60s — FR-MKT-09).
Optional sample/fallback mode is configuration (FR-MKT-08), not a table.
"""
