"""Unit tests for PropStrata database models."""

from django.test import TestCase
from apps.agencies.models import Agency, Agent
from apps.locations.models import City, Country, District, Governorate
from apps.properties.models import Amenity, Property, PropertyType


class TestPropStrataModels(TestCase):
    """Test model constraints, auto-generation, and relationships."""

    def setUp(self):
        self.country = Country.objects.create(
            code="KW",
            name_en="Kuwait",
            name_ar="الكويت",
            currency_code="KWD",
            currency_symbol_en="KD",
        )
        self.gov = Governorate.objects.create(country=self.country, name_en="Hawalli", name_ar="حولي", slug="hawalli")
        self.city = City.objects.create(governorate=self.gov, name_en="Salmiya", name_ar="السالمية", slug="salmiya")
        self.district = District.objects.create(
            city=self.city,
            name_en="Salmiya Block 4",
            name_ar="السالمية قطعة 4",
            slug="salmiya-b4",
            latitude=29.3344,
            longitude=48.0772,
        )
        self.prop_type = PropertyType.objects.create(
            category="RESIDENTIAL",
            name_en="Apartment",
            name_ar="شقة",
            slug="apartment",
        )
        self.agency = Agency.objects.create(
            name_en="Test Horizon Realty",
            name_ar="شركة الأفق للتجربة",
            slug="test-horizon",
            phone="+96522001122",
            whatsapp="+96590001122",
        )

    def test_property_creation_and_auto_reference_id(self):
        prop = Property.objects.create(
            title_en="Test Modern Flat",
            title_ar="شقة عصرية تجريبية",
            property_type=self.prop_type,
            purpose="RENT",
            price=550.0,
            currency="KWD",
            area_sqm=120.0,
            bedrooms=2,
            bathrooms=2,
            district=self.district,
            agency=self.agency,
        )

        self.assertTrue(prop.reference_id.startswith("PST-"))
        self.assertIn("pst-", prop.slug)
        self.assertEqual(prop.price_formatted, "550 KWD")

    def test_agency_and_agent_relationship(self):
        agent = Agent.objects.create(
            agency=self.agency,
            name_en="Tariq Ali",
            name_ar="طارق علي",
            slug="tariq-ali",
            phone="+96599887766",
            whatsapp="+96599887766",
        )
        self.assertEqual(agent.agency.name_en, "Test Horizon Realty")
        self.assertEqual(self.agency.agents.count(), 1)
