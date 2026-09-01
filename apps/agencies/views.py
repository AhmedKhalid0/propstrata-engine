from django.db.models import Count, Sum
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.agencies.models import Agency, Agent
from apps.agencies.serializers import AgencySerializer, AgentSerializer
from apps.leads.models import LeadInquiry
from apps.properties.models import Property


class AgencyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Agency.objects.filter(is_verified=True).prefetch_related("agents")
    serializer_class = AgencySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"

    @action(detail=False, methods=["get"])
    def analytics(self, request):
        """Returns aggregate CRM and lead generation performance metrics."""
        total_views = Property.objects.aggregate(Sum("views_count"))["views_count__sum"] or 0
        total_wa = Property.objects.aggregate(Sum("whatsapp_clicks"))["whatsapp_clicks__sum"] or 0
        total_calls = Property.objects.aggregate(Sum("call_clicks"))["call_clicks__sum"] or 0
        total_leads = LeadInquiry.objects.count()

        top_properties = list(
            Property.objects.filter(status="ACTIVE")
            .order_by("-views_count")[:5]
            .values("id", "reference_id", "title_en", "price", "currency", "views_count", "whatsapp_clicks")
        )

        leads_by_source = dict(
            LeadInquiry.objects.values("source")
            .annotate(count=Count("id"))
            .values_list("source", "count")
        )

        return Response({
            "total_views": total_views,
            "total_whatsapp_clicks": total_wa,
            "total_call_clicks": total_calls,
            "total_inquiries": total_leads,
            "leads_by_source": leads_by_source,
            "top_performing_properties": top_properties,
        })


class AgentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Agent.objects.filter(is_active=True).select_related("agency")
    serializer_class = AgentSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"
