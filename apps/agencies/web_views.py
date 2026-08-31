"""Web views for Agency directory and profile pages."""

from django.shortcuts import get_object_or_404, render
from apps.agencies.models import Agency


def agency_list_view(request):
    """Renders directory of verified real estate agencies."""
    agencies = Agency.objects.filter(is_verified=True).prefetch_related("agents", "properties")
    return render(
        request,
        "agencies/list.html",
        {
            "agencies": agencies,
            "page_title": "Real Estate Agencies & Verified Brokers | PropStrata",
        },
    )


def agency_detail_view(request, slug):
    """Renders agency profile with assigned agent roster and active property listings."""
    agency = get_object_or_404(Agency.objects.prefetch_related("agents", "properties"), slug=slug)
    active_listings = agency.properties.filter(status="ACTIVE")[:12]
    return render(
        request,
        "agencies/detail.html",
        {
            "agency": agency,
            "properties": active_listings,
            "page_title": f"{agency.name_en} | Verified Broker Agency",
        },
    )
