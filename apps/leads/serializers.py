"""DRF Serializers for Leads, Inquiries, and Favorites."""

from rest_framework import serializers
from apps.leads.models import Favorite, LeadInquiry, SavedSearch
from apps.properties.serializers import PropertyListSerializer


class LeadInquirySerializer(serializers.ModelSerializer):
    property_ref = serializers.CharField(source="property.reference_id", read_only=True)

    class Meta:
        model = LeadInquiry
        fields = [
            "id",
            "property",
            "property_ref",
            "name",
            "phone",
            "email",
            "message",
            "source",
            "is_read",
            "created_at",
        ]


class FavoriteSerializer(serializers.ModelSerializer):
    property_details = PropertyListSerializer(source="property", read_only=True)

    class Meta:
        model = Favorite
        fields = ["id", "session_key", "property", "property_details", "created_at"]


class SavedSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedSearch
        fields = ["id", "session_key", "title", "filters_query", "email", "is_active", "created_at"]
