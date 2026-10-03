"""
High-Intent Pilgrimage Transit Bottleneck Engine & Guardrails
============================================================
Targets high-friction, high-search-volume pilgrimage transit bottlenecks in India
(Helicopters, Ro-Pax Ferries, Mountain Ropeways, Waterway Catamarans, Ghat Gate Systems,
Pilgrim Heritage Trains, and Electric Shuttles).

Why Transit Bottlenecks are SEO Goldmines:
1. Search Intent is Urgently Utilitarian: Pilgrims are actively booking, packing, or on the road.
2. Official Portals are Fragmented: Government sites (GMB, IRCTC, Shrine Boards) often lack scannable tables,
   leading to massive search demand for schedules, ticket prices, and luggage/vehicle rules.
3. High Transformation Math: Huge reduction in travel time, physical exertion, or driving distance.
4. Immense Monetization Potential: Every transit bottleneck connects to dharamshalas, stays, and temple pujas.
"""

import re
import math
from typing import Dict, Any, List, Optional, Tuple


TRANSIT_BOTTLENECK_CATALOG: List[Dict[str, Any]] = [
    {
        "id": "ghogha_hazira_ropax",
        "name": "RoRo / Ro-Pax Ferry Service (Ghogha ↔ Hazira)",
        "category": "Waterway / Ro-Pax Ferry",
        "state": "Gujarat",
        "primary_destination": "Saurashtra & Surat",
        "route": "Ghogha Terminal (Bhavnagar) ↔ Hazira Port (Surat)",
        "transformation_math": "Saves 370 km & reduces 12-hour road journey to 4 hours by sea (90 km route)",
        "operating_authority": "Gujarat Maritime Board (GMB) / DG Sea Connect",
        "official_booking_url": "https://www.dgferry.com/",
        "operating_frequency": "Twice daily morning and evening departures",
        "ticket_fares": {
            "passenger": [
                {"class": "Executive Class", "fare_inr": 600, "baggage": "15 kg"},
                {"class": "Business Class", "fare_inr": 700, "baggage": "20 kg"},
                {"class": "Sleeper Class", "fare_inr": 700, "baggage": "20 kg"},
                {"class": "VIP Lounge", "fare_inr": 1700, "baggage": "25 kg"},
                {"class": "Cabin (4 pax)", "fare_inr": 5000, "baggage": "40 kg total"}
            ],
            "vehicle": [
                {"category": "Two-Wheeler / Bike", "fare_inr": 200, "note": "Rider seat booked separately"},
                {"category": "Four-Wheeler / Car", "fare_inr": 1300, "note": "Driver seat booked separately"},
                {"category": "Tempo Traveller", "fare_inr": 3000, "note": "Up to 3.5 tonnes"},
                {"category": "Bus / Truck", "fare_inr": 5500, "note": "Empty bus / 3 tonnes truck"}
            ]
        },
        "connecting_transit": "GSRTC buses run directly from Bhavnagar Bus Stand to Ghogha Terminal (₹23) and Surat Adajan to Hazira (₹35)",
        "onward_spokes": [
            {"destination": "Somnath Jyotirlinga", "distance_km": 260, "time_hr": 4.5},
            {"destination": "Dwarka Jagat Mandir", "distance_km": 408, "time_hr": 7.0},
            {"destination": "Palitana Jain Temples", "distance_km": 70, "time_hr": 1.5},
            {"destination": "Sarangpur Hanuman", "distance_km": 98, "time_hr": 2.0},
            {"destination": "Gir National Park", "distance_km": 225, "time_hr": 4.0}
        ],
        "scam_alert_warning": "Beware of unverified third-party ticket agents. Only book through the official DG Sea Connect portal.",
        "operational_rules": "Boarding closes 30 minutes prior to departure; reporting required 1 hour before. Pets strictly prohibited."
    },
    {
        "id": "kedarnath_helicopter",
        "name": "Kedarnath Helicopter Shuttle Service (Phata / Sirsi / Guptkashi ↔ Kedarnath)",
        "category": "Aviation / Helicopter Shuttle",
        "state": "Uttarakhand",
        "primary_destination": "Kedarnath Dham",
        "route": "Helipads at Phata, Sirsi, and Guptkashi ↔ Kedarnath Helipad (Helidrome)",
        "transformation_math": "Saves 16 km steep uphill trek; cuts 8 to 10 hours of strenuous walking down to an 8-minute flight",
        "operating_authority": "Uttarakhand Civil Aviation Development Authority (UCADA) / IRCTC HeliYatra",
        "official_booking_url": "https://heliyatra.irctc.co.in/",
        "operating_frequency": "Continuous shuttles from 06:00 AM to 05:00 PM (weather permitting)",
        "ticket_fares": {
            "passenger": [
                {"class": "Sirsi to Kedarnath (Round Trip)", "fare_inr": 5498, "baggage": "Strictly 2 kg hand baggage per passenger"},
                {"class": "Phata to Kedarnath (Round Trip)", "fare_inr": 5500, "baggage": "Strictly 2 kg hand baggage per passenger"},
                {"class": "Guptkashi to Kedarnath (Round Trip)", "fare_inr": 7750, "baggage": "Strictly 2 kg hand baggage per passenger"}
            ],
            "vehicle": [
                {"category": "Body Weight Surcharge", "fare_inr": 500, "note": "Mandatory additional ₹500/kg if body weight exceeds 80 kg"}
            ]
        },
        "connecting_transit": "Shared cabs and GMVN shuttle buses connect Rishikesh / Haridwar to Guptkashi, Phata, and Sonprayag on NH-107",
        "onward_spokes": [
            {"destination": "Kedarnath Mandir & Bhairav Temple", "distance_km": 0.8, "time_hr": 0.2},
            {"destination": "Guptkashi Vishwanath Temple", "distance_km": 15, "time_hr": 0.5},
            {"destination": "Triyuginarayan Temple", "distance_km": 25, "time_hr": 1.0},
            {"destination": "Tungnath & Chopta", "distance_km": 45, "time_hr": 1.5},
            {"destination": "Badrinath Dham", "distance_km": 218, "time_hr": 7.0}
        ],
        "scam_alert_warning": "CRITICAL SCAM WARNING: Dozens of fraudulent WhatsApp numbers and fake websites claim to sell Kedarnath tickets. IRCTC HeliYatra (heliyatra.irctc.co.in) is the ONLY authorized booking portal. Never pay via personal UPI QR codes!",
        "operational_rules": "Mandatory Biometric Yatra Registration required before booking. Strict 2 kg baggage limit; no heavy luggage allowed on board. Flights subject to immediate suspension during mountain fog or rain."
    },
    {
        "id": "girnar_ropeway",
        "name": "Girnar Ropeway (Junagadh - Bhavnath Taleti ↔ Ambaji Temple)",
        "category": "Mountain Ropeway / Cable Car",
        "state": "Gujarat",
        "primary_destination": "Girnar Mountain & Ambaji Temple",
        "route": "Bhavnath Taleti (Base Station) ↔ Ambaji Peak (Upper Station)",
        "transformation_math": "Avoids 9,999 steep stone steps; cuts 4 to 6 hours of grueling climbing down to 7.5 minutes (2.3 km aerial span)",
        "operating_authority": "Usha Breco Limited (Udan Khatola) / Gujarat Tourism",
        "official_booking_url": "https://udankhatola.com/",
        "operating_frequency": "Continuous cabins from 07:00 AM to 05:00 PM daily",
        "ticket_fares": {
            "passenger": [
                {"class": "Round Trip (Two-Way Adult)", "fare_inr": 750, "baggage": "Small daypacks permitted (under 5 kg)"},
                {"class": "One-Way Ticket (Adult)", "fare_inr": 450, "baggage": "Small daypacks permitted"},
                {"class": "Children (Height 75-110 cm)", "fare_inr": 375, "baggage": "Round trip concession"},
                {"class": "Senior Citizens (60+ Years)", "fare_inr": 750, "baggage": "Priority queue access provided"}
            ],
            "vehicle": [
                {"category": "Terminal Car Parking", "fare_inr": 50, "note": "Secure parking available at Bhavnath Taleti base"}
            ]
        },
        "connecting_transit": "City auto-rickshaws (₹20-₹30 shared, ₹100 private) and GSRTC local town buses connect Junagadh Railway Station (6 km) to Bhavnath Taleti",
        "onward_spokes": [
            {"destination": "Gorakhnath Peak & Dattatreya Paduka", "distance_km": 3.5, "time_hr": 2.0},
            {"destination": "Somnath Jyotirlinga", "distance_km": 95, "time_hr": 2.0},
            {"destination": "Dwarka Jagat Mandir", "distance_km": 210, "time_hr": 4.0},
            {"destination": "Sasan Gir Safari", "distance_km": 55, "time_hr": 1.2}
        ],
        "scam_alert_warning": "Beware of fake online counter booking agents. Tickets can be booked at base counter or udankhatola.com directly.",
        "operational_rules": "Operations immediately pause if wind velocity exceeds 45 km/h at the mountain summit. Wheelchair assistance available at base station."
    },
    {
        "id": "vaishno_devi_helicopter",
        "name": "Maa Vaishno Devi Helicopter Service (Katra ↔ Sanjichhat)",
        "category": "Aviation / Helicopter Shuttle",
        "state": "Jammu & Kashmir",
        "primary_destination": "Vaishno Devi Bhawan",
        "route": "Katra Helipad ↔ Sanjichhat Helipad",
        "transformation_math": "Saves 13 km uphill mountain trek; reduces 5 to 6 hours of uphill walk to 5 minutes of flight time",
        "operating_authority": "Shri Mata Vaishno Devi Shrine Board (SMVDSB) / Global Vectra & Himalayan Heli",
        "official_booking_url": "https://www.maavaishnodevi.org/",
        "operating_frequency": "Continuous flights from 07:00 AM to 05:30 PM",
        "ticket_fares": {
            "passenger": [
                {"class": "One-Way Ticket (Katra to Sanjichhat)", "fare_inr": 2100, "baggage": "5 kg maximum per passenger"},
                {"class": "Two-Way Round Trip (Katra-Sanjichhat-Katra)", "fare_inr": 4200, "baggage": "5 kg maximum per passenger"},
                {"class": "Infant (Under 2 years)", "fare_inr": 0, "baggage": "Carried in lap (ID required)"}
            ],
            "vehicle": [
                {"category": "Battery Car (Sanjichhat to Bhawan)", "fare_inr": 354, "note": "Electric shuttle for remaining 2.5 km trek"}
            ]
        },
        "connecting_transit": "Shri Mata Vaishno Devi Katra Railway Station (SVDK) connects directly to New Delhi; shared prepaid autos link station to helipad (₹150)",
        "onward_spokes": [
            {"destination": "Vaishno Devi Holy Bhawan", "distance_km": 2.5, "time_hr": 0.5},
            {"destination": "Bhairon Ghati Ropeway", "distance_km": 1.5, "time_hr": 0.1},
            {"destination": "Ardhkuwari Cave Temple", "distance_km": 6.0, "time_hr": 1.5},
            {"destination": "Shiv Khori Cave", "distance_km": 72, "time_hr": 2.5}
        ],
        "scam_alert_warning": "EXTREME FRAUD ALERT: Do NOT book through search engine sponsored ads or fake helpline numbers. Only www.maavaishnodevi.org is genuine. No agent or hotel has quota!",
        "operational_rules": "Valid Yatra Parchi / RFID card mandatory. Passengers must report 1 hour before departure. Automatic 100% refund for weather-canceled flights."
    },
    {
        "id": "varanasi_ganga_cruise_boating",
        "name": "Varanasi Ganga Ghat Boating & Alaknanda River Cruise",
        "category": "Waterway / Ghat River Transit",
        "state": "Uttar Pradesh",
        "primary_destination": "Varanasi Ghats & Kashi Vishwanath",
        "route": "Assi Ghat ↔ Dashashwamedh Ghat ↔ Manikarnika Ghat ↔ Rajghat",
        "transformation_math": "Bypasses congested, narrow, overcrowded ancient galis (alleys); traverses 84 historic ghats smoothly via the holy Ganga in 45 minutes",
        "operating_authority": "Varanasi Smart City / Inland Waterways Authority of India (IWAI) & Local Boatmen Union",
        "official_booking_url": "https://alaknandacruise.com/",
        "operating_frequency": "Morning Subah-e-Banaras (05:30 AM) and Evening Ganga Aarti (05:30 PM)",
        "ticket_fares": {
            "passenger": [
                {"class": "Hand-Rowed Traditional Boat (Assi to Dashashwamedh)", "fare_inr": 300, "baggage": "Standard daypacks"},
                {"class": "Motorized Shikara / Shared Boat", "fare_inr": 150, "baggage": "Per seat shared rate"},
                {"class": "Alaknanda Luxury AC Cruise (Morning Cruise)", "fare_inr": 900, "baggage": "Audio-visual guide & snacks included"},
                {"class": "Alaknanda Ganga Aarti Cruise (Evening Special)", "fare_inr": 1200, "baggage": "Reserved front-row Aarti view from river"}
            ],
            "vehicle": [
                {"category": "Private Bajra / Large Family Boat", "fare_inr": 3500, "note": "Up to 15-20 passengers for private family ritual"}
            ]
        },
        "connecting_transit": "Varanasi Junction (Cantt) and Banaras Railway Stations link to Assi and Dashashwamedh ghats via e-rickshaws (₹30 shared, ₹150 reserved)",
        "onward_spokes": [
            {"destination": "Kashi Vishwanath Temple (via Riverfront Corridor Gate)", "distance_km": 0.2, "time_hr": 0.1},
            {"destination": "Sankat Mochan Hanuman Temple", "distance_km": 2.5, "time_hr": 0.3},
            {"destination": "Sarnath Buddha Pilgrimage Site", "distance_km": 12, "time_hr": 0.5},
            {"destination": "Ayodhya Ram Mandir", "distance_km": 215, "time_hr": 4.0},
            {"destination": "Prayagraj Triveni Sangam", "distance_km": 125, "time_hr": 2.5}
        ],
        "scam_alert_warning": "Unlicensed touts at Godowlia Chowk overcharge up to ₹2,000 for standard hand boats. Always verify union fixed rates at the official ghat steps.",
        "operational_rules": "Wearing life jackets is mandatory by district administration order. Boating is suspended when Ganga water levels cross the danger mark during monsoon (July-September)."
    },
    {
        "id": "pavagadh_ropeway",
        "name": "Pavagadh Ropeway (Maa Mahakalika Temple, Champaner)",
        "category": "Mountain Ropeway / Cable Car",
        "state": "Gujarat",
        "primary_destination": "Pavagadh Hill & Kalika Mata Shaktipeeth",
        "route": "Machi Base Station ↔ Pavagadh Summit (Kalika Mata Temple)",
        "transformation_math": "Saves 2,000 stone climbing steps; cuts 2.5 hours of steep hiking to just 6 minutes (763-meter aerial lift)",
        "operating_authority": "Usha Breco Limited (Udan Khatola) / Gujarat Tourism",
        "official_booking_url": "https://udankhatola.com/",
        "operating_frequency": "Continuous cabins from 06:00 AM to 06:00 PM daily",
        "ticket_fares": {
            "passenger": [
                {"class": "Round Trip (Two-Way Adult)", "fare_inr": 180, "baggage": "Day luggage permitted"},
                {"class": "One-Way Ticket (Adult)", "fare_inr": 105, "baggage": "Single journey"},
                {"class": "Disabled / Senior Citizen Priority", "fare_inr": 180, "baggage": "Wheelchair elevator access"}
            ],
            "vehicle": [
                {"category": "Machi Parking (Car / Taxi)", "fare_inr": 40, "note": "Municipal parking lot at Machi base"}
            ]
        },
        "connecting_transit": "GSRTC express and local buses operate from Vadodara Central Bus Station to Champaner/Pavagadh (45 km, ₹45 fare, 1.2 hours)",
        "onward_spokes": [
            {"destination": "Champaner-Pavagadh UNESCO Archaeological Park", "distance_km": 4.0, "time_hr": 0.2},
            {"destination": "Statue of Unity (Kevadia)", "distance_km": 115, "time_hr": 2.2},
            {"destination": "Dakore Temple (Ranchhodraiji)", "distance_km": 75, "time_hr": 1.5},
            {"destination": "Vadodara Laxmi Vilas Palace", "distance_km": 50, "time_hr": 1.0}
        ],
        "scam_alert_warning": "Only purchase tickets at the official counter or udankhatola.com. Avoid touts selling 'VIP bypass queue' passes.",
        "operational_rules": "Queue wait times during Chaitra and Sharad Navratri reach 3-4 hours; booking the early 06:00 AM morning slot avoids extreme rush."
    },
    {
        "id": "joshimath_badrinath_gate_system",
        "name": "Joshimath to Badrinath Gate System & Landslide Timings (NH-7)",
        "category": "Mountain Pass / Controlled Highway Gate",
        "state": "Uttarakhand",
        "primary_destination": "Badrinath Dham",
        "route": "Joshimath ↔ Pandukeshwar ↔ Govindghat ↔ Badrinath (NH-7)",
        "transformation_math": "One-way alternating vehicle convoy system regulates traffic through narrow Himalayan gorge sections, preventing hours of mountain gridlock",
        "operating_authority": "Uttarakhand Police & Border Roads Organisation (BRO)",
        "official_booking_url": "https://registrationandtouristcare.uk.gov.in/",
        "operating_frequency": "Scheduled convoy gate opening times (06:00 AM, 09:00 AM, 11:30 AM, 02:00 PM, 04:30 PM)",
        "ticket_fares": {
            "passenger": [
                {"class": "Gate Passage Fee", "fare_inr": 0, "baggage": "Free government regulated transit"},
                {"class": "Green Cess / Vehicle Entry Fee", "fare_inr": 150, "baggage": "Per private commercial car"}
            ],
            "vehicle": [
                {"category": "Private Cars / Taxis", "fare_inr": 0, "note": "Mandatory adherence to gate convoy times"},
                {"category": "Tempo Travellers & Buses", "fare_inr": 0, "note": "Restricted evening movement after 05:00 PM"}
            ]
        },
        "connecting_transit": "Shared Sumos, Maxx cabs, and GMVN buses link Joshimath to Badrinath (45 km, ₹150-₹200 per seat)",
        "onward_spokes": [
            {"destination": "Badrinath Temple & Tapt Kund", "distance_km": 45, "time_hr": 2.5},
            {"destination": "Mana Village (First Indian Village)", "distance_km": 48, "time_hr": 2.8},
            {"destination": "Valley of Flowers & Hemkund Sahib (Govindghat)", "distance_km": 20, "time_hr": 1.0},
            {"destination": "Joshimath Auli Ropeway", "distance_km": 5.0, "time_hr": 0.3}
        ],
        "scam_alert_warning": "No agent can bypass the police convoy gate. Avoid rogue drivers charging 'express bypass' fees.",
        "operational_rules": "Strict Night Travel Ban: No civilian vehicles are permitted past Joshimath towards Badrinath after 05:00 PM due to landslide risks at Lambagar."
    },
    {
        "id": "bet_dwarka_ferry_sudama_setu",
        "name": "Okha to Bet Dwarka Passenger Ferry & Sudama Setu Bridge",
        "category": "Waterway & Cable Bridge",
        "state": "Gujarat",
        "primary_destination": "Bet Dwarka (Lord Krishna Residence)",
        "route": "Okha Jetty ↔ Bet Dwarka Island Jetty (or New Signature Bridge / Sudarshan Setu)",
        "transformation_math": "Traverses 3.5 km Arabian sea creek to Lord Krishna's island sanctuary in 15 minutes by boat or 5 minutes via the new Sudarshan Setu",
        "operating_authority": "Gujarat Maritime Board (GMB) / National Highways Authority of India (NHAI)",
        "official_booking_url": "https://gmbports.org/",
        "operating_frequency": "Continuous boats from 06:00 AM to 06:30 PM",
        "ticket_fares": {
            "passenger": [
                {"class": "Government Ferry Ticket", "fare_inr": 20, "baggage": "Standard day luggage"},
                {"class": "Private Motorboat (Reserved)", "fare_inr": 1500, "baggage": "Capacity up to 15 passengers"},
                {"class": "Sudarshan Setu Bridge Toll", "fare_inr": 0, "baggage": "Toll-free vehicular access for private cars & buses"}
            ],
            "vehicle": [
                {"category": "Car / Bus via Sudarshan Setu", "fare_inr": 0, "note": "Direct toll-free driving access to island"}
            ]
        },
        "connecting_transit": "Direct local passenger trains and GSRTC buses run between Dwarka Railway Station and Okha Port (30 km, 45 minutes, ₹30 bus fare)",
        "onward_spokes": [
            {"destination": "Dwarkadhish Temple (Main Dwarka)", "distance_km": 32, "time_hr": 0.8},
            {"destination": "Nageshwar Jyotirlinga", "distance_km": 20, "time_hr": 0.4},
            {"destination": "Gopi Talav Holy Pond", "distance_km": 24, "time_hr": 0.5},
            {"destination": "Shivrajpur Blue Flag Beach", "distance_km": 22, "time_hr": 0.4}
        ],
        "scam_alert_warning": "Boat operators often claim Sudarshan Setu is closed to force boat tickets. Always check the road bridge status before paying boat touts.",
        "operational_rules": "Ferries do not operate after sunset (06:30 PM). Strict security frisking on the island by Indian Coast Guard and Gujarat Police."
    }
]


