"""Integration tests for Property REST API endpoints."""

from django.test import TestCase
from rest_framework.test import APIClient
from apps.locations.models import City, Country, District, Governorate
from apps.properties.models import Property, PropertyType


class TestPropertyAPI(TestCase):
    """Test REST endpoints for properties listing, filters, and detail."""

    def setUp(self):
        self.client = APIClient()
        self.country = Country.objects.create(code="KW", name_en="Kuwait", name_ar="الكويت")
        self.gov = Governorate.objects.create(country=self.country, name_en="Hawalli", name_ar="حولي", slug="hawalli")
        self.city = City.objects.create(governorate=self.gov, name_en="Salmiya", name_ar="السالمية", slug="salmiya")
        self.district = District.objects.create(city=self.city, name_en="Salmiya Seafront", name_ar="السالمية", slug="salmiya-sf")

        self.pt_apt = PropertyType.objects.create(name_en="Apartment", name_ar="شقة", slug="apt")
        self.pt_villa = PropertyType.objects.create(name_en="Villa", name_ar="فيلا", slug="villa")

        self.prop1 = Property.objects.create(
            title_en="Beachside Apartment",
            title_ar="شقة شاطئية",
            property_type=self.pt_apt,
            purpose="RENT",
            price=600.0,
            bedrooms=3,
            bathrooms=2,
            district=self.district,
            status="ACTIVE",
        )

        self.prop2 = Property.objects.create(
            title_en="Grand Villa For Sale",
            title_ar="فيلا كبرى للبيع",
            property_type=self.pt_villa,
            purpose="BUY",
            price=450000.0,
            bedrooms=6,
            bathrooms=7,
            district=self.district,
            status="ACTIVE",
        )

    def test_list_properties(self):
        res = self.client.get("/api/v1/properties/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], 2)

    def test_filter_by_purpose(self):
        res = self.client.get("/api/v1/properties/?purpose=RENT")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], 1)
        self.assertEqual(res.data["results"][0]["title_en"], "Beachside Apartment")

    def test_filter_by_price_range(self):
        res = self.client.get("/api/v1/properties/?min_price=1000")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], 1)
        self.assertEqual(res.data["results"][0]["title_en"], "Grand Villa For Sale")

    def test_retrieve_property_detail(self):
        res = self.client.get(f"/api/v1/properties/{self.prop1.id}/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["reference_id"], self.prop1.reference_id)
        self.assertEqual(res.data["views_count"], 1)  # Incremented views
