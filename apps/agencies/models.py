"""Agency and Agent models for brokerage businesses and individual brokers."""

from django.db import models
from apps.locations.models import District


class Agency(models.Model):
    """Licensed Real Estate Brokerage Company or Developer."""

    name_en = models.CharField(max_length=150)
    name_ar = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True)
    license_no = models.CharField(max_length=60, blank=True, help_text="Ministry / Regulatory Broker License")
    logo_url = models.URLField(blank=True, default="https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=300")
    description_en = models.TextField(blank=True)
    description_ar = models.TextField(blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, related_name="agencies")
    phone = models.CharField(max_length=25, default="+96522000000")
    whatsapp = models.CharField(max_length=25, default="+96590000000")
    email = models.EmailField(blank=True, default="info@agency.com")
    website = models.URLField(blank=True)
    is_verified = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.9)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Agency"
        verbose_name_plural = "Agencies"
        ordering = ["-is_verified", "-rating", "name_en"]

    def __str__(self) -> str:
        return self.name_en


class Agent(models.Model):
    """Professional Real Estate Agent or Broker."""

    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name="agents")
    name_en = models.CharField(max_length=120)
    name_ar = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140)
    title_en = models.CharField(max_length=100, default="Senior Property Consultant")
    title_ar = models.CharField(max_length=100, default="مستشار عقاري أول")
    license_no = models.CharField(max_length=60, blank=True)
    avatar_url = models.URLField(blank=True, default="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=300")
    phone = models.CharField(max_length=25, default="+96590000001")
    whatsapp = models.CharField(max_length=25, default="+96590000001")
    email = models.EmailField(blank=True, default="agent@agency.com")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.8)
    is_verified = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Agent"
        verbose_name_plural = "Agents"
        ordering = ["-rating", "name_en"]

    def __str__(self) -> str:
        return f"{self.name_en} ({self.agency.name_en})"
