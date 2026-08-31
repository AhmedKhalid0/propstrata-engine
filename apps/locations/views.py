"""Location API views and GeoJSON endpoints."""

from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.locations.models import City, Country, District, Governorate
from apps.locations.serializers import (
    CitySerializer,
    CountrySerializer,
    DistrictSerializer,
    GovernorateSerializer,
)


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.filter(is_active=True).prefetch_related("governorates__cities__districts")
    serializer_class = CountrySerializer
    permission_classes = [permissions.AllowAny]


class GovernorateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Governorate.objects.all().select_related("country").prefetch_related("cities__districts")
    serializer_class = GovernorateSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        country_code = self.request.query_params.get("country")
        if country_code:
            qs = qs.filter(country__code__iexact=country_code)
        return qs


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all().select_related("governorate").prefetch_related("districts")
    serializer_class = CitySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        governorate_id = self.request.query_params.get("governorate")
        if governorate_id:
            qs = qs.filter(governorate_id=governorate_id)
        return qs


class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = District.objects.all().select_related("city__governorate__country")
    serializer_class = DistrictSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        city_slug = self.request.query_params.get("city")
        if city_slug:
            qs = qs.filter(city__slug=city_slug)
        return qs

    @action(detail=False, methods=["get"])
    def geojson(self, request):
        """Returns lightweight GeoJSON FeatureCollection of all districts."""
        districts = self.get_queryset()
        features = [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(d.longitude), float(d.latitude)],
                },
                "properties": {
                    "id": d.id,
                    "name_en": d.name_en,
                    "name_ar": d.name_ar,
                    "slug": d.slug,
                    "city": d.city.name_en,
                },
            }
            for d in districts
        ]
        return Response({"type": "FeatureCollection", "features": features})
