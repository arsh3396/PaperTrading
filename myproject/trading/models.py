"""
Trading and ledger models (Appendix A: POSITION, TRANSACTION).

Quantities and money use DecimalField (DC-02, FR-WAL-06). Database CHECKs and
uniqueness match DC-03. Transaction rows are append-only (FR-LED-03).
"""

from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

SYMBOL_VALIDATOR = RegexValidator(
    regex=r"^[A-Z]{1,5}([.-][A-Z])?$",
    message="Symbol must match FR-MKT-02 (e.g. AAPL, BRK.B).",
)


class AppendOnlyQuerySet(models.QuerySet):
    def delete(self):
        raise ValidationError("Ledger entries cannot be deleted (FR-LED-03).")

    def update(self, **kwargs):
        raise ValidationError("Ledger entries are append-only (FR-LED-03).")


class Position(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="positions",
    )
    symbol = models.CharField(max_length=8, validators=[SYMBOL_VALIDATOR])
    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        validators=[MinValueValidator(Decimal("0"))],
        help_text="Whole shares currently held (A-1, DC-02).",
    )
    avg_price = models.DecimalField(
        max_digits=14,
        decimal_places=4,
        validators=[MinValueValidator(Decimal("0.0000"))],
        help_text="Weighted average purchase price (FR-BUY-05).",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "symbol"],
                name="position_unique_user_symbol",
            ),
            models.CheckConstraint(
                condition=models.Q(quantity__gte=Decimal("0")),
                name="position_quantity_gte_zero",
            ),
            models.CheckConstraint(
                condition=models.Q(avg_price__gte=Decimal("0.0000")),
                name="position_avg_price_gte_zero",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.symbol} x {self.quantity} @{self.avg_price}"


class Transaction(models.Model):
    """Append-only executed-order ledger (FR-LED-01, FR-LED-03)."""

    class Side(models.TextChoices):
        BUY = "BUY", "Buy"
        SELL = "SELL", "Sell"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transactions",
    )
    symbol = models.CharField(max_length=8, validators=[SYMBOL_VALIDATOR])
    type = models.CharField(max_length=4, choices=Side.choices)
    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        validators=[MinValueValidator(Decimal("1"))],
        help_text="Whole shares executed; must be > 0 (DC-03, FR-ORD-07).",
    )
    exec_price = models.DecimalField(
        max_digits=14,
        decimal_places=4,
        validators=[MinValueValidator(Decimal("0.0000"))],
    )
    total_value = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Quantity x exec_price, rounded half-up to 2 dp (FR-ORD-08).",
    )
    cash_balance_after = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    avg_price_after = models.DecimalField(
        max_digits=14,
        decimal_places=4,
        null=True,
        blank=True,
        help_text="Position average after a buy (FR-BUY-06); null on sells.",
    )
    realized_pnl = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realized P&L for a sell (FR-SELL-06); null on buys.",
    )
    idempotency_key = models.UUIDField()
    executed_at = models.DateTimeField(auto_now_add=True)

    objects = AppendOnlyQuerySet.as_manager()

    class Meta:
        ordering = ["-executed_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "idempotency_key"],
                name="txn_unique_user_idempotency_key",
            ),
            models.CheckConstraint(
                condition=models.Q(type__in=["BUY", "SELL"]),
                name="txn_type_buy_or_sell",
            ),
            models.CheckConstraint(
                condition=models.Q(quantity__gt=Decimal("0")),
                name="txn_quantity_gt_zero",
            ),
            models.CheckConstraint(
                condition=models.Q(exec_price__gte=Decimal("0.0000")),
                name="txn_exec_price_gte_zero",
            ),
            models.CheckConstraint(
                condition=models.Q(total_value__gte=Decimal("0.00")),
                name="txn_total_value_gte_zero",
            ),
            models.CheckConstraint(
                condition=models.Q(cash_balance_after__gte=Decimal("0.00")),
                name="txn_cash_after_gte_zero",
            ),
        ]
        indexes = [
            models.Index(
                fields=["user", "-executed_at"],
                name="txn_user_executed_idx",
            ),
            models.Index(fields=["user", "symbol"], name="txn_user_symbol_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.type} {self.quantity} {self.symbol} @ {self.exec_price}"

    def save(self, *args, **kwargs):
        if self.pk is not None:
            raise ValidationError("Ledger entries are append-only (FR-LED-03).")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Ledger entries cannot be deleted (FR-LED-03).")
