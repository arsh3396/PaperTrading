"""
Trading engine service layer (DC-01).

Intended responsibilities (not implemented yet):
    - Market buy/sell inside transaction.atomic() (FR-ORD-04, C-7, REL-01)
    - select_for_update on wallet and position (FR-ORD-05)
    - Idempotency keys (FR-ORD-06)
    - Weighted average cost (FR-BUY-04..06, BR-1)
    - Holdings checks and short-sale rejection (FR-SELL-*)
    - Ledger writes (FR-LED-01)

DC-01 names this file `trading/services.py`. Views must call this module only.
"""
