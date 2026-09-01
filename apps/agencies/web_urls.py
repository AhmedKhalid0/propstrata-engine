"""URL routes for Agency web views."""

from django.urls import path
from apps.agencies.web_views import (
    agency_analytics_dashboard_view,
    agency_detail_view,
    agency_list_view,
)

app_name = "agencies"

urlpatterns = [
    path("", agency_list_view, name="list"),
    path("analytics/", agency_analytics_dashboard_view, name="analytics"),
    path("<slug:slug>/", agency_detail_view, name="detail"),
]
