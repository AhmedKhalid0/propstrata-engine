"""Agencies API views and endpoints."""

from rest_framework import permissions, viewsets
from apps.agencies.models import Agency, Agent
from apps.agencies.serializers import AgencySerializer, AgentSerializer


class AgencyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Agency.objects.filter(is_verified=True).prefetch_related("agents")
    serializer_class = AgencySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"


class AgentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Agent.objects.filter(is_active=True).select_related("agency")
    serializer_class = AgentSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"
