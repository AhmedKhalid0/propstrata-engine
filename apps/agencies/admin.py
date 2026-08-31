"""Admin interface for agencies and agents."""

from django.contrib import admin
from apps.agencies.models import Agency, Agent


class AgentInline(admin.TabularInline):
    model = Agent
    extra = 1
    fields = ("name_en", "name_ar", "title_en", "phone", "whatsapp", "rating", "is_verified", "is_active")


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ("name_en", "name_ar", "license_no", "phone", "whatsapp", "is_verified", "rating")
    list_filter = ("is_verified", "rating")
    search_fields = ("name_en", "name_ar", "license_no")
    prepopulated_fields = {"slug": ("name_en",)}
    inlines = [AgentInline]


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ("name_en", "name_ar", "agency", "title_en", "phone", "whatsapp", "rating", "is_verified", "is_active")
    list_filter = ("is_verified", "is_active", "agency")
    search_fields = ("name_en", "name_ar", "agency__name_en")
    prepopulated_fields = {"slug": ("name_en",)}
