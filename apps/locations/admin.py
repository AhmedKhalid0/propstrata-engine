"""Admin interface for location models."""

from django.contrib import admin
from apps.locations.models import City, Country, District, Governorate


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("code", "name_en", "name_ar", "currency_code", "calling_code", "is_active", "display_order")
    list_editable = ("is_active", "display_order")
    search_fields = ("name_en", "name_ar", "code")


@admin.register(Governorate)
class GovernorateAdmin(admin.ModelAdmin):
    list_display = ("name_en", "name_ar", "slug", "country")
    list_filter = ("country",)
    search_fields = ("name_en", "name_ar")
    prepopulated_fields = {"slug": ("name_en",)}


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name_en", "name_ar", "slug", "governorate")
    list_filter = ("governorate__country", "governorate")
    search_fields = ("name_en", "name_ar")
    prepopulated_fields = {"slug": ("name_en",)}


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ("name_en", "name_ar", "slug", "city", "latitude", "longitude")
    list_filter = ("city__governorate__country", "city__governorate", "city")
    search_fields = ("name_en", "name_ar")
    prepopulated_fields = {"slug": ("name_en",)}
