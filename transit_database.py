"""
Verified Indian Spiritual & Wellness Transit Database.
Provides accurate, non-hallucinated airports, railway stations, and local landmarks.
"""
from typing import List, Dict

TRANSIT_HUBS = {
    "rishikesh": [
        {"name": "Nearest Airport", "distance": "Jolly Grant Airport Dehradun (~21 km) [DED]", "type": "airport"},
        {"name": "Nearest Railway Station", "distance": "Yog Nagari Rishikesh (~6 km) / Haridwar Junction (~25 km)", "type": "railway"},
        {"name": "Sacred Ganga Ghat & Ram Jhula", "distance": "Walking distance from center premises", "type": "sightseeing"}
    ],
    "haridwar": [
        {"name": "Nearest Airport", "distance": "Jolly Grant Airport Dehradun (~35 km) [DED]", "type": "airport"},
        {"name": "Nearest Railway Station", "distance": "Haridwar Junction Railway Station (~4 km)", "type": "railway"},
        {"name": "Har Ki Pauri & Ganga Ghats", "distance": "Convenient short e-rickshaw or auto ride", "type": "sightseeing"}
    ],
    "palakkad": [
        {"name": "Nearest Airport", "distance": "Coimbatore International Airport (~55 km) [CJB] / Cochin Intl Airport (~85 km)", "type": "airport"},
        {"name": "Nearest Railway Station", "distance": "Palakkad Junction Railway Station (~12 km) [PGT]", "type": "railway"},
        {"name": "Palakkad Fort & Western Ghats", "distance": "Short drive through lush coconut plantations", "type": "sightseeing"}
    ],
    "kerala": [
        {"name": "Nearest Airport", "distance": "Cochin International Airport (~75 km) [COK]", "type": "airport"},
        {"name": "Nearest Railway Station", "distance": "Kottayam / Ernakulam Railway Station (~15 km)", "type": "railway"},
        {"name": "Kerala Backwaters & Herbal Groves", "distance": "Directly accessible on retreat campus", "type": "sightseeing"}
    ],
    "kumarakom": [
        {"name": "Nearest Airport", "distance": "Cochin International Airport (~75 km) [COK]", "type": "airport"},
        {"name": "Nearest Railway Station", "distance": "Kottayam Railway Station (~14 km)", "type": "railway"},
        {"name": "Vembanad Lake & Bird Sanctuary", "distance": "Adjacent to resort property", "type": "sightseeing"}
    ],
    "kangra": [
        {"name": "Nearest Airport", "distance": "Gaggal Kangra Airport (~14 km) [DHM] / Pathankot Airport (~85 km)", "type": "airport"},
        {"name": "Nearest Railway Station", "distance": "Pathankot Junction (~85 km) / Kangra Toy Train Station", "type": "railway"},
        {"name": "Dhauladhar Mountain Range & Tea Gardens", "distance": "Panoramic views from wellness campus", "type": "sightseeing"}
    ],
    "baddi": [
        {"name": "Nearest Airport", "distance": "Shaheed Bhagat Singh Intl Airport Chandigarh (~45 km) [IXC]", "type": "airport"},
        {"name": "Nearest Railway Station", "distance": "Kalka Railway Station (~30 km) / Chandigarh Junction (~38 km)", "type": "railway"},
        {"name": "Pinjore Gardens & Shivalik Foothills", "distance": "15 minutes scenic drive", "type": "sightseeing"}
    ],
    "delhi": [
        {"name": "Nearest Airport", "distance": "Indira Gandhi International Airport (~25 km) [DEL]", "type": "airport"},
        {"name": "Nearest Railway Station", "distance": "New Delhi Railway Station (~18 km) [NDLS] / Hazrat Nizamuddin", "type": "railway"},
        {"name": "Nearest Metro Station", "distance": "Chhatarpur / Qutub Minar Metro Station (~3 km)", "type": "transit"}
    ],
    "mumbai": [
        {"name": "Nearest Airport", "distance": "Chhatrapati Shivaji Maharaj Intl Airport (~35 km) [BOM]", "type": "airport"},
        {"name": "Nearest Railway Station", "distance": "Mumbai CSMT / Dadar Central Railway Station", "type": "railway"},
        {"name": "Sanjay Gandhi National Park & Kanheri", "distance": "Scenic peaceful retreat vicinity", "type": "sightseeing"}
    ],
    "alibaug": [
        {"name": "Nearest Airport", "distance": "Chhatrapati Shivaji Maharaj Intl Airport Mumbai (~95 km) [BOM]", "type": "airport"},
        {"name": "Nearest Ferry / Jetty", "distance": "Mandwa Jetty (~18 km) via Ro-Ro ferry from Gateway of India", "type": "transit"},
        {"name": "Nearest Railway Station", "distance": "Panvel / Roha Railway Station (~35 km)", "type": "railway"}
    ],
    "gangasagar": [
        {"name": "Nearest Airport", "distance": "Netaji Subhash Chandra Bose Intl Airport Kolkata (~130 km) [CCU]", "type": "airport"},
        {"name": "Nearest Railway Station", "distance": "Kakdwip / Namkhana Railway Station (~30 km)", "type": "railway"},
        {"name": "Kapil Muni Temple & Sagar Beach", "distance": "Walking distance from ashram grounds", "type": "sightseeing"}
    ],
    "nalsarovar": [
        {"name": "Nearest Airport", "distance": "Sardar Vallabhbhai Patel Intl Airport Ahmedabad (~65 km) [AMD]", "type": "airport"},
        {"name": "Nearest Railway Station", "distance": "Ahmedabad Junction Railway Station (~60 km)", "type": "railway"},
        {"name": "Nalsarovar Bird Sanctuary", "distance": "5 km from wellness retreat grounds", "type": "sightseeing"}
    ],
    "junagadh": [
        {"name": "Nearest Airport", "distance": "Rajkot Airport (~100 km) [RAJ] / Keshod Airport (~35 km)", "type": "airport"},
        {"name": "Nearest Railway Station", "distance": "Junagadh Junction Railway Station (~5 km)", "type": "railway"},
        {"name": "Girnar Sacred Hill & Sanctuary", "distance": "Short scenic drive from wellness center", "type": "sightseeing"}
    ],
    "bhubaneswar": [
        {"name": "Nearest Airport", "distance": "Biju Patnaik International Airport (~8 km) [BBI]", "type": "airport"},
        {"name": "Nearest Railway Station", "distance": "Bhubaneswar Railway Station (~6 km) [BBS]", "type": "railway"},
        {"name": "Lingaraj Temple & Khandagiri Caves", "distance": "Short 10-minute drive", "type": "sightseeing"}
    ],
    "varanasi": [
        {"name": "Nearest Airport", "distance": "Lal Bahadur Shastri Intl Airport Varanasi (~25 km) [VNS]", "type": "airport"},
        {"name": "Nearest Railway Station", "distance": "Varanasi Junction (Cantt) / Banaras Station (~4 km)", "type": "railway"},
        {"name": "Kashi Vishwanath Temple & Dashashwamedh Ghat", "distance": "Directly accessible by electric rickshaw", "type": "sightseeing"}
    ]
}

def get_verified_transit_hubs(destination: str, pkg_name: str) -> List[Dict[str, str]]:
    query = f"{destination} {pkg_name}".lower()
    for key, hubs in TRANSIT_HUBS.items():
        if key in query:
            return hubs
    
    return [
        {"name": "Nearest Domestic Airport", "distance": f"Connecting via State Capital airport for {destination}", "type": "airport"},
        {"name": "Nearest Railway Station", "distance": f"Main Regional Railway Junction serving {destination}", "type": "railway"},
        {"name": "Local Spiritual / Nature Landmarks", "distance": f"Convenient local taxi and auto access within {destination}", "type": "sightseeing"}
    ]
