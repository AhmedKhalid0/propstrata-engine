"""Admin interface for Property, Image, FloorPlan, Type, and Amenity models."""

from django.contrib import admin
from apps.properties.models import Amenity, FloorPlan, Property, PropertyImage, PropertyType


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 2
    fields = ("image_url", "caption", "order", "is_primary")


class FloorPlanInline(admin.TabularInline):
    model = FloorPlan
    extra = 1
    fields = ("title", "image_url")


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "reference_id",
        "title_en",
        "purpose",
        "property_type",
        "price",
        "currency",
        "district",
        "tier",
        "status",
        "views_count",
        "whatsapp_clicks",
    )
    list_filter = ("purpose", "tier", "status", "property_type", "district__city__governorate__country", "furnishing")
    search_fields = ("reference_id", "title_en", "title_ar", "description_en")
    inlines = [PropertyImageInline, FloorPlanInline]
    filter_horizontal = ("amenities",)
    readonly_fields = ("reference_id", "slug", "views_count", "whatsapp_clicks", "call_clicks", "created_at", "updated_at")


@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ("name_en", "name_ar", "category", "slug", "icon_svg")
    list_filter = ("category",)
    search_fields = ("name_en", "name_ar")
    prepopulated_fields = {"slug": ("name_en",)}


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name_en", "name_ar", "slug", "icon_name")
    search_fields = ("name_en", "name_ar")
    prepopulated_fields = {"slug": ("name_en",)}
