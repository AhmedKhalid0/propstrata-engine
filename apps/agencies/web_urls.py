"""URL routes for Agency web views."""

from django.urls import path
from apps.agencies.web_views import agency_detail_view, agency_list_view

app_name = "agencies"

urlpatterns = [
    path("", agency_list_view, name="list"),
    path("<slug:slug>/", agency_detail_view, name="detail"),
]
