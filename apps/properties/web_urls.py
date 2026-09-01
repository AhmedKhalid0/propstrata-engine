"""URL routes for Web UI property pages."""

from django.urls import path
from apps.properties.web_views import (
    add_property_view,
    home_view,
    property_compare_view,
    property_detail_view,
    property_list_view,
)

app_name = "properties"

urlpatterns = [
    path("", home_view, name="home"),
    path("properties/", property_list_view, name="list"),
    path("compare/", property_compare_view, name="compare"),
    path("properties/<slug:slug>/", property_detail_view, name="detail"),
    path("list-property/", add_property_view, name="add"),
]
