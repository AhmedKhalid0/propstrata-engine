"""Admin interface for leads and favorites."""

from django.contrib import admin
from apps.leads.models import Favorite, LeadInquiry, SavedSearch


@admin.register(LeadInquiry)
class LeadInquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "property", "source", "is_read", "created_at")
    list_filter = ("source", "is_read", "created_at")
    search_fields = ("name", "phone", "email", "property__reference_id")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("session_key", "property", "created_at")
    search_fields = ("session_key", "property__reference_id")


@admin.register(SavedSearch)
class SavedSearchAdmin(admin.ModelAdmin):
    list_display = ("title", "email", "is_active", "created_at")
    search_fields = ("title", "email", "filters_query")
