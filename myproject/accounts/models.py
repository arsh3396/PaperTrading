from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Wallet(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wallet",
    )
    cash_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("100000.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Virtual USD available for purchases (FR-WAL-04).",
    )
    initial_capital = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("100000.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Configurable starting cash recorded for Total P&L (FR-WAL-02).",
    )
    realized_pnl = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Running realized P&L from sells (FR-SELL-06).",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(cash_balance__gte=Decimal("0.00")),
                name="wallet_cash_balance_gte_zero",
            ),
            models.CheckConstraint(
                condition=models.Q(initial_capital__gte=Decimal("0.00")),
                name="wallet_initial_capital_gte_zero",
            ),
        ]

    def __str__(self) -> str:
        return f"Wallet({self.user_id}, cash={self.cash_balance})"
