"""Integration tests for GeoJSON Map Search endpoints."""

from django.test import TestCase
from rest_framework.test import APIClient
from apps.locations.models import City, Country, District, Governorate
from apps.properties.models import Property, PropertyType


class TestGeoSearch(TestCase):
    """Test map endpoint GeoJSON outputs and coordinate payloads."""

    def setUp(self):
        self.client = APIClient()
        self.country = Country.objects.create(code="KW", name_en="Kuwait", name_ar="الكويت")
        self.gov = Governorate.objects.create(country=self.country, name_en="Hawalli", slug="hawalli")
        self.city = City.objects.create(governorate=self.gov, name_en="Salmiya", slug="salmiya")
        self.dist1 = District.objects.create(city=self.city, name_en="Salmiya East", slug="salmiya-e", latitude=29.3344, longitude=48.0772)

        self.pt = PropertyType.objects.create(name_en="Apartment", slug="apt")

        Property.objects.create(
            title_en="Seafront Luxury Flat",
            title_ar="شقة بحرية",
            property_type=self.pt,
            purpose="RENT",
            price=700.0,
            district=self.dist1,
            latitude=29.3344,
            longitude=48.0772,
            status="ACTIVE",
        )

    def test_map_geojson_feature_collection(self):
        res = self.client.get("/api/v1/properties/map/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["type"], "FeatureCollection")
        self.assertGreater(len(res.data["features"]), 0)

        feat = res.data["features"][0]
        self.assertEqual(feat["geometry"]["type"], "Point")
        self.assertEqual(feat["geometry"]["coordinates"], [48.0772, 29.3344])  # [lon, lat]
        self.assertIn("price_display", feat["properties"])
        self.assertIn("700", feat["properties"]["price_display"])
