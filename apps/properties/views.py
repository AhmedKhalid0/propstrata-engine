"""DRF ViewSets and endpoints for Properties, Categories, and Map Search."""

from django.db.models import F, Q
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.properties.models import Amenity, Property, PropertyType
from apps.properties.serializers import (
    AmenitySerializer,
    PropertyCreateSerializer,
    PropertyDetailSerializer,
    PropertyListSerializer,
    PropertyTypeSerializer,
)


class PropertyViewSet(viewsets.ModelViewSet):
    """Primary Property listing API supporting faceted filtering, full-text search, and GeoJSON map pins."""

    queryset = (
        Property.objects.filter(status="ACTIVE")
        .select_related("property_type", "district__city__governorate__country", "agency", "agent")
        .prefetch_related("images", "amenities")
    )
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PropertyDetailSerializer
        elif self.action in ["create", "update", "partial_update"]:
            return PropertyCreateSerializer
        return PropertyListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params

        # 1. Purpose Filter (RENT / BUY / COMMERCIAL)
        purpose = params.get("purpose")
        if purpose:
            qs = qs.filter(purpose__iexact=purpose)

        # 2. Property Type Slug
        type_slug = params.get("type")
        if type_slug:
            qs = qs.filter(property_type__slug=type_slug)

        # 3. Country & City & District
        country = params.get("country")
        if country:
            qs = qs.filter(district__city__governorate__country__code__iexact=country)

        city = params.get("city")
        if city:
            qs = qs.filter(district__city__slug=city)

        district = params.get("district")
        if district:
            qs = qs.filter(district__slug=district)

        # 4. Price Bounds
        min_price = params.get("min_price")
        if min_price:
            try:
                qs = qs.filter(price__gte=float(min_price))
            except ValueError:
                pass

        max_price = params.get("max_price")
        if max_price:
            try:
                qs = qs.filter(price__lte=float(max_price))
            except ValueError:
                pass

        # 5. Bedrooms & Bathrooms
        bedrooms = params.get("bedrooms")
        if bedrooms:
            try:
                if bedrooms == "5+":
                    qs = qs.filter(bedrooms__gte=5)
                else:
                    qs = qs.filter(bedrooms=int(bedrooms))
            except ValueError:
                pass

        # 6. Keywords Search
        q = params.get("q")
        if q:
            qs = qs.filter(
                Q(title_en__icontains=q)
                | Q(title_ar__icontains=q)
                | Q(description_en__icontains=q)
                | Q(description_ar__icontains=q)
                | Q(reference_id__icontains=q)
            )

        # 7. Sorting
        sort = params.get("sort")
        if sort == "price_asc":
            qs = qs.order_by("price")
        elif sort == "price_desc":
            qs = qs.order_by("-price")
        elif sort == "area_desc":
            qs = qs.order_by("-area_sqm")
        elif sort == "featured":
            qs = qs.order_by("-tier", "-created_at")

        return qs

    def retrieve(self, request, *args, **kwargs):
        """Retrieves property detail and atomically increments views counter."""
        instance = self.get_object()
        Property.objects.filter(pk=instance.pk).update(views_count=F("views_count") + 1)
        instance.refresh_from_db(fields=["views_count"])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def map(self, request):
        """Returns lightweight GeoJSON FeatureCollection tailored for Leaflet / Mapbox price pin rendering."""
        properties = self.get_queryset()[:200]
        features = []
        for p in properties:
            features.append(
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [float(p.longitude), float(p.latitude)],
                    },
                    "properties": {
                        "id": p.id,
                        "reference_id": p.reference_id,
                        "title": p.title_en,
                        "title_ar": p.title_ar,
                        "price": float(p.price),
                        "price_display": p.price_formatted,
                        "currency": p.currency,
                        "purpose": p.purpose,
                        "bedrooms": p.bedrooms,
                        "bathrooms": p.bathrooms,
                        "area_sqm": float(p.area_sqm),
                        "type_name": p.property_type.name_en,
                        "district_name": p.district.name_en,
                        "image_url": p.primary_image_url,
                        "detail_url": f"/properties/{p.slug}/",
                    },
                }
            )
        return Response({"type": "FeatureCollection", "features": features})

    @action(detail=False, methods=["get"])
    def featured(self, request):
        """Returns top featured listings for homepage carousels."""
        featured_qs = self.get_queryset().filter(tier__in=["FEATURED", "PREMIUM"])[:8]
        serializer = PropertyListSerializer(featured_qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def track_click(self, request, pk=None):
        """Tracks user conversion clicks (WhatsApp or Phone call)."""
        prop = self.get_object()
        action_type = request.data.get("type", "whatsapp")

        if action_type == "whatsapp":
            Property.objects.filter(pk=prop.pk).update(whatsapp_clicks=F("whatsapp_clicks") + 1)
        elif action_type == "call":
            Property.objects.filter(pk=prop.pk).update(call_clicks=F("call_clicks") + 1)

        return Response({"status": "tracked", "action": action_type})


class PropertyTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PropertyType.objects.all()
    serializer_class = PropertyTypeSerializer
    permission_classes = [permissions.AllowAny]


class AmenityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    permission_classes = [permissions.AllowAny]
