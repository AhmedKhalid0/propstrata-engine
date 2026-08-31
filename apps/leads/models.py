"""Lead Inquiries, WhatsApp Clicks, and Saved Searches models."""

from django.db import models
from apps.properties.models import Property


class InquirySource(models.TextChoices):
    WHATSAPP = "WHATSAPP", "WhatsApp Direct"
    PHONE_CALL = "CALL", "Phone Call"
    WEB_FORM = "FORM", "Web Contact Form"
    MOBILE_APP = "APP", "Mobile App Inquiry"


class LeadInquiry(models.Model):
    """Prospective client lead inquiry submitted for a property."""

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="inquiries")
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=25)
    email = models.EmailField(blank=True)
    message = models.TextField(blank=True)
    source = models.CharField(max_length=15, choices=InquirySource.choices, default=InquirySource.WEB_FORM)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Lead Inquiry"
        verbose_name_plural = "Lead Inquiries"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Lead from {self.name} on [{self.property.reference_id}]"


class Favorite(models.Model):
    """User bookmarked property (Session/Token bound)."""

    session_key = models.CharField(max_length=64, db_index=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Favorite"
        verbose_name_plural = "Favorites"
        unique_together = ("session_key", "property")


class SavedSearch(models.Model):
    """User saved search query criteria for email/SMS notifications."""

    session_key = models.CharField(max_length=64, db_index=True)
    title = models.CharField(max_length=150, default="My Saved Search")
    filters_query = models.CharField(max_length=500)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Saved Search"
        verbose_name_plural = "Saved Searches"
        ordering = ["-created_at"]
