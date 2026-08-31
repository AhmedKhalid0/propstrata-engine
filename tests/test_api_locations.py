"""Integration tests for Location taxonomy endpoints."""

from django.test import TestCase
from rest_framework.test import APIClient
from apps.locations.models import City, Country, District, Governorate


class TestLocationAPI(TestCase):
    """Test locations, countries, and districts endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.country = Country.objects.create(
            code="KW", name_en="Kuwait", name_ar="الكويت", currency_code="KWD"
        )
        self.gov = Governorate.objects.create(country=self.country, name_en="Capital", name_ar="العاصمة", slug="capital")
        self.city = City.objects.create(governorate=self.gov, name_en="Kuwait City", name_ar="مدينة الكويت", slug="kuwait-city")
        self.district = District.objects.create(
            city=self.city, name_en="Sharq", name_ar="شرق", slug="sharq", latitude=29.3872, longitude=47.9868
        )

    def test_list_countries(self):
        res = self.client.get("/api/v1/locations/countries/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data["results"]), 1)
        self.assertEqual(res.data["results"][0]["code"], "KW")

    def test_districts_geojson_endpoint(self):
        res = self.client.get("/api/v1/locations/districts/geojson/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["type"], "FeatureCollection")
        self.assertEqual(len(res.data["features"]), 1)
        self.assertEqual(res.data["features"][0]["properties"]["name_en"], "Sharq")
