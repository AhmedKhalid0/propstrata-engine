"""Unified REST API Router for Mobile Apps and Web Clients."""

from django.http import JsonResponse
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.agencies.views import AgencyViewSet, AgentViewSet
from apps.leads.views import FavoriteViewSet, LeadInquiryViewSet, SavedSearchViewSet
from apps.locations.views import (
    CityViewSet,
    CountryViewSet,
    DistrictViewSet,
    GovernorateViewSet,
)
from apps.properties.models import Property
from apps.properties.views import (
    AmenityViewSet,
    PropertyTypeViewSet,
    PropertyViewSet,
)
from propstrata_core import __version__

router = DefaultRouter()

# Properties & Taxonomy
router.register(r"properties", PropertyViewSet, basename="property")
router.register(r"property-types", PropertyTypeViewSet, basename="property-type")
router.register(r"amenities", AmenityViewSet, basename="amenity")

# Locations & Spatial
router.register(r"locations/countries", CountryViewSet, basename="country")
router.register(r"locations/governorates", GovernorateViewSet, basename="governorate")
router.register(r"locations/cities", CityViewSet, basename="city")
router.register(r"locations/districts", DistrictViewSet, basename="district")

# Agencies & Agents
router.register(r"agencies", AgencyViewSet, basename="agency")
router.register(r"agents", AgentViewSet, basename="agent")

# Leads & Interactivity
router.register(r"leads/inquiries", LeadInquiryViewSet, basename="lead-inquiry")
router.register(r"leads/favorites", FavoriteViewSet, basename="favorite")
router.register(r"leads/saved-searches", SavedSearchViewSet, basename="saved-search")


def api_health_check(request):
    """Returns engine health, database status, and total active listings."""
    total_active = Property.objects.filter(status="ACTIVE").count()
    return JsonResponse(
        {
            "status": "healthy",
            "service": "PropStrata-Engine REST API",
            "version": __version__,
            "database": "connected (SQLite/PostgreSQL)",
            "active_listings_count": total_active,
        }
    )


urlpatterns = [
    path("health/", api_health_check, name="api-health"),
    path("", include(router.urls)),
]
