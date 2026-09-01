"""Web UI views for browsing properties, interactive map search, and property details."""

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from apps.agencies.models import Agency
from apps.locations.models import Country, District
from apps.properties.models import Amenity, Property, PropertyType


def home_view(request):
    """Homepage with Hero search, purpose switch, featured listings, and category showcase."""
    featured_properties = (
        Property.objects.filter(status="ACTIVE", tier__in=["FEATURED", "PREMIUM"])
        .select_related("property_type", "district", "agency")
        .prefetch_related("images")[:6]
    )
    recent_properties = (
        Property.objects.filter(status="ACTIVE")
        .select_related("property_type", "district", "agency")
        .prefetch_related("images")[:8]
    )

    property_types = PropertyType.objects.annotate(active_count=Count("properties")).filter(active_count__gt=0)
    countries = Country.objects.filter(is_active=True).prefetch_related("governorates__cities__districts")
    districts = District.objects.all()[:20]

    total_listings = Property.objects.filter(status="ACTIVE").count()
    total_agencies = Agency.objects.filter(is_verified=True).count()

    return render(
        request,
        "index.html",
        {
            "featured_properties": featured_properties,
            "recent_properties": recent_properties,
            "property_types": property_types,
            "countries": countries,
            "districts": districts,
            "total_listings": total_listings,
            "total_agencies": total_agencies,
            "page_title": "PropStrata | Enterprise Open-Source PropTech & Real Estate Marketplace",
        },
    )


def property_list_view(request):
    """Split-Screen Search: Filters on left, Property cards in center, Interactive Leaflet Map on right."""
    qs = (
        Property.objects.filter(status="ACTIVE")
        .select_related("property_type", "district__city__governorate__country", "agency", "agent")
        .prefetch_related("images")
    )

    # Extract Filters from GET parameters
    purpose = request.GET.get("purpose", "")
    prop_type = request.GET.get("type", "")
    district_id = request.GET.get("district", "")
    min_price = request.GET.get("min_price", "")
    max_price = request.GET.get("max_price", "")
    bedrooms = request.GET.get("bedrooms", "")
    furnishing = request.GET.get("furnishing", "")
    query = request.GET.get("q", "")
    sort = request.GET.get("sort", "featured")

    if purpose:
        qs = qs.filter(purpose__iexact=purpose)
    if prop_type:
        qs = qs.filter(property_type__slug=prop_type)
    if district_id:
        qs = qs.filter(district_id=district_id)
    if min_price:
        try:
            qs = qs.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            qs = qs.filter(price__lte=float(max_price))
        except ValueError:
            pass
    if bedrooms:
        if bedrooms == "5+":
            qs = qs.filter(bedrooms__gte=5)
        else:
            try:
                qs = qs.filter(bedrooms=int(bedrooms))
            except ValueError:
                pass
    if furnishing:
        qs = qs.filter(furnishing=furnishing)
    if query:
        qs = qs.filter(
            Q(title_en__icontains=query)
            | Q(title_ar__icontains=query)
            | Q(description_en__icontains=query)
            | Q(reference_id__icontains=query)
        )

    # Sorting
    if sort == "price_asc":
        qs = qs.order_by("price")
    elif sort == "price_desc":
        qs = qs.order_by("-price")
    elif sort == "area_desc":
        qs = qs.order_by("-area_sqm")
    else:
        qs = qs.order_by("-tier", "-created_at")

    paginator = Paginator(qs, 12)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    property_types = PropertyType.objects.all()
    districts = District.objects.all().select_related("city")

    return render(
        request,
        "properties/list.html",
        {
            "page_obj": page_obj,
            "total_count": qs.count(),
            "property_types": property_types,
            "districts": districts,
            "selected_purpose": purpose,
            "selected_type": prop_type,
            "selected_district": district_id,
            "selected_min_price": min_price,
            "selected_max_price": max_price,
            "selected_bedrooms": bedrooms,
            "selected_sort": sort,
            "query": query,
            "page_title": "Search Real Estate Properties & Interactive Map | PropStrata",
        },
    )


