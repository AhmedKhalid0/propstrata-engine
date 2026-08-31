"""Integration tests for Lead inquiries, conversion tracking, and favorites."""

from django.test import TestCase
from rest_framework.test import APIClient
from apps.locations.models import City, Country, District, Governorate
from apps.properties.models import Property, PropertyType


class TestLeadsAPI(TestCase):
    """Test leads, inquiries, and conversion tracking endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.country = Country.objects.create(code="KW", name_en="Kuwait", name_ar="الكويت")
        self.gov = Governorate.objects.create(country=self.country, name_en="Capital", slug="capital")
        self.city = City.objects.create(governorate=self.gov, name_en="Kuwait City", slug="kuwait-city")
        self.district = District.objects.create(city=self.city, name_en="Sharq", slug="sharq")
        self.pt = PropertyType.objects.create(name_en="Apartment", slug="apt")

        self.prop = Property.objects.create(
            title_en="Luxury Studio",
            title_ar="استوديو فاخر",
            property_type=self.pt,
            purpose="RENT",
            price=350.0,
            district=self.district,
        )

    def test_submit_lead_inquiry(self):
        payload = {
            "property": self.prop.id,
            "name": "Sarah Miller",
            "phone": "+96590008877",
            "email": "sarah@example.com",
            "message": "Is this studio available for immediate move-in?",
            "source": "FORM",
        }
        res = self.client.post("/api/v1/leads/inquiries/", data=payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(self.prop.inquiries.count(), 1)
        self.assertEqual(self.prop.inquiries.first().name, "Sarah Miller")

    def test_toggle_favorite(self):
        payload = {"session_key": "user-session-123", "property_id": self.prop.id}
        # Add favorite
        res1 = self.client.post("/api/v1/leads/favorites/toggle/", data=payload)
        self.assertEqual(res1.status_code, 200)
        self.assertTrue(res1.data["is_favorited"])

        # Remove favorite
        res2 = self.client.post("/api/v1/leads/favorites/toggle/", data=payload)
        self.assertEqual(res2.status_code, 200)
        self.assertFalse(res2.data["is_favorited"])

    def test_track_whatsapp_click(self):
        res = self.client.post(f"/api/v1/properties/{self.prop.id}/track_click/", data={"type": "whatsapp"})
        self.assertEqual(res.status_code, 200)
        self.prop.refresh_from_db()
        self.assertEqual(self.prop.whatsapp_clicks, 1)
