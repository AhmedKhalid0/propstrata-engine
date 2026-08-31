"""Deterministic seed data populating GCC countries, locations, agencies, and properties."""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "propstrata_core.settings")
django.setup()

from apps.agencies.models import Agency, Agent
from apps.locations.models import City, Country, District, Governorate
from apps.properties.models import Amenity, Property, PropertyImage, PropertyType


def seed_database():
    """Seeds database with complete GCC real estate taxonomy and sample properties."""
    print("Seeding PropStrata database...")

    # 1. Countries
    kw, _ = Country.objects.get_or_create(
        code="KW",
        defaults={
            "name_en": "Kuwait",
            "name_ar": "الكويت",
            "currency_code": "KWD",
            "currency_symbol_en": "KD",
            "currency_symbol_ar": "د.ك",
            "calling_code": "+965",
            "flag_emoji": "🇰🇼",
            "display_order": 1,
        },
    )

    sa, _ = Country.objects.get_or_create(
        code="SA",
        defaults={
            "name_en": "Saudi Arabia",
            "name_ar": "المملكة العربية السعودية",
            "currency_code": "SAR",
            "currency_symbol_en": "SAR",
            "currency_symbol_ar": "ر.س",
            "calling_code": "+966",
            "flag_emoji": "🇸🇦",
            "display_order": 2,
        },
    )

    ae, _ = Country.objects.get_or_create(
        code="AE",
        defaults={
            "name_en": "United Arab Emirates",
            "name_ar": "الإمارات العربية المتحدة",
            "currency_code": "AED",
            "currency_symbol_en": "AED",
            "currency_symbol_ar": "د.إ",
            "calling_code": "+971",
            "flag_emoji": "🇦🇪",
            "display_order": 3,
        },
    )

    # 2. Governorates & Cities & Districts (Kuwait)
    gov_hawalli, _ = Governorate.objects.get_or_create(country=kw, slug="hawalli", defaults={"name_en": "Hawalli Governorate", "name_ar": "محافظة حولي"})
    city_hawalli, _ = City.objects.get_or_create(governorate=gov_hawalli, slug="salmiya-city", defaults={"name_en": "Salmiya", "name_ar": "السالمية"})
    dist_salmiya, _ = District.objects.get_or_create(
        city=city_hawalli, slug="salmiya-block-4",
        defaults={"name_en": "Salmiya Seafront", "name_ar": "السالمية - الواجهة البحرية", "latitude": 29.3344, "longitude": 48.0772}
    )
    dist_hawalli, _ = District.objects.get_or_create(
        city=city_hawalli, slug="hawalli-commercial",
        defaults={"name_en": "Hawalli Central", "name_ar": "حولي - شارع تونس", "latitude": 29.3392, "longitude": 48.0048}
    )

    gov_capital, _ = Governorate.objects.get_or_create(country=kw, slug="capital", defaults={"name_en": "Capital Governorate", "name_ar": "محافظة العاصمة"})
    city_kuwait, _ = City.objects.get_or_create(governorate=gov_capital, slug="kuwait-city", defaults={"name_en": "Kuwait City", "name_ar": "مدينة الكويت"})
    dist_sharq, _ = District.objects.get_or_create(
        city=city_kuwait, slug="sharq-financial",
        defaults={"name_en": "Sharq Financial Hub", "name_ar": "شرق - الحي المالي", "latitude": 29.3872, "longitude": 47.9868}
    )

    # Saudi Arabia
    gov_riyadh, _ = Governorate.objects.get_or_create(country=sa, slug="riyadh-province", defaults={"name_en": "Riyadh Province", "name_ar": "منطقة الرياض"})
    city_riyadh, _ = City.objects.get_or_create(governorate=gov_riyadh, slug="riyadh", defaults={"name_en": "Riyadh", "name_ar": "الرياض"})
    dist_malqa, _ = District.objects.get_or_create(
        city=city_riyadh, slug="al-malqa",
        defaults={"name_en": "Al-Malqa Luxury District", "name_ar": "حي الملقا الراقي", "latitude": 24.7932, "longitude": 46.5982}
    )

    # 3. Property Types
    pt_apartment, _ = PropertyType.objects.get_or_create(slug="apartment", defaults={"name_en": "Apartment", "name_ar": "شقة سكنية", "category": "RESIDENTIAL", "icon_svg": "building"})
    pt_villa, _ = PropertyType.objects.get_or_create(slug="luxury-villa", defaults={"name_en": "Luxury Villa", "name_ar": "فيلا فاخرة", "category": "RESIDENTIAL", "icon_svg": "home"})
    pt_office, _ = PropertyType.objects.get_or_create(slug="commercial-office", defaults={"name_en": "Commercial Office", "name_ar": "مكتب تجاري", "category": "COMMERCIAL", "icon_svg": "briefcase"})
    pt_floor, _ = PropertyType.objects.get_or_create(slug="private-floor", defaults={"name_en": "Private Floor", "name_ar": "دور كامل", "category": "RESIDENTIAL", "icon_svg": "layers"})
    pt_chalet, _ = PropertyType.objects.get_or_create(slug="seafront-chalet", defaults={"name_en": "Seafront Chalet", "name_ar": "شاليه بحري", "category": "RESIDENTIAL", "icon_svg": "anchor"})

    # 4. Amenities
    am_pool, _ = Amenity.objects.get_or_create(slug="swimming-pool", defaults={"name_en": "Swimming Pool", "name_ar": "حمام سباحة"})
    am_sea, _ = Amenity.objects.get_or_create(slug="sea-view", defaults={"name_en": "Full Sea View", "name_ar": "إطلالة بحرية كاملة"})
    am_maid, _ = Amenity.objects.get_or_create(slug="maid-room", defaults={"name_en": "Maid's Room with Bath", "name_ar": "غرفة عاملة مع حمام"})
    am_balcony, _ = Amenity.objects.get_or_create(slug="balcony", defaults={"name_en": "Private Balcony", "name_ar": "بلكونة خاصة"})
    am_gym, _ = Amenity.objects.get_or_create(slug="gym", defaults={"name_en": "Equipped Fitness Center", "name_ar": "نادي صحي مجهز"})
    am_parking, _ = Amenity.objects.get_or_create(slug="parking", defaults={"name_en": "Covered Shaded Parking", "name_ar": "مواقف مظللة"})

    # 5. Agencies & Agents
    agency_gulf, _ = Agency.objects.get_or_create(
        slug="gulf-horizon-realty",
        defaults={
            "name_en": "Gulf Horizon Real Estate",
            "name_ar": "شركة أفق الخليج العقارية",
            "license_no": "KW-REG-4890",
            "logo_url": "https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=300",
            "description_en": "Leading premier real estate brokerage specializing in luxury waterfront apartments, private floors, and commercial towers.",
            "description_ar": "شركة رائدة في الاستشارات العقارية وإدارة الأبراج والشقق الفاخرة المطلة على البحر.",
            "phone": "+96522005500",
            "whatsapp": "+96590001122",
            "email": "info@gulfhorizon.com",
            "website": "https://gulfhorizon.example.com",
            "is_verified": True,
            "rating": 4.9,
            "district": dist_salmiya,
        },
    )

    agent_ahmed, _ = Agent.objects.get_or_create(
        agency=agency_gulf,
        slug="ahmed-al-sabah",
        defaults={
            "name_en": "Ahmed Al-Sabah",
            "name_ar": "أحمد الصباح",
            "title_en": "Head of Residential Acquisitions",
            "title_ar": "رئيس قسم العقارات السكنية",
            "license_no": "AGT-8891",
            "avatar_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=300",
            "phone": "+96590001122",
            "whatsapp": "+96590001122",
            "email": "ahmed@gulfhorizon.com",
            "rating": 4.9,
            "is_verified": True,
        },
    )

    agency_apex, _ = Agency.objects.get_or_create(
        slug="apex-capital-properties",
        defaults={
            "name_en": "Apex Capital Properties",
            "name_ar": "شركة أبيكس كابيتال العقارية",
            "license_no": "SA-REG-9102",
            "logo_url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=300",
            "description_en": "Specialized in luxury Saudi & GCC residential compounds and grade-A commercial developments.",
            "phone": "+966114008800",
            "whatsapp": "+966500008800",
            "rating": 4.8,
            "district": dist_malqa,
        },
    )

    # 6. Sample Properties
    props_data = [
        {
            "title_en": "Luxury 3BHK Sea-Front Apartment with Balcony",
            "title_ar": "شقة فاخرة 3 غرف نوم إطلالة بحرية مباشرة وبلكونة",
            "purpose": "RENT",
            "property_type": pt_apartment,
            "price": 650.0,
            "currency": "KWD",
            "area_sqm": 160.0,
            "bedrooms": 3,
            "master_bedrooms": 2,
            "bathrooms": 3,
            "parking_spaces": 2,
            "furnishing": "SEMI_FURNISHED",
            "has_maid_room": True,
            "has_balcony": True,
            "has_sea_view": True,
            "district": dist_salmiya,
            "latitude": 29.3350,
            "longitude": 48.0780,
            "agency": agency_gulf,
            "agent": agent_ahmed,
            "tier": "PREMIUM",
            "description_en": "Breathtaking panoramic Arabian Gulf views. Features high-end finishes, German kitchen appliances, master suite with walk-in closet, dedicated maid room, and 2 shaded parking slots.",
            "description_ar": "إطلالة بانورامية ساحرة على الخليج العربي في أرقى مواقع السالمية. تشطيبات ديلوكس، مطبخ مجهز، غرفة خادمة، وموقفين سيارة.",
            "images": [
                "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=1200",
                "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=1200",
                "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=1200",
            ],
            "amenities": [am_sea, am_balcony, am_maid, am_pool, am_gym, am_parking],
        },
        {
            "title_en": "Modern Duplex Villa with Private Swimming Pool",
            "title_ar": "فيلا دوبلكس عصرية مع مسبح خاص وحديقة",
            "purpose": "BUY",
            "property_type": pt_villa,
            "price": 380000.0,
            "currency": "KWD",
            "area_sqm": 450.0,
            "bedrooms": 5,
            "master_bedrooms": 4,
            "bathrooms": 6,
            "parking_spaces": 4,
            "furnishing": "UNFURNISHED",
            "has_maid_room": True,
            "has_driver_room": True,
            "has_balcony": True,
            "has_sea_view": False,
            "district": dist_hawalli,
            "latitude": 29.3400,
            "longitude": 48.0060,
            "agency": agency_gulf,
            "agent": agent_ahmed,
            "tier": "FEATURED",
            "description_en": "Super deluxe architectural masterpiece with smart home automation, private heated swimming pool, rooftop terrace, elevator, driver room, and 4 shaded parking bays.",
            "images": [
                "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=1200",
                "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=1200",
            ],
            "amenities": [am_pool, am_maid, am_parking, am_balcony],
        },
        {
            "title_en": "Grade-A Commercial Office Floor in Financial Hub",
            "title_ar": "دور مكتبي تجاري فاخر في قلب الحي المالي",
            "purpose": "COMMERCIAL",
            "property_type": pt_office,
            "price": 1400.0,
            "currency": "KWD",
            "area_sqm": 280.0,
            "bedrooms": 0,
            "bathrooms": 4,
            "parking_spaces": 6,
            "furnishing": "UNFURNISHED",
            "has_sea_view": True,
            "district": dist_sharq,
            "latitude": 29.3875,
            "longitude": 47.9870,
            "agency": agency_gulf,
            "tier": "FEATURED",
            "description_en": "Turnkey open-plan corporate headquarters with executive meeting suites, high-speed fiber connectivity, 24/7 security, and 6 allocated parking cards in Sharq.",
            "images": [
                "https://images.unsplash.com/photo-1497366216548-37526070297c?w=1200",
                "https://images.unsplash.com/photo-1497215728101-856f4ea42174?w=1200",
            ],
            "amenities": [am_parking, am_sea],
        },
        {
            "title_en": "Contemporary Luxury Villa with Landscaped Courtyard",
            "title_ar": "فيلا مودرن فاخرة مع فناء وحديقة خاصة بالملقا",
            "purpose": "BUY",
            "property_type": pt_villa,
            "price": 4200000.0,
            "currency": "SAR",
            "area_sqm": 520.0,
            "bedrooms": 6,
            "master_bedrooms": 5,
            "bathrooms": 7,
            "parking_spaces": 3,
            "furnishing": "FULLY_FURNISHED",
            "has_maid_room": True,
            "has_driver_room": True,
            "district": dist_malqa,
            "latitude": 24.7940,
            "longitude": 46.5990,
            "agency": agency_apex,
            "tier": "PREMIUM",
            "description_en": "Prestigious smart villa located in Al-Malqa Riyadh. Custom Italian marble, double-height living ceilings, private cinema room, and driver suite.",
            "images": [
                "https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=1200",
            ],
            "amenities": [am_pool, am_maid, am_gym, am_parking],
        },
    ]

    for pdata in props_data:
        images = pdata.pop("images", [])
        amenities = pdata.pop("amenities", [])

        prop, created = Property.objects.get_or_create(
            title_en=pdata["title_en"],
            defaults=pdata,
        )

        if created:
            for idx, img_url in enumerate(images):
                PropertyImage.objects.create(
                    property=prop,
                    image_url=img_url,
                    order=idx,
                    is_primary=(idx == 0),
                )
            if amenities:
                prop.amenities.set(amenities)

    print("Database seeding completed successfully!")


if __name__ == "__main__":
    seed_database()
