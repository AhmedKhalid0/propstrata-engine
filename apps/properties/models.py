"""Core Real Estate Property models, specifications, media, and amenities."""

import uuid
from django.db import models
from apps.agencies.models import Agency, Agent
from apps.locations.models import District


class PropertyCategory(models.TextChoices):
    RESIDENTIAL = "RESIDENTIAL", "Residential"
    COMMERCIAL = "COMMERCIAL", "Commercial"
    LAND = "LAND", "Land & Plots"


class PropertyPurpose(models.TextChoices):
    FOR_RENT = "RENT", "For Rent"
    FOR_SALE = "BUY", "For Sale"
    COMMERCIAL = "COMMERCIAL", "Commercial"


class RentFrequency(models.TextChoices):
    MONTHLY = "MONTHLY", "Monthly"
    YEARLY = "YEARLY", "Yearly"
    DAILY = "DAILY", "Daily"


class FurnishingStatus(models.TextChoices):
    UNFURNISHED = "UNFURNISHED", "Unfurnished"
    SEMI_FURNISHED = "SEMI_FURNISHED", "Semi-Furnished"
    FULLY_FURNISHED = "FULLY_FURNISHED", "Fully Furnished"


class ListingTier(models.TextChoices):
    STANDARD = "STANDARD", "Standard"
    FEATURED = "FEATURED", "Featured"
    PREMIUM = "PREMIUM", "Premium"


class ListingStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    ACTIVE = "ACTIVE", "Active"
    UNDER_OFFER = "UNDER_OFFER", "Under Offer"
    SOLD_RENTED = "SOLD_RENTED", "Sold / Rented"
    ARCHIVED = "ARCHIVED", "Archived"


class PropertyType(models.Model):
    """Property sub-type (e.g. Apartment, Villa, Duplex, Office, Floor, Chalet)."""

    category = models.CharField(max_length=20, choices=PropertyCategory.choices, default=PropertyCategory.RESIDENTIAL)
    name_en = models.CharField(max_length=80)
    name_ar = models.CharField(max_length=80)
    slug = models.SlugField(max_length=90, unique=True)
    icon_svg = models.CharField(max_length=50, default="home", help_text="Lucide icon name")

    class Meta:
        verbose_name = "Property Type"
        verbose_name_plural = "Property Types"
        ordering = ["category", "name_en"]

    def __str__(self) -> str:
        return f"{self.name_en} ({self.get_category_display()})"


class Amenity(models.Model):
    """Property amenities (e.g. Swimming Pool, Gym, Sea View, Maid's Room, Balcony)."""

    name_en = models.CharField(max_length=100)
    name_ar = models.CharField(max_length=100)
    slug = models.SlugField(max_length=110, unique=True)
    icon_name = models.CharField(max_length=50, default="check-circle")

    class Meta:
        verbose_name = "Amenity"
        verbose_name_plural = "Amenities"
        ordering = ["name_en"]

    def __str__(self) -> str:
        return self.name_en


class Property(models.Model):
    """Main Real Estate Listing model with geo-coordinates, specs, and agency linkage."""

    reference_id = models.CharField(max_length=30, unique=True, db_index=True, editable=False)
    title_en = models.CharField(max_length=220)
    title_ar = models.CharField(max_length=220)
    slug = models.SlugField(max_length=260, unique=True, blank=True)
    description_en = models.TextField(blank=True)
    description_ar = models.TextField(blank=True)

    property_type = models.ForeignKey(PropertyType, on_delete=models.PROTECT, related_name="properties")
    purpose = models.CharField(max_length=15, choices=PropertyPurpose.choices, default=PropertyPurpose.FOR_RENT)
    rent_frequency = models.CharField(max_length=15, choices=RentFrequency.choices, default=RentFrequency.MONTHLY, blank=True)

    # Pricing & Currency
    price = models.DecimalField(max_digits=12, decimal_places=3, help_text="Supports KWD 3 decimals & SAR 2 decimals")
    currency = models.CharField(max_length=5, default="KWD")

    # Specifications
    area_sqm = models.DecimalField(max_digits=8, decimal_places=2, default=120.0)
    bedrooms = models.PositiveSmallIntegerField(default=2)
    master_bedrooms = models.PositiveSmallIntegerField(default=1)
    bathrooms = models.PositiveSmallIntegerField(default=2)
    parking_spaces = models.PositiveSmallIntegerField(default=1)
    furnishing = models.CharField(max_length=20, choices=FurnishingStatus.choices, default=FurnishingStatus.UNFURNISHED)

    has_maid_room = models.BooleanField(default=False)
    has_driver_room = models.BooleanField(default=False)
    has_balcony = models.BooleanField(default=False)
    has_sea_view = models.BooleanField(default=False)

    amenities = models.ManyToManyField(Amenity, blank=True, related_name="properties")

    # Location & Geo-Coordinates
    district = models.ForeignKey(District, on_delete=models.PROTECT, related_name="properties")
    address_line_en = models.CharField(max_length=255, blank=True)
    address_line_ar = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=29.3759)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=47.9774)

    # Agency & Broker Relationship
    agency = models.ForeignKey(Agency, on_delete=models.SET_NULL, null=True, blank=True, related_name="properties")
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True, related_name="properties")

    # Tier, Status & Telemetry
    tier = models.CharField(max_length=15, choices=ListingTier.choices, default=ListingTier.STANDARD)
    status = models.CharField(max_length=15, choices=ListingStatus.choices, default=ListingStatus.ACTIVE)

    views_count = models.PositiveIntegerField(default=0)
    whatsapp_clicks = models.PositiveIntegerField(default=0)
    call_clicks = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"
        ordering = ["-tier", "-created_at"]
        indexes = [
            models.Index(fields=["purpose", "status", "price"]),
            models.Index(fields=["district", "property_type"]),
        ]

    def save(self, *args, **kwargs):
        if not self.reference_id:
            self.reference_id = f"PST-{uuid.uuid4().hex[:6].upper()}"
        if not self.slug:
            self.slug = f"{self.reference_id.lower()}-{uuid.uuid4().hex[:4]}"
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"[{self.reference_id}] {self.title_en} - {self.price} {self.currency}"

    @property
    def primary_image_url(self) -> str:
        primary = self.images.filter(is_primary=True).first()
        if primary:
            return primary.image_url
        first = self.images.first()
        return first.image_url if first else "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800"

    @property
    def price_formatted(self) -> str:
        if self.price % 1 == 0:
            return f"{int(self.price):,} {self.currency}"
        return f"{self.price:,.3f} {self.currency}"


class PropertyImage(models.Model):
    """High-resolution property photography with CDN support."""

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="images")
    image_url = models.URLField(default="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=1200")
    caption = models.CharField(max_length=150, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_primary = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Property Image"
        verbose_name_plural = "Property Images"
        ordering = ["order", "id"]


class FloorPlan(models.Model):
    """Architectural 2D / 3D Floor plans."""

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="floor_plans")
    title = models.CharField(max_length=100, default="Floor Plan Layout")
    image_url = models.URLField(default="https://images.unsplash.com/photo-1574362848149-11496d93a7c7?w=1000")

    class Meta:
        verbose_name = "Floor Plan"
        verbose_name_plural = "Floor Plans"
