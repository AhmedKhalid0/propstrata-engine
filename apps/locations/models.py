"""Geographical and Administrative Hierarchy models for GCC and MENA regions."""

from django.db import models


class Country(models.Model):
    """Supported Country with regional currency and dialing code."""

    code = models.CharField(max_length=2, primary_key=True, help_text="ISO 3166-1 alpha-2 (e.g. KW, SA, AE)")
    name_en = models.CharField(max_length=100)
    name_ar = models.CharField(max_length=100)
    currency_code = models.CharField(max_length=5, default="KWD")
    currency_symbol_en = models.CharField(max_length=10, default="KD")
    currency_symbol_ar = models.CharField(max_length=10, default="د.ك")
    calling_code = models.CharField(max_length=10, default="+965")
    flag_emoji = models.CharField(max_length=10, default="🇰🇼")
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ["display_order", "name_en"]

    def __str__(self) -> str:
        return f"{self.flag_emoji} {self.name_en} ({self.code})"


class Governorate(models.Model):
    """Governorate or Province (e.g. Hawalli, Capital, Riyadh Province)."""

    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="governorates")
    name_en = models.CharField(max_length=120)
    name_ar = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, db_index=True)

    class Meta:
        verbose_name = "Governorate / Region"
        verbose_name_plural = "Governorates / Regions"
        unique_together = ("country", "slug")
        ordering = ["name_en"]

    def __str__(self) -> str:
        return f"{self.name_en} ({self.country.code})"


class City(models.Model):
    """City or Major Municipality."""

    governorate = models.ForeignKey(Governorate, on_delete=models.CASCADE, related_name="cities")
    name_en = models.CharField(max_length=120)
    name_ar = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, db_index=True)

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"
        unique_together = ("governorate", "slug")
        ordering = ["name_en"]

    def __str__(self) -> str:
        return f"{self.name_en}, {self.governorate.name_en}"


class District(models.Model):
    """Neighborhood or Specific Urban District with geo-coordinates."""

    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="districts")
    name_en = models.CharField(max_length=120)
    name_ar = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, db_index=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=29.3759)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=47.9774)
    zoom_level = models.PositiveSmallIntegerField(default=14)

    class Meta:
        verbose_name = "District / Neighborhood"
        verbose_name_plural = "Districts / Neighborhoods"
        unique_together = ("city", "slug")
        ordering = ["name_en"]

    def __str__(self) -> str:
        return f"{self.name_en} - {self.city.name_en}"
