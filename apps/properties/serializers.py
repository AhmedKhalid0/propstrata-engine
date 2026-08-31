"""DRF Serializers for Property listings, specs, images, and Map GeoJSON endpoints."""

from rest_framework import serializers
from apps.agencies.serializers import AgencySerializer, AgentSerializer
from apps.locations.serializers import DistrictSerializer
from apps.properties.models import Amenity, FloorPlan, Property, PropertyImage, PropertyType


class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = ["id", "category", "name_en", "name_ar", "slug", "icon_svg"]


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ["id", "name_en", "name_ar", "slug", "icon_name"]


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ["id", "image_url", "caption", "order", "is_primary"]


class FloorPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloorPlan
        fields = ["id", "title", "image_url"]


class PropertyListSerializer(serializers.ModelSerializer):
    """Optimized lightweight serializer for Mobile Lists and Grid Search Cards."""

    type_name = serializers.CharField(source="property_type.name_en", read_only=True)
    type_name_ar = serializers.CharField(source="property_type.name_ar", read_only=True)
    district_name = serializers.CharField(source="district.name_en", read_only=True)
    district_name_ar = serializers.CharField(source="district.name_ar", read_only=True)
    city_name = serializers.CharField(source="district.city.name_en", read_only=True)
    country_code = serializers.CharField(source="district.city.governorate.country.code", read_only=True)
    primary_image = serializers.CharField(source="primary_image_url", read_only=True)
    price_display = serializers.CharField(source="price_formatted", read_only=True)
    agency_name = serializers.CharField(source="agency.name_en", read_only=True, default=None)
    agency_logo = serializers.CharField(source="agency.logo_url", read_only=True, default=None)

    class Meta:
        model = Property
        fields = [
            "id",
            "reference_id",
            "title_en",
            "title_ar",
            "slug",
            "purpose",
            "rent_frequency",
            "price",
            "currency",
            "price_display",
            "area_sqm",
            "bedrooms",
            "bathrooms",
            "furnishing",
            "tier",
            "status",
            "type_name",
            "type_name_ar",
            "district_name",
            "district_name_ar",
            "city_name",
            "country_code",
            "primary_image",
            "agency_name",
            "agency_logo",
            "latitude",
            "longitude",
            "created_at",
        ]


class PropertyDetailSerializer(serializers.ModelSerializer):
    """Full detail serializer for Property details view in Mobile & Web."""

    property_type = PropertyTypeSerializer(read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    images = PropertyImageSerializer(many=True, read_only=True)
    floor_plans = FloorPlanSerializer(many=True, read_only=True)
    district = DistrictSerializer(read_only=True)
    agency = AgencySerializer(read_only=True)
    agent = AgentSerializer(read_only=True)
    primary_image = serializers.CharField(source="primary_image_url", read_only=True)
    price_display = serializers.CharField(source="price_formatted", read_only=True)

    class Meta:
        model = Property
        fields = [
            "id",
            "reference_id",
            "title_en",
            "title_ar",
            "slug",
            "description_en",
            "description_ar",
            "purpose",
            "rent_frequency",
            "price",
            "currency",
            "price_display",
            "area_sqm",
            "bedrooms",
            "master_bedrooms",
            "bathrooms",
            "parking_spaces",
            "furnishing",
            "has_maid_room",
            "has_driver_room",
            "has_balcony",
            "has_sea_view",
            "property_type",
            "district",
            "address_line_en",
            "address_line_ar",
            "latitude",
            "longitude",
            "agency",
            "agent",
            "tier",
            "status",
            "views_count",
            "whatsapp_clicks",
            "call_clicks",
            "primary_image",
            "amenities",
            "images",
            "floor_plans",
            "created_at",
            "updated_at",
        ]


class PropertyCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating listings via API."""

    class Meta:
        model = Property
        fields = [
            "id",
            "title_en",
            "title_ar",
            "description_en",
            "description_ar",
            "property_type",
            "purpose",
            "rent_frequency",
            "price",
            "currency",
            "area_sqm",
            "bedrooms",
            "bathrooms",
            "furnishing",
            "district",
            "latitude",
            "longitude",
            "agency",
            "agent",
            "amenities",
        ]
