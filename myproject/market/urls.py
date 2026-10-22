from django.urls import path

app_name = "market"

urlpatterns = [
    path("search/", views.search, name="search"),
    path("quote/<str:symbol>/", views.quote_detail, name="quote"),
]
