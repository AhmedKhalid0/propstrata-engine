# Broker CRM & WhatsApp Lead Conversion Playbook

This document details the multi-tenancy agency architecture and automated WhatsApp conversion attribution engine within **PropStrata-Engine**.

---

## 1. Multi-Tenancy Agency Hierarchy

```mermaid
graph TD
    Agency["🏢 Certified Real Estate Brokerage Agency<br/>(Commercial Registration & Verified Badge)"]
    
    Agency --> Agent1["👤 Managing Partner / Principal Broker"]
    Agency --> Agent2["👤 Senior Residential Specialist"]
    Agency --> Agent3["👤 Commercial Leasing Consultant"]
    
    Agent1 --> Prop1["🏡 Luxury Penthouse (PST-1001)"]
    Agent2 --> Prop2["🏢 Commercial Office Floor (PST-1002)"]
    Agent3 --> Prop3["🏖️ Seafront Villa (PST-1003)"]
```

---

## 2. Dynamic WhatsApp Deep-Link Constructor

PropStrata eliminates friction for property buyers by constructing intelligent prefilled WhatsApp URLs that preserve listing context across platforms:

```text
https://wa.me/{agent_whatsapp}?text={encoded_message}
```

### Prefilled Parameter Structure:
* **Property Reference**: `[PST-589628]`
* **Property Title**: `Contemporary Luxury Villa with Landscaped Courtyard`
* **Asking Price**: `4,200,000 SAR`
* **Canonical URL**: `https://propstrata.com/properties/pst-589628-5fd1/`

---

## 3. Lead Conversion Pipeline Stages

```mermaid
stateDiagram-v2
    [*] --> NewLead: Web Form / WhatsApp Click Tracked
    NewLead --> Contacted: Broker Initiates Direct Chat / Call
    Contacted --> ViewingScheduled: Physical / Virtual Site Inspection
    ViewingScheduled --> OfferSubmitted: Letter of Intent (LOI) Received
    OfferSubmitted --> ClosedWon: Contract Signed & Commission Recorded
    OfferSubmitted --> ClosedLost: Incompatible Terms / Price
```

---

## 4. CRM Telemetry & Conversion Rate Formula

Agencies access real-time analytics in the dashboard (`/agencies/analytics/`):

$$\text{Conversion Rate} = \left( \frac{\text{WhatsApp Clicks} + \text{Phone Calls} + \text{Web Form Leads}}{\text{Total Unique Listing Views}} \right) \times 100$$