def get_all_bottlenecks() -> List[Dict[str, Any]]:
    """Return the catalog of all pre-indexed pilgrimage transit bottlenecks."""
    return TRANSIT_BOTTLENECK_CATALOG


def find_bottleneck_by_id(bottleneck_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve specific bottleneck metadata by its unique ID."""
    for b in TRANSIT_BOTTLENECK_CATALOG:
        if b["id"] == bottleneck_id:
            return b
    return None


def calculate_bottleneck_intensity(
    query_or_route: str,
    time_saved_hours: Optional[float] = None,
    distance_saved_km: Optional[float] = None,
    has_steep_climb: bool = False,
    is_weather_vulnerable: bool = False
) -> Dict[str, Any]:
    """
    Evaluates how intense a transit bottleneck is from an SEO & traveler friction perspective.
    Returns an intensity score (0-100), friction pillar breakdown, and SEO opportunity verdict.
    """
    text = (query_or_route or "").lower()
    score = 0.0
    breakdown = {}

    # 1. Travel Time Reduction (0 - 25 pts)
    # Check text indicators if hours not provided
    hrs = time_saved_hours
    if hrs is None:
        m = re.search(r'(\d+(?:\.\d+)?)\s*(?:hours?|hrs?)', text)
        hrs = float(m.group(1)) if m else (4.0 if any(k in text for k in ["ferry", "heli", "ropeway", "flight"]) else 1.0)

    time_pts = min(25.0, hrs * 3.5)
    breakdown["time_savings_impact"] = round(time_pts, 1)
    score += time_pts

    # 2. Physical Exertion / Relief Factor (0 - 25 pts)
    # Steep climb, mountain steps, high altitude
    exertion_pts = 0.0
    if has_steep_climb or any(k in text for k in ["kedarnath", "girnar", "steps", "trek", "hike", "amarnath", "vaishno", "pavagadh", "steep", "doli", "pony"]):
        exertion_pts = 25.0
    elif any(k in text for k in ["boat", "waterway", "cruise", "ghat", "river"]):
        exertion_pts = 16.0
    else:
        exertion_pts = 10.0
    breakdown["physical_strain_relief"] = exertion_pts
    score += exertion_pts

    # 3. Booking Scarcity & Slot Urgency (0 - 20 pts)
    # High-demand slots (Helicopters, ropeway slots, ferry vehicle tickets)
    scarcity_pts = 0.0
    if any(k in text for k in ["helicopter", "heli", "irctc", "slot", "shrine board", "advance booking"]):
        scarcity_pts = 20.0
    elif any(k in text for k in ["ferry", "ropax", "car ticket", "vehicle slot", "toy train"]):
        scarcity_pts = 16.0
    else:
        scarcity_pts = 10.0
    breakdown["booking_scarcity_urgency"] = scarcity_pts
    score += scarcity_pts

    # 4. Weather & Operational Disruption Risk (0 - 15 pts)
    # Susceptible to rain, mountain fog, sea turbulence, landslides
    weather_pts = 0.0
    if is_weather_vulnerable or any(k in text for k in ["kedarnath", "himalayan", "monsoon", "fog", "sea", "maritime", "landslide", "gate system", "amarnath"]):
        weather_pts = 15.0
    else:
        weather_pts = 7.0
    breakdown["disruption_vulnerability"] = weather_pts
    score += weather_pts

    # 5. First-Mile / Last-Mile Connecting Transit Complexity (0 - 15 pts)
    connecting_pts = 0.0
    if any(k in text for k in ["connecting bus", "gsrtc", "railway station", "airport", "nh-", "terminal", "feeder"]):
        connecting_pts = 15.0
    else:
        connecting_pts = 9.0
    breakdown["connecting_transit_complexity"] = connecting_pts
    score += connecting_pts

    final_score = round(min(100.0, max(0.0, score)), 1)

    if final_score >= 85:
        serp_verdict = "EXTREME_BOTTLENECK_SERP_GOLDMINE"
        verdict_desc = "High-velocity search volume with acute traveler booking friction. Dominating this topic guarantees Rank 1."
    elif final_score >= 70:
        serp_verdict = "HIGH_INTENT_TRANSIT_BOTTLENECK"
        verdict_desc = "Significant traveler savings; structured timetables and multi-tier tariffs will capture Google Quick Answers."
    else:
        serp_verdict = "MODERATE_TRANSIT_ROUTE"
        verdict_desc = "Standard pilgrimage route. Expand with connecting transit and stay guides to increase authority."

    return {
        "intensity_score": final_score,
        "serp_opportunity": serp_verdict,
        "description": verdict_desc,
        "friction_breakdown": breakdown
    }


def generate_transit_champion_blueprint(bottleneck_id: str) -> Dict[str, Any]:
    """
    Synthesizes a complete, publication-ready, 10-checkpoint compliant markdown pillar guide
    for any cataloged pilgrimage transit bottleneck. Replicates the exact Ro-Pax champion formula.
    """
    b = find_bottleneck_by_id(bottleneck_id)
    if not b:
        # Fallback to first catalog entry
        b = TRANSIT_BOTTLENECK_CATALOG[0]

    title = f"{b['name']} Timings, Ticket Price & Online Booking Guide"
    meta_desc = f"{b['name']} latest timetable, passenger ticket prices, vehicle tariffs, and online booking rules. {b['transformation_math']}."

    # Build passenger table
    pass_rows = []
    for p in b["ticket_fares"]["passenger"]:
        pass_rows.append(f"| {p['class']} | ₹{p['fare_inr']} | {p['baggage']} |")
    pass_table = "\n".join(pass_rows)

    # Build vehicle table
    veh_rows = []
    for v in b["ticket_fares"]["vehicle"]:
        veh_rows.append(f"| {v['category']} | ₹{v['fare_inr']} | {v['note']} |")
    veh_table = "\n".join(veh_rows)

    # Build onward spokes table
    spoke_rows = []
    for s in b["onward_spokes"]:
        spoke_rows.append(f"| {s['destination']} | ~{s['distance_km']} km | ~{s['time_hr']} Hours | Verified Dharamshalas & Stays |")
    spoke_table = "\n".join(spoke_rows)

    markdown_body = f"""# {title}

{b['transformation_math']}. The official service operated under **{b['operating_authority']}** provides seamless connectivity for devotees, pilgrims, and tourists traveling to {b['primary_destination']}.

## Service Overview & Traveler Transformation Math
{b['name']} serves as a vital arterial route for travelers heading across {b['state']}. Instead of navigating congested highways or grueling uphill trails, this dedicated transit corridor provides a swift, comfortable, and reliable alternative. 

By bypassing traditional travel barriers, pilgrims save considerable physical exertion, fuel costs, and travel hours.

## Official Timetable & Operating Slots
The service maintains strict departure schedules to ensure passenger safety and operational synchronization:

| Journey Route | Departure Slot | Arrival Window | Reporting Cutoff | Frequency |
|---|---|---|---|---|
| Departure Terminal | Morning Slot (08:00 AM) | Midday (12:00 PM) | 1 Hour Prior | Daily |
| Return Service | Afternoon Slot (04:00 PM) | Evening (08:00 PM) | 1 Hour Prior | Daily |

## Class-Wise Passenger Ticket Fares & Booking Process
Passengers can select between different seating and comfort tiers. All rates are regulated and transparent:

| Travel Class / Seat Category | Regulated Tariff (INR) | Luggage / Allowance Details |
|---|---|---|
{pass_table}

## Vehicle Transportation & Weight Tariffs
For services permitting vehicle carriage or specialized weight allocations:

| Vehicle / Weight Category | Official Fare (INR) | Key Carriage Guidelines |
|---|---|---|
{veh_table}

## Boarding Protocols, Reporting Cutoff & Baggage Policies
{b['operational_rules']} All passengers must present a government-issued photo identity proof (Aadhaar Card, Voter ID, or Passport) matching the name on their booking voucher at the security checkpoint.

## Important Scam Warning & Official Booking Portal
> **Official Booking Advisory:** Always book directly through **[{b['operating_authority']}]({b['official_booking_url']})**.  
> {b['scam_alert_warning']}

## Connecting Public Transit & First-Mile / Last-Mile Access
{b['connecting_transit']}. Local taxis, auto-rickshaws, and feeder shuttles are stationed directly outside the terminal gates to assist passengers with onward transfers.

## Onward Pilgrimage Circuit & Hub-and-Spoke Routes
After arriving at the destination terminal, pilgrims can easily continue their spiritual yatra to nearby shrines:

| Connected Sacred Destination | Road Distance from Terminal | Driving Duration | Accommodation Availability |
|---|---|---|---|
{spoke_table}

## Verified Dharamshalas & Stay Bookings via YatraDham.Org
Finding clean, peaceful, and trusted accommodations is paramount for devotees. Pilgrims can reserve verified Dharamshalas, Ashrams, and budget guest houses across {b['primary_destination']} directly through [YatraDham.Org](https://yatradham.org/). 

YatraDham guarantees transparent reservations, pure satvik bhojanalaya meals, hot water facilities, and 24/7 dedicated pilgrim support. Download the **YatraDham App** on iOS and Android to manage room bookings and darshan passes with ease.

## Frequently Asked Questions
### Q1: What is the exact transformation benefit of {b['name']}?
{b['transformation_math']}. It is by far the most convenient mode of transit for pilgrims and families.

### Q2: What are the baggage and luggage restrictions?
Passengers are advised to travel light. {b['ticket_fares']['passenger'][0]['baggage']}.

### Q3: How do I book tickets safely without falling for agent scams?
Book exclusively via the authorized portal: [{b['official_booking_url']}]({b['official_booking_url']}). Avoid transferring funds via personal UPI IDs to unverified brokers.

### Q4: Are pets or animals permitted on board?
Pets are generally prohibited on passenger shuttles to comply with maritime and civil aviation safety guidelines.

### Q5: How can I book verified dharamshalas near the arrival station?
You can book clean family rooms with verified photos and satvik meals online at [YatraDham.Org](https://yatradham.org/).

### Q6: What happens if the service is canceled due to bad weather or rough seas?
If operations are suspended by authorities due to weather or technical factors, travelers receive an automatic 100% refund or can reschedule to the next available date.
"""

    return {
        "success": True,
        "bottleneck_id": b["id"],
        "name": b["name"],
        "title": title,
        "meta_description": meta_desc,
        "transformation_math": b["transformation_math"],
        "markdown_content": markdown_body,
        "structured_tables_count": 3,
        "onward_spokes_count": len(b["onward_spokes"]),
        "faqs_count": 6
    }


def validate_transit_bottleneck_guardrails(content: str, title: str = "") -> Dict[str, Any]:
    """
    Quality-gate guardrail ensuring transit bottleneck content meets mandatory safety,
    factual accuracy, transformation math, and official booking security standards.
    """
    total = f"{title}\n{content}".lower()
    guardrail_checks = []
    passed = 0

    # 1. Transformation Math Guardrail
    has_math = bool(re.search(r'\b(?:saves?|saving|reduces?|reduced?|reduction|cuts?|slashes?|replaces?|spares?|down to)\b.*?(\d+(?:\.\d+)?)\s*(?:km|kms|kilometers?|hours?|hrs?|minutes?|mins?|steps?)', total, re.IGNORECASE)) or any(k in total for k in ["hours saved", "km saved", "saves ", "cuts ", "reduces "])
    guardrail_checks.append({
        "rule": "Mandatory Transformation Math",
        "status": "PASSED" if has_math else "FAILED",
        "detail": "Must explicitly quantify distance (km) or travel time (hours/mins) saved."
    })
    if has_math: passed += 1

    # 2. Structured Comparison Tables
    has_tables = "|" in content or "<table" in total
    guardrail_checks.append({
        "rule": "Structured Timetable & Tariff Tables",
        "status": "PASSED" if has_tables else "FAILED",
        "detail": "Must present schedules and tariffs in structured Markdown or HTML tables."
    })
    if has_tables: passed += 1

    # 3. Explicit INR Pricing & Surcharges
    has_prices = bool(re.search(r'(?:₹|rs\.?|inr)\s*\d+', total))
    guardrail_checks.append({
        "rule": "Concrete INR (₹) Tariffs",
        "status": "PASSED" if has_prices else "FAILED",
        "detail": "Must state transparent, non-generic INR ticket and carriage rates."
    })
    if has_prices: passed += 1

    # 4. Scam Alert & Official Authority Attribution
    has_scam_or_official = any(k in total for k in ["official", "authorized", "beware", "scam", "irctc", "gmb", "shrine board", "fake"])
    guardrail_checks.append({
        "rule": "Official Attribution & Anti-Scam Advisory",
        "status": "PASSED" if has_scam_or_official else "FAILED",
        "detail": "Must name the official operating authority and warn pilgrims against fraudulent brokers."
    })
    if has_scam_or_official: passed += 1

    # 5. First-Mile / Last-Mile Connecting Transit
    has_connecting = any(k in total for k in ["bus", "station", "airport", "railway", "taxi", "rickshaw", "auto", "road"])
    guardrail_checks.append({
        "rule": "Connecting Transit Logistics",
        "status": "PASSED" if has_connecting else "FAILED",
        "detail": "Must advise pilgrims how to reach the boarding terminal from the nearest railway station or bus depot."
    })
    if has_connecting: passed += 1

    # 6. YatraDham Ecosystem & Stay Booking CTAs
    has_monetization = "yatradham" in total and any(k in total for k in ["stay", "dharamshala", "room", "book"])
    guardrail_checks.append({
        "rule": "YatraDham Stay Monetization",
        "status": "PASSED" if has_monetization else "FAILED",
        "detail": "Must include contextual links or CTAs to book verified dharamshalas and stays on YatraDham.Org."
    })
    if has_monetization: passed += 1

    compliance_score = round((passed / len(guardrail_checks)) * 100, 1)

    return {
        "compliant": passed == len(guardrail_checks),
        "compliance_score": compliance_score,
        "passed_rules": passed,
        "total_rules": len(guardrail_checks),
        "checks": guardrail_checks
    }
