"""
Trading / ledger models (Appendix A: POSITION, TRANSACTION).

Intended models (not implemented yet):
    Position — user, symbol, quantity, avg_price; UNIQUE(user, symbol) (DC-03).
    Transaction — append-only ledger (FR-LED-01..08): ticker, type BUY/SELL,
        shares, exec_price, total_value, executed_at, idempotency_key,
        cash_balance_after, avg_price_after, realized_pnl.
"""
