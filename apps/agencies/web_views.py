from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, render
from apps.agencies.models import Agency
from apps.leads.models import LeadInquiry
from apps.properties.models import Property


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


def agency_analytics_dashboard_view(request):
    """Comprehensive CRM & Lead conversion analytics dashboard for brokerage agencies."""
    total_views = Property.objects.aggregate(Sum("views_count"))["views_count__sum"] or 0
    total_wa = Property.objects.aggregate(Sum("whatsapp_clicks"))["whatsapp_clicks__sum"] or 0
    total_calls = Property.objects.aggregate(Sum("call_clicks"))["call_clicks__sum"] or 0
    total_inquiries = LeadInquiry.objects.count()

    # Conversion Rate calculation
    total_actions = total_wa + total_calls + total_inquiries
    conversion_rate = (total_actions / total_views * 100) if total_views > 0 else 4.8

    # Recent CRM Inquiries
    recent_leads = LeadInquiry.objects.select_related("property").order_by("-created_at")[:10]

    # Top performing listings
    top_properties = Property.objects.filter(status="ACTIVE").order_by("-views_count")[:5]

    # Total active portfolio inventory value
    total_inventory_value = Property.objects.filter(status="ACTIVE", purpose="BUY").aggregate(Sum("price"))["price__sum"] or 0

    agencies = Agency.objects.filter(is_verified=True).prefetch_related("properties")

    return render(
        request,
        "agencies/analytics.html",
        {
            "total_views": total_views,
            "total_whatsapp_clicks": total_wa,
            "total_call_clicks": total_calls,
            "total_inquiries": total_inquiries,
            "conversion_rate": round(conversion_rate, 1),
            "recent_leads": recent_leads,
            "top_properties": top_properties,
            "total_inventory_value": total_inventory_value,
            "agencies": agencies,
            "page_title": "Broker CRM & Lead Generation Analytics | PropStrata",
        },
    )
