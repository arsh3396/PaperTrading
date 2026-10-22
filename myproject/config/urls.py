from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("market/", include("market.urls")),
    path("trade/", include("trading.urls")),
    path("", include("portfolio.urls")),
    path("", include("ai_explainer.urls")),
]
