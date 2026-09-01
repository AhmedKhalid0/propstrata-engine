# PropStrata Mobile & Frontend REST API Reference (v1)

Base API Path: `/api/v1/`  
Authentication: Session & Token Authentication Supported  
Content-Type: `application/json`  

---

## 1. Overview & Response Format

All endpoints follow standard REST principles and return JSON payloads. Listing endpoints feature paginated envelopes:

```json
{
  "count": 42,
  "next": "/api/v1/properties/?page=2",
  "previous": null,
  "results": [ ... ]
}
```

---

## 2. Properties API (`/api/v1/properties/`)

### 2.1 List Properties (Faceted Search & Filters)
* **Method**: `GET`
* **Path**: `/api/v1/properties/`
* **Query Parameters**:
  * `purpose` (string): `RENT`, `BUY`, `COMMERCIAL`
  * `type` (string): Property type slug (e.g. `apartment`, `villa`, `office`)
  * `bedrooms` (integer): Exact number of bedrooms (e.g. `3`)
  * `min_price` (float): Minimum price filter
  * `max_price` (float): Maximum price filter
  * `district` (string): District slug (e.g. `salmiya-sf`, `al-malqa`)
  * `q` (string): Full-text keyword search against English & Arabic titles
  * `ordering` (string): Sort field (`-created_at`, `price`, `-price`, `-views_count`)

#### Example cURL Request:
```bash
curl -X GET "http://127.0.0.1:8097/api/v1/properties/?purpose=RENT&bedrooms=3&min_price=500" \
     -H "Accept: application/json"
```

---

### 2.2 Interactive GeoJSON Map Pins
* **Method**: `GET`
* **Path**: `/api/v1/properties/map/`
* **Description**: Returns lightweight `FeatureCollection` payload optimized for Leaflet / Mapbox price pin markers.

#### Example JSON Response:
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [48.0772, 29.3344]
      },
      "properties": {
        "id": 1,
        "reference_id": "PST-FCC07D",
        "title": "Luxury 3BHK Sea-Front Apartment with Balcony",
        "title_ar": "شقة فاخرة 3 غرف نوم مطلة على البحر مع بلكونة",
        "price": 650.0,
        "price_display": "650 KWD",
        "currency": "KWD",
        "purpose": "RENT",
        "bedrooms": 3,
        "bathrooms": 3,
        "area_sqm": 185.0,
        "type_name": "Apartment",
        "district_name": "Salmiya Seafront",
        "image_url": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800",
        "detail_url": "/properties/pst-fcc07d-5fd1/"
      }
    }
  ]
}
```

---

### 2.3 Property Comparison Matrix
* **Method**: `GET`
* **Path**: `/api/v1/properties/compare/?ids=1,2,3`
* **Description**: Returns side-by-side comparative matrices for up to 4 properties with calculated price per $m^2$ and complete specifications.

---

### 2.4 Conversion Click Tracking
* **Method**: `POST`
* **Path**: `/api/v1/properties/{id}/track_click/`
* **Payload**: `{"type": "whatsapp"}` or `{"type": "call"}`
* **Description**: Atomically increments conversion click telemetry for broker reporting.

---

## 3. Locations & Regional Taxonomy (`/api/v1/locations/`)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/locations/countries/` | List GCC countries with currencies & dialing codes |
| `GET` | `/api/v1/locations/governorates/` | List regional governorates |
| `GET` | `/api/v1/locations/cities/` | List metropolitan cities |
| `GET` | `/api/v1/locations/districts/` | List neighborhoods with centroid coordinates |
| `GET` | `/api/v1/locations/districts/geojson/` | District spatial polygons for map boundaries |

---

## 4. Agency Directory & Analytics (`/api/v1/agencies/`)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/agencies/` | Directory of verified brokerage companies |
| `GET` | `/api/v1/agencies/{slug}/` | Agency profile with agent roster and listings |
| `GET` | `/api/v1/agencies/analytics/` | Aggregate CRM performance & lead channel distribution |

---

## 5. Leads & Seeker Inquiries (`/api/v1/leads/`)

### 5.1 Submit Lead Inquiry
* **Method**: `POST`
* **Path**: `/api/v1/leads/inquiries/`
* **Payload**:
```json
{
  "property": 1,
  "name": "Sarah Miller",
  "phone": "+96590008877",
  "email": "sarah@example.com",
  "message": "Is this property available for viewing tomorrow?",
  "source": "FORM"
}
```
* **Response**: `201 Created`

### 5.2 Toggle Saved Favorite
* **Method**: `POST`
* **Path**: `/api/v1/leads/favorites/toggle/`
* **Payload**: `{"session_key": "user_session_abc123", "property_id": 1}`
* **Response**: `{"is_favorited": true}`