def property_detail_view(request, slug):
    """Property detail page with photo gallery, specs, amenities, agent card, and WhatsApp deep link."""
    property_obj = get_object_or_404(
        Property.objects.select_related("property_type", "district__city__governorate__country", "agency", "agent").prefetch_related(
            "images", "amenities", "floor_plans"
        ),
        slug=slug,
    )

    # Similar properties in the same district
    similar_properties = (
        Property.objects.filter(status="ACTIVE", district=property_obj.district)
        .exclude(pk=property_obj.pk)
        .select_related("property_type", "district")
        .prefetch_related("images")[:4]
    )

    # Prepare prefilled WhatsApp message
    clean_whatsapp = ""
    if property_obj.agent and property_obj.agent.whatsapp:
        clean_whatsapp = property_obj.agent.whatsapp.replace("+", "").replace(" ", "").replace("-", "")
    elif property_obj.agency and property_obj.agency.whatsapp:
        clean_whatsapp = property_obj.agency.whatsapp.replace("+", "").replace(" ", "").replace("-", "")
    else:
        clean_whatsapp = "96590000000"

    wa_text = f"Hello, I am inquiring about property [{property_obj.reference_id}] {property_obj.title_en} priced at {property_obj.price_formatted}: {request.build_absolute_uri()}"
    wa_url = f"https://wa.me/{clean_whatsapp}?text={wa_text.replace(' ', '%20')}"

    return render(
        request,
        "properties/detail.html",
        {
            "property": property_obj,
            "similar_properties": similar_properties,
            "whatsapp_url": wa_url,
            "page_title": f"{property_obj.title_en} | {property_obj.district.name_en} | PropStrata",
        },
    )


def add_property_view(request):
    """Multi-step listing creation wizard with map pin placement."""
    if request.method == "POST":
        title_en = request.POST.get("title_en", "Spacious Modern Apartment")
        title_ar = request.POST.get("title_ar", "شقة عصرية واسعة")
        purpose = request.POST.get("purpose", "RENT")
        type_id = request.POST.get("property_type")
        price = request.POST.get("price", 500)
        currency = request.POST.get("currency", "KWD")
        area_sqm = request.POST.get("area_sqm", 120)
        bedrooms = request.POST.get("bedrooms", 2)
        bathrooms = request.POST.get("bathrooms", 2)
        district_id = request.POST.get("district")
        latitude = request.POST.get("latitude", 29.3759)
        longitude = request.POST.get("longitude", 47.9774)
        description_en = request.POST.get("description_en", "")

        prop = Property.objects.create(
            title_en=title_en,
            title_ar=title_ar,
            purpose=purpose,
            property_type_id=type_id,
            price=price,
            currency=currency,
            area_sqm=area_sqm,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            district_id=district_id,
            latitude=latitude,
            longitude=longitude,
            description_en=description_en,
            status="ACTIVE",
        )
        return redirect("properties:detail", slug=prop.slug)

    property_types = PropertyType.objects.all()
    districts = District.objects.all().select_related("city")
    amenities = Amenity.objects.all()

    return render(
        request,
        "dashboard/add_property.html",
        {
            "property_types": property_types,
            "districts": districts,
            "amenities": amenities,
            "page_title": "List Your Property | PropStrata Listing Wizard",
        },
    )


def property_compare_view(request):
    """Interactive Property Comparison Studio comparing up to 4 listings side-by-side."""
    raw_ids = request.GET.get("ids", "")
    all_properties = Property.objects.filter(status="ACTIVE").select_related("property_type", "district")

    if raw_ids:
        try:
            ids = [int(i.strip()) for i in raw_ids.split(",") if i.strip().isdigit()][:4]
            selected_properties = list(
                Property.objects.filter(id__in=ids)
                .select_related("property_type", "district__city__governorate__country", "agency", "agent")
                .prefetch_related("images", "amenities")
            )
        except ValueError:
            selected_properties = list(all_properties[:3])
    else:
        # Default showcase of 3 properties
        selected_properties = list(
            Property.objects.filter(status="ACTIVE")
            .select_related("property_type", "district__city__governorate__country", "agency", "agent")
            .prefetch_related("images", "amenities")[:3]
        )

    # Compute comparative attributes
    for p in selected_properties:
        p.price_per_sqm = (float(p.price) / float(p.area_sqm)) if p.area_sqm > 0 else 0
        p.amenity_ids = set(p.amenities.values_list("id", flat=True))

    all_amenities = Amenity.objects.all()

    return render(
        request,
        "properties/compare.html",
        {
            "selected_properties": selected_properties,
            "all_properties": all_properties,
            "all_amenities": all_amenities,
            "page_title": "Property Comparison Studio | PropStrata",
        },
    )
