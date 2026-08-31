"""DRF Serializers for Locations and Geographic Taxonomies."""

from rest_framework import serializers
from apps.locations.models import City, Country, District, Governorate


class DistrictSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source="city.name_en", read_only=True)
    city_name_ar = serializers.CharField(source="city.name_ar", read_only=True)
    country_code = serializers.CharField(source="city.governorate.country.code", read_only=True)

    class Meta:
        model = District
        fields = [
            "id",
            "name_en",
            "name_ar",
            "slug",
            "city",
            "city_name",
            "city_name_ar",
            "country_code",
            "latitude",
            "longitude",
            "zoom_level",
        ]


class CitySerializer(serializers.ModelSerializer):
    districts = DistrictSerializer(many=True, read_only=True)

    class Meta:
        model = City
        fields = ["id", "name_en", "name_ar", "slug", "governorate", "districts"]


class GovernorateSerializer(serializers.ModelSerializer):
    cities = CitySerializer(many=True, read_only=True)

    class Meta:
        model = Governorate
        fields = ["id", "name_en", "name_ar", "slug", "country", "cities"]


class CountrySerializer(serializers.ModelSerializer):
    governorates = GovernorateSerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = [
            "code",
            "name_en",
            "name_ar",
            "currency_code",
            "currency_symbol_en",
            "currency_symbol_ar",
            "calling_code",
            "flag_emoji",
            "is_active",
            "governorates",
        ]
