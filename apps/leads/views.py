"""Leads and Inquiries API views."""

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.leads.models import Favorite, LeadInquiry, SavedSearch
from apps.leads.serializers import (
    FavoriteSerializer,
    LeadInquirySerializer,
    SavedSearchSerializer,
)


class LeadInquiryViewSet(viewsets.ModelViewSet):
    queryset = LeadInquiry.objects.all()
    serializer_class = LeadInquirySerializer
    permission_classes = [permissions.AllowAny]


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all().select_related("property__property_type", "property__district")
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        session_key = self.request.query_params.get("session_key")
        if session_key:
            qs = qs.filter(session_key=session_key)
        return qs

    @action(detail=False, methods=["post"])
    def toggle(self, request):
        """Toggles bookmarking a property for a user session."""
        session_key = request.data.get("session_key", "anon-session")
        property_id = request.data.get("property_id")

        if not property_id:
            return Response({"error": "property_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        fav = Favorite.objects.filter(session_key=session_key, property_id=property_id).first()
        if fav:
            fav.delete()
            return Response({"status": "removed", "is_favorited": False})
        else:
            Favorite.objects.create(session_key=session_key, property_id=property_id)
            return Response({"status": "added", "is_favorited": True})


class SavedSearchViewSet(viewsets.ModelViewSet):
    queryset = SavedSearch.objects.all()
    serializer_class = SavedSearchSerializer
    permission_classes = [permissions.AllowAny]
