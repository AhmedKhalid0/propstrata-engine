"""DRF Serializers for Agencies and Agents."""

from rest_framework import serializers
from apps.agencies.models import Agency, Agent


class AgentSerializer(serializers.ModelSerializer):
    agency_name = serializers.CharField(source="agency.name_en", read_only=True)
    agency_logo = serializers.CharField(source="agency.logo_url", read_only=True)

    class Meta:
        model = Agent
        fields = [
            "id",
            "name_en",
            "name_ar",
            "slug",
            "title_en",
            "title_ar",
            "license_no",
            "avatar_url",
            "phone",
            "whatsapp",
            "email",
            "rating",
            "is_verified",
            "agency",
            "agency_name",
            "agency_logo",
        ]


class AgencySerializer(serializers.ModelSerializer):
    agents = AgentSerializer(many=True, read_only=True)
    active_properties_count = serializers.SerializerMethodField()

    class Meta:
        model = Agency
        fields = [
            "id",
            "name_en",
            "name_ar",
            "slug",
            "license_no",
            "logo_url",
            "description_en",
            "description_ar",
            "district",
            "phone",
            "whatsapp",
            "email",
            "website",
            "is_verified",
            "rating",
            "active_properties_count",
            "agents",
        ]

    def get_active_properties_count(self, obj) -> int:
        return obj.properties.filter(status="ACTIVE").count() if hasattr(obj, "properties") else 0
