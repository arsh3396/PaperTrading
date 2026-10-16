"""
Root URL configuration (DC-09, CI internal endpoints).

Planned routes (not wired yet):
    GET/POST  /accounts/register/, /accounts/login/, /accounts/logout/
    GET       /                         -> portfolio dashboard
    GET       /market/search/           -> ticker lookup
    GET       /market/quote/<symbol>/   -> quote detail / order ticket
    POST      /trade/buy/, /trade/sell/ -> order execution
    GET       /history/                 -> transaction ledger
    POST      /api/explain/             -> AI term explanation
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("market/", include("market.urls")),
    path("trade/", include("trading.urls")),
    path("", include("portfolio.urls")),
    path("", include("ai_explainer.urls")),
    # GET /history/ will be added from trading.views when the ledger UI is implemented.
]
