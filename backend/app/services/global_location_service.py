import time
import re
import unicodedata
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import httpx
from sqlalchemy.orm import Session
from app.models.destination import Country, RegionState, City, AttractionPOI, HotelStay, RestaurantVenue, TravelRequirement

logger = logging.getLogger(__name__)


def clean_ascii(text: Optional[str]) -> str:
    """Converts accents and unicode characters into clean standard ascii."""
    if not text:
        return ""
    normalized = unicodedata.normalize('NFKD', str(text))
    ascii_bytes = normalized.encode('ascii', 'ignore')
    res = ascii_bytes.decode('ascii').strip()
    return res if res else ""


# =====================================================================
# GLOBAL WORLD KNOWLEDGE REPOSITORY
# Covers all major world countries and top global cities with real
# coordinates, timezones, currencies, vibes, and top attractions.
# =====================================================================

WORLD_COUNTRIES_DATA = {
    "china": {
        "name": "China",
        "code": "CN",
        "continent": "Asia",
        "currency": "CNY",
        "timezone": "Asia/Shanghai",
        "latitude": 35.8617,
        "longitude": 104.1954,
        "capital": "Beijing",
        "vibe": "Ancient Dynasties, Futuristic Metropolises & The Great Wall",
        "best_months": "Apr - May, Sep - Oct",
        "budget_inr": 9500,
        "image_url": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=1200&auto=format&fit=crop&q=80",
        "visa_guidelines": "144-Hour Visa-Free Transit available for 54 countries; Tourist (L) Visa required for longer stays.",
        "top_cities": ["Beijing", "Shanghai", "Xi'an", "Chengdu", "Guilin", "Hong Kong"],
        "top_attractions": ["Great Wall of China", "Forbidden City", "Terracotta Army", "Summer Palace", "The Bund", "Zhangjiajie National Forest"]
    },
    "india": {
        "name": "India",
        "code": "IN",
        "continent": "Asia",
        "currency": "INR",
        "timezone": "Asia/Kolkata",
        "latitude": 20.5937,
        "longitude": 78.9629,
        "capital": "New Delhi",
        "vibe": "Royal Palaces, Vibrant Heritage, Spice Trails & Spiritual Havens",
        "best_months": "Oct - Mar",
        "budget_inr": 6500,
        "image_url": "https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=1200&auto=format&fit=crop&q=80",
        "visa_guidelines": "e-Tourist Visa available online for 165+ nationalities; fast 72-hour processing.",
        "top_cities": ["Jaipur", "Udaipur", "New Delhi", "Mumbai", "Goa", "Varanasi", "Agra", "Bengaluru"],
        "top_attractions": ["Amber Palace", "Taj Mahal", "Hawa Mahal", "City Palace Udaipur", "Gateway of India", "Qutub Minar"]
    },
    "japan": {
        "name": "Japan",
        "code": "JP",
        "continent": "Asia",
        "currency": "JPY",
        "timezone": "Asia/Tokyo",
        "latitude": 36.2048,
        "longitude": 138.2529,
        "capital": "Tokyo",
        "vibe": "Neon Metropolises, Ancient Shinto Shrines & Michelin Gastronomy",
        "best_months": "Mar - May, Oct - Nov",
        "budget_inr": 18500,
        "image_url": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=1200&auto=format&fit=crop&q=80",
        "visa_guidelines": "Visa exemption for 68 countries (up to 90 days); eVisa for eligible short-term tourists.",
        "top_cities": ["Tokyo", "Kyoto", "Osaka", "Sapporo", "Hiroshima", "Nara"],
        "top_attractions": ["Senso-ji Temple", "Mount Fuji", "Fushimi Inari Taisha", "Shibuya Crossing", "Kinkaku-ji", "Dotonbori"]
    },
    "france": {
        "name": "France",
        "code": "FR",
        "continent": "Europe",
        "currency": "EUR",
        "timezone": "Europe/Paris",
        "latitude": 46.2276,
        "longitude": 2.2137,
        "capital": "Paris",
        "vibe": "Haute Couture, Louvre Masterpieces, Wine Chateaux & Riviera Sunshine",
        "best_months": "Apr - Oct",
        "budget_inr": 22000,
        "image_url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1200&auto=format&fit=crop&q=80",
        "visa_guidelines": "Schengen Visa required for non-exempt countries (90 days in 180-day period).",
        "top_cities": ["Paris", "Nice", "Lyon", "Marseille", "Bordeaux", "Strasbourg"],
        "top_attractions": ["Eiffel Tower", "Louvre Museum", "Palace of Versailles", "Mont Saint-Michel", "Cote d'Azur", "Arc de Triomphe"]
    },
    "usa": {
        "name": "United States",
        "code": "US",
        "continent": "North America",
        "currency": "USD",
        "timezone": "America/New_York",
        "latitude": 37.0902,
        "longitude": -95.7129,
        "capital": "Washington D.C.",
        "vibe": "Iconic Skylines, National Parks, Broadway Lights & Pacific Coastlines",
        "best_months": "May - Oct",
        "budget_inr": 25000,
        "image_url": "https://images.unsplash.com/photo-1485738422979-f5c462d49f74?w=1200&auto=format&fit=crop&q=80",
        "visa_guidelines": "ESTA Visa Waiver for eligible VWP nations; B1/B2 Tourist Visa for others.",
        "top_cities": ["New York", "San Francisco", "Los Angeles", "Las Vegas", "Miami", "Chicago"],
        "top_attractions": ["Statue of Liberty", "Grand Canyon", "Times Square", "Golden Gate Bridge", "Yellowstone", "Central Park"]
    },
    "united kingdom": {
        "name": "United Kingdom",
        "code": "GB",
        "continent": "Europe",
        "currency": "GBP",
        "timezone": "Europe/London",
        "latitude": 55.3781,
        "longitude": -3.4360,
        "capital": "London",
        "vibe": "Royal Palaces, West End Theatres, Historic Castles & Country Pubs",
        "best_months": "May - Sep",
        "budget_inr": 23000,
        "image_url": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=1200&auto=format&fit=crop&q=80",
        "visa_guidelines": "Standard Visitor Visa (up to 6 months) or ETA for eligible passport holders.",
        "top_cities": ["London", "Edinburgh", "Manchester", "Bath", "Oxford", "Liverpool"],
        "top_attractions": ["Big Ben", "Tower of London", "British Museum", "Stonehenge", "Edinburgh Castle", "Buckingham Palace"]
    },
    "thailand": {
        "name": "Thailand",
        "code": "TH",
        "continent": "Asia",
        "currency": "THB",
        "timezone": "Asia/Bangkok",
        "latitude": 15.8700,
        "longitude": 100.9925,
        "capital": "Bangkok",
        "vibe": "Golden Temples, Bustling Night Markets, Street Food & Island Beaches",
        "best_months": "Nov - Apr",
        "budget_inr": 7000,
        "image_url": "https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=1200&auto=format&fit=crop&q=80",
        "visa_guidelines": "Visa exemption for 93 countries (up to 60 days); Visa on Arrival available.",
        "top_cities": ["Bangkok", "Phuket", "Chiang Mai", "Pattaya", "Koh Samui", "Krabi"],
        "top_attractions": ["Grand Palace", "Wat Arun", "Phi Phi Islands", "Chatuchak Market", "Wat Phra That Doi Suthep", "Railay Beach"]
    },
    "australia": {
        "name": "Australia",
        "code": "AU",
        "continent": "Oceania",
        "currency": "AUD",
        "timezone": "Australia/Sydney",
        "latitude": -25.2744,
        "longitude": 133.7751,
        "capital": "Canberra",
        "vibe": "Harbour Harbors, Great Barrier Reef, Outback Sunsets & Surfing Beaches",
        "best_months": "Sep - Nov, Mar - May",
        "budget_inr": 21000,
        "image_url": "https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?w=1200&auto=format&fit=crop&q=80",
        "visa_guidelines": "eVisitor / ETA online visa application required prior to departure.",
        "top_cities": ["Sydney", "Melbourne", "Brisbane", "Perth", "Cairns", "Gold Coast"],
        "top_attractions": ["Sydney Opera House", "Great Barrier Reef", "Sydney Harbour Bridge", "Bondi Beach", "Uluru", "Great Ocean Road"]
    },
    "canada": {
        "name": "Canada",
        "code": "CA",
        "continent": "North America",
        "currency": "CAD",
        "timezone": "America/Toronto",
        "latitude": 56.1304,
        "longitude": -106.3468,
        "capital": "Ottawa",
        "vibe": "Glacial Lakes, Rocky Mountains, Multicultural Cities & Autumn Foliage",
        "best_months": "Jun - Oct",
        "budget_inr": 20000,
        "image_url": "https://images.unsplash.com/photo-1503614472-8c93d56e92ce?w=1200&auto=format&fit=crop&q=80",
        "visa_guidelines": "eTA required for visa-exempt travelers arriving by air; Visitor Visa for others.",
        "top_cities": ["Toronto", "Vancouver", "Montreal", "Calgary", "Quebec City", "Banff"],
        "top_attractions": ["Banff National Park", "Niagara Falls", "CN Tower", "Stanley Park", "Old Quebec", "Lake Louise"]
    },
    "italy": {
        "name": "Italy",
        "code": "IT",
        "continent": "Europe",
        "currency": "EUR",
        "timezone": "Europe/Rome",
        "latitude": 41.8719,
        "longitude": 12.5674,
        "capital": "Rome",
        "vibe": "Renaissance Art, Colosseum Antiquities, Tuscan Hills & Coastal Glamour",
        "best_months": "Apr - Jun, Sep - Oct",
        "budget_inr": 21000,
        "image_url": "https://images.unsplash.com/photo-1516483638261-f4dbaf036963?w=1200&auto=format&fit=crop&q=80",
        "visa_guidelines": "Schengen Visa rules apply (up to 90 days).",
        "top_cities": ["Rome", "Florence", "Venice", "Milan", "Naples", "Amalfi Coast"],
        "top_attractions": ["Colosseum", "Vatican Museums", "Duomo di Firenze", "Canals of Venice", "Pantheon", "Leaning Tower of Pisa"]
    },
    "germany": {
        "name": "Germany",
        "code": "DE",
        "continent": "Europe",
        "currency": "EUR",
        "timezone": "Europe/Berlin",
        "latitude": 51.1657,
        "longitude": 10.4515,
        "capital": "Berlin",
        "vibe": "Bavarian Castles, High-Tech Metropolises, Historic Cathedrals & Beer Gardens",
        "best_months": "May - Oct",
        "budget_inr": 19000,
        "image_url": "https://images.unsplash.com/photo-1467269204594-9661b134dd2b?w=1200&auto=format&fit=crop&q=80",
        "visa_guidelines": "Schengen Visa rules apply.",
        "top_cities": ["Berlin", "Munich", "Frankfurt", "Hamburg", "Cologne", "Dresden"],
        "top_attractions": ["Brandenburg Gate", "Neuschwanstein Castle", "Cologne Cathedral", "Marienplatz", "Black Forest", "Reichstag Building"]
    },
    "singapore": {
        "name": "Singapore",
        "code": "SG",
        "continent": "Asia",
        "currency": "SGD",
        "timezone": "Asia/Singapore",
        "latitude": 1.3521,
        "longitude": 103.8198,
        "capital": "Singapore",
        "vibe": "Supertrees, Futuristic Skyline, Michelin Hawker Stalls & Luxury Shopping",
        "best_months": "Year-round",
        "budget_inr": 19000,
        "image_url": "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=1200&auto=format&fit=crop&q=80",
        "visa_guidelines": "Visa-free entry for up to 90 days for most passport holders; SG Arrival Card required.",
        "top_cities": ["Singapore"],
        "top_attractions": ["Gardens by the Bay", "Marina Bay Sands", "Sentosa Island", "Jewel Changi", "Universal Studios Singapore", "Chinatown"]
    },
    "malaysia": {
        "name": "Malaysia",
        "code": "MY",
        "continent": "Asia",
        "currency": "MYR",
        "timezone": "Asia/Kuala_Lumpur",
        "latitude": 4.2105,
        "longitude": 101.9758,
        "capital": "Kuala Lumpur",
        "vibe": "Petronas Twin Towers, Rainforest Biodiversity, Street Gastronomy & Island Resorts",
        "best_months": "Year-round",
        "budget_inr": 7500,
        "image_url": "https://images.unsplash.com/photo-1596422846543-75c6fc197f07?w=1200&auto=format&fit=crop&q=80",
        "visa_guidelines": "Visa-free for 30-90 days for most countries; MDAC digital arrival card required.",
        "top_cities": ["Kuala Lumpur", "Penang", "Langkawi", "Malacca", "Kota Kinabalu"],
        "top_attractions": ["Petronas Twin Towers", "Batu Caves", "Langkawi Sky Bridge", "George Town Heritage", "Mount Kinabalu"]
    },
    "spain": {
        "name": "Spain",
        "code": "ES",
        "continent": "Europe",
        "currency": "EUR",
        "timezone": "Europe/Madrid",
        "latitude": 40.4637,
        "longitude": -3.7492,
        "capital": "Madrid",
        "vibe": "Gaudi Masterpieces, Flamenco Rhythms, Tapas Culture & Mediterranean Sun",
        "best_months": "Apr - Jun, Sep - Oct",
        "budget_inr": 18000,
        "image_url": "https://images.unsplash.com/photo-1543783207-ec64e4d95325?w=1200&auto=format&fit=crop&q=80",
        "visa_guidelines": "Schengen Visa regulations apply.",
        "top_cities": ["Barcelona", "Madrid", "Seville", "Valencia", "Granada", "Ibiza"],
        "top_attractions": ["Sagrada Familia", "Park Guell", "Alhambra Palace", "Prado Museum", "Plaza de Espana", "La Rambla"]
    },
    "brazil": {
        "name": "Brazil",
        "code": "BR",
        "continent": "South America",
        "currency": "BRL",
        "timezone": "America/Sao_Paulo",
        "latitude": -14.2350,
        "longitude": -51.9253,
        "capital": "Brasilia",
        "vibe": "Copacabana Beaches, Christ the Redeemer, Amazon Rainforest & Samba Beats",
        "best_months": "Dec - Mar",
        "budget_inr": 12000,
        "image_url": "https://images.unsplash.com/photo-1483729558449-99ef09a8c325?w=1200&auto=format&fit=crop&q=80",
        "visa_guidelines": "eVisa available for US, Canada, Australia passport holders; visa-exempt for EU/UK.",
        "top_cities": ["Rio de Janeiro", "Sao Paulo", "Salvador", "Florianopolis", "Manaus"],
        "top_attractions": ["Christ the Redeemer", "Sugarloaf Mountain", "Copacabana Beach", "Iguazu Falls", "Amazon Rainforest"]
    },
    "south korea": {
        "name": "South Korea",
        "code": "KR",
        "continent": "Asia",
        "currency": "KRW",
        "timezone": "Asia/Seoul",
        "latitude": 35.9078,
        "longitude": 127.7669,
        "capital": "Seoul",
        "vibe": "K-Pop Culture, Joseon Royal Palaces, Street Food Alleys & High-Tech Hubs",
        "best_months": "Apr - Jun, Sep - Nov",
        "budget_inr": 16000,
        "image_url": "https://images.unsplash.com/photo-1538485399081-7191377e8241?w=1200&auto=format&fit=crop&q=80",
        "visa_guidelines": "K-ETA required for eligible visa-exempt travelers; Tourist Visa for others.",
        "top_cities": ["Seoul", "Busan", "Jeju Island", "Incheon", "Gyeongju"],
        "top_attractions": ["Gyeongbokgung Palace", "N Seoul Tower", "Bukchon Hanok Village", "Myeongdong Shopping", "Haeundae Beach"]
    },
    "egypt": {
        "name": "Egypt",
        "code": "EG",
        "continent": "Africa",
        "currency": "EGP",
        "timezone": "Africa/Cairo",
        "latitude": 26.8206,
        "longitude": 30.8025,
        "capital": "Cairo",
        "vibe": "Great Pyramids of Giza, Ancient Pharaoh Tombs, Nile River Cruises & Red Sea Diving",
        "best_months": "Oct - Apr",
        "budget_inr": 8000,
        "image_url": "https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=1200&auto=format&fit=crop&q=80",
        "visa_guidelines": "e-Visa and Visa on Arrival available for 74+ nationalities (30 days single entry).",
        "top_cities": ["Cairo", "Luxor", "Aswan", "Alexandria", "Sharm El Sheikh", "Hurghada"],
        "top_attractions": ["Pyramids of Giza", "Great Sphinx", "Valley of the Kings", "Karnak Temple", "Egyptian Museum", "Nile River Cruise"]
    },
    "turkey": {
        "name": "Turkey",
        "code": "TR",
        "continent": "Europe",
        "currency": "TRY",
        "timezone": "Europe/Istanbul",
        "latitude": 38.9637,
        "longitude": 35.2433,
        "capital": "Ankara",
        "vibe": "Bosphorus Straits, Cappadocia Hot Air Balloons, Byzantine Mosaics & Spice Bazaars",
        "best_months": "Apr - May, Sep - Nov",
        "budget_inr": 11000,
        "image_url": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=1200&auto=format&fit=crop&q=80",
        "visa_guidelines": "e-Visa available online for eligible travelers in minutes; visa-exempt for many.",
        "top_cities": ["Istanbul", "Antalya", "Cappadocia", "Izmir", "Bodrum", "Ankara"],
        "top_attractions": ["Hagia Sophia", "Blue Mosque", "Cappadocia Balloons", "Topkapi Palace", "Pamukkale Terraces", "Grand Bazaar"]
    },
    "nepal": {
        "name": "Nepal",
        "code": "NP",
        "continent": "Asia",
        "currency": "NPR",
        "timezone": "Asia/Kathmandu",
        "latitude": 28.3949,
        "longitude": 84.1240,
        "capital": "Kathmandu",
        "vibe": "Himalayan Peaks, Mount Everest Expeditions, Ancient Pagodas & Peace Stupas",
        "best_months": "Oct - Nov, Mar - Apr",
        "budget_inr": 5500,
        "image_url": "https://images.unsplash.com/photo-1544735716-392fe2489ffa?w=1200&auto=format&fit=crop&q=80",
        "visa_guidelines": "Visa on Arrival available at Tribhuvan International Airport (Kathmandu); Indian citizens exempt.",
        "top_cities": ["Kathmandu", "Pokhara", "Lalitpur", "Chitwan", "Bhaktapur"],
        "top_attractions": ["Boudhanath Stupa", "Swayambhunath Monkey Temple", "Pashupatinath Temple", "Phewa Lake", "Annapurna Circuit", "Kathmandu Durbar Square"]
    },
    "bhutan": {
        "name": "Bhutan",
        "code": "BT",
        "continent": "Asia",
        "currency": "BTN",
        "timezone": "Asia/Thimphu",
        "latitude": 27.5142,
        "longitude": 90.4336,
        "capital": "Thimphu",
        "vibe": "Gross National Happiness, Cliffside Monasteries, Pine Valleys & Dzongs",
        "best_months": "Mar - May, Sep - Nov",
        "budget_inr": 16000,
        "image_url": "https://images.unsplash.com/photo-1584551246679-0daf3d275d0f?w=1200&auto=format&fit=crop&q=80",
        "visa_guidelines": "Visa or permit required with Sustainable Development Fee (SDF); special rates for SAARC citizens.",
        "top_cities": ["Thimphu", "Paro", "Punakha", "Phuentsholing"],
        "top_attractions": ["Tiger's Nest Monastery (Paro Taktsang)", "Punakha Dzong", "Buddha Dordenma", "Dochula Pass", "Rinpung Dzong"]
    },
    "maldives": {
        "name": "Maldives",
        "code": "MV",
        "continent": "Asia",
        "currency": "MVR",
        "timezone": "Indian/Maldives",
        "latitude": 3.2028,
        "longitude": 73.2207,
        "capital": "Male",
        "vibe": "Overwater Luxury Villas, Turquoise Lagoons, Coral Reefs & Manta Ray Dives",
        "best_months": "Nov - Apr",
        "budget_inr": 28000,
        "image_url": "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?w=1200&auto=format&fit=crop&q=80",
        "visa_guidelines": "Free 30-day Visa on Arrival for all tourists with confirmed resort booking & return ticket.",
        "top_cities": ["Male", "Maafushi", "Hulhumale", "Ari Atoll", "Baa Atoll"],
        "top_attractions": ["Banana Reef", "Grand Friday Mosque", "Maafushi Island", "Male Local Market", "Baa Atoll Biosphere Reserve"]
    },
    "united arab emirates": {
        "name": "United Arab Emirates",
        "code": "AE",
        "continent": "Middle East",
        "currency": "AED",
        "timezone": "Asia/Dubai",
        "latitude": 23.4241,
        "longitude": 53.8478,
        "capital": "Abu Dhabi",
        "vibe": "Burj Khalifa Skyscraper, Luxury Dune Safaris, Mega Malls & Marina Cruises",
        "best_months": "Nov - Mar",
        "budget_inr": 22000,
        "image_url": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=1200&auto=format&fit=crop&q=80",
        "visa_guidelines": "Visa on arrival for 70+ countries; 30/60-day tourist visas available online.",
        "top_cities": ["Dubai", "Abu Dhabi", "Sharjah", "Ras Al Khaimah"],
        "top_attractions": ["Burj Khalifa", "Sheikh Zayed Grand Mosque", "Dubai Mall", "Palm Jumeirah", "Louvre Abu Dhabi"]
    },
    "indonesia": {
        "name": "Indonesia",
        "code": "ID",
        "continent": "Asia",
        "currency": "IDR",
        "timezone": "Asia/Jakarta",
        "latitude": -0.7893,
        "longitude": 113.9213,
        "capital": "Jakarta",
        "vibe": "Tropical Beach Villas, Volcanic Sunrises, Balinese Temples & Coral Atolls",
        "best_months": "May - Sep",
        "budget_inr": 8500,
        "image_url": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=1200&auto=format&fit=crop&q=80",
        "visa_guidelines": "Electronic Visa on Arrival (e-VOA) available for 90+ nationalities (30 days).",
        "top_cities": ["Bali", "Jakarta", "Yogyakarta", "Lombok", "Komodo"],
        "top_attractions": ["Uluwatu Temple", "Borobudur", "Mount Bromo", "Tegallalang Rice Terraces", "Komodo National Park"]
    },
    "switzerland": {
        "name": "Switzerland",
        "code": "CH",
        "continent": "Europe",
        "currency": "CHF",
        "timezone": "Europe/Zurich",
        "latitude": 46.8182,
        "longitude": 8.2275,
        "capital": "Bern",
        "vibe": "Glacial Alpine Peaks, Scenic Panoramic Trains, Crystal Lakes & Fondue Chalets",
        "best_months": "Dec - Mar (Ski), Jun - Sep (Hiking)",
        "budget_inr": 29000,
        "image_url": "https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?w=1200&auto=format&fit=crop&q=80",
        "visa_guidelines": "Schengen Visa required for non-exempt travelers.",
        "top_cities": ["Interlaken", "Zurich", "Geneva", "Lucerne", "Zermatt"],
        "top_attractions": ["Jungfraujoch Top of Europe", "Matterhorn", "Lake Geneva", "Chapel Bridge", "Grindelwald First"]
    }
}

# Alias map for quick lookup
COUNTRY_ALIASES = {
    "us": "usa",
    "united states of america": "usa",
    "united states": "usa",
    "uk": "united kingdom",
    "great britain": "united kingdom",
    "england": "united kingdom",
    "scotland": "united kingdom",
    "uae": "united arab emirates",
    "emirates": "united arab emirates",
    "korea": "south korea",
    "republic of korea": "south korea",
}

# =====================================================================
# GLOBAL WORLD CITIES REPOSITORY
# Fast lookup for top global metropolises with real coordinates
# =====================================================================

WORLD_CITIES_DATA = {
    "beijing": {
        "name": "Beijing",
        "country": "China",
        "country_code": "CN",
        "continent": "Asia",
        "region": "Beijing Municipality",
        "latitude": 39.9042,
        "longitude": 116.4074,
        "vibe": "Imperial Palaces, Forbidden City Treasures, Peking Duck & Hutong Culture",
        "best_months": "Sep - Nov, Apr - May",
        "budget_inr": 8500,
        "image_url": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=1200&auto=format&fit=crop&q=80",
        "attractions": [
            {"name": "The Forbidden City", "category": "Imperial Palace", "duration_minutes": 240, "entry_fee_inr": 700, "indoor_outdoor": "Both", "description": "The monumental imperial palace complex of the Ming and Qing dynasties with 980 surviving buildings."},
            {"name": "Mutianyu Great Wall", "category": "World Wonder", "duration_minutes": 300, "entry_fee_inr": 850, "indoor_outdoor": "Outdoor", "description": "Magnificent restored section of the Great Wall winding across rolling forested mountain ridges."},
            {"name": "Summer Palace & Kunming Lake", "category": "Royal Garden", "duration_minutes": 180, "entry_fee_inr": 450, "indoor_outdoor": "Outdoor", "description": "Masterpiece of Chinese garden design integrating hills, open waters, and ornate pavilions."},
            {"name": "Temple of Heaven", "category": "Sacred Architecture", "duration_minutes": 120, "entry_fee_inr": 400, "indoor_outdoor": "Both", "description": "Imperial sacrificial altar complex where emperors prayed for annual bountiful harvests."}
        ]
    },
    "shanghai": {
        "name": "Shanghai",
        "country": "China",
        "country_code": "CN",
        "continent": "Asia",
        "region": "East China",
        "latitude": 31.2304,
        "longitude": 121.4737,
        "vibe": "Futuristic Pudong Skyline, Historic Bund Architecture & Modern Art",
        "best_months": "Oct - Nov, Mar - May",
        "budget_inr": 9500,
        "image_url": "https://images.unsplash.com/photo-1548919973-5cef591cdbc9?w=1200&auto=format&fit=crop&q=80",
        "attractions": [
            {"name": "The Bund (Waitan)", "category": "Waterfront Promenade", "duration_minutes": 120, "entry_fee_inr": 0, "indoor_outdoor": "Outdoor", "description": "Historic colonial waterfront facing the iconic neon-lit Pudong skyscraper skyline."},
            {"name": "Shanghai Tower & Observation Deck", "category": "Skyscraper Viewpoint", "duration_minutes": 90, "entry_fee_inr": 2100, "indoor_outdoor": "Indoor", "description": "World's third-tallest building offering panoramic views from 562 meters high."},
            {"name": "Yu Garden & Bazaar", "category": "Classical Garden", "duration_minutes": 120, "entry_fee_inr": 500, "indoor_outdoor": "Both", "description": "Extensive Ming dynasty garden with koi ponds, rockeries, and tea houses."}
        ]
    },
    "london": {
        "name": "London",
        "country": "United Kingdom",
        "country_code": "GB",
        "continent": "Europe",
        "region": "Greater London",
        "latitude": 51.5074,
        "longitude": -0.1278,
        "vibe": "West End Theatres, Historic Royal Castles, Thames Cruises & Red Buses",
        "best_months": "May - Sep",
        "budget_inr": 23000,
        "image_url": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=1200&auto=format&fit=crop&q=80",
        "attractions": [
            {"name": "The British Museum", "category": "Museum & History", "duration_minutes": 180, "entry_fee_inr": 0, "indoor_outdoor": "Indoor", "description": "World-famous dedicated collection of human history, art, and the Rosetta Stone."},
            {"name": "Tower of London & Crown Jewels", "category": "Royal Fortress", "duration_minutes": 180, "entry_fee_inr": 3500, "indoor_outdoor": "Both", "description": "Nearly 1,000-year-old historic castle and home to the priceless Crown Jewels."},
            {"name": "Big Ben & Palace of Westminster", "category": "Historic Landmark", "duration_minutes": 60, "entry_fee_inr": 0, "indoor_outdoor": "Outdoor", "description": "The quintessential gothic clock tower and UK parliamentary seat on the River Thames."}
        ]
    },
    "new york": {
        "name": "New York",
        "country": "United States",
        "country_code": "US",
        "continent": "North America",
        "region": "New York State",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "vibe": "Broadway Theatres, Central Park, Iconic Skylines & 24/7 Street Life",
        "best_months": "Apr - Jun, Sep - Nov",
        "budget_inr": 26000,
        "image_url": "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=1200&auto=format&fit=crop&q=80",
        "attractions": [
            {"name": "Statue of Liberty & Ellis Island", "category": "National Monument", "duration_minutes": 240, "entry_fee_inr": 2200, "indoor_outdoor": "Both", "description": "Colossal neoclassical sculpture on Liberty Island in New York Harbor."},
            {"name": "Central Park", "category": "Urban Park", "duration_minutes": 180, "entry_fee_inr": 0, "indoor_outdoor": "Outdoor", "description": "843-acre lush urban oasis featuring lakes, walking trails, and bridges."},
            {"name": "Empire State Building & Summit One", "category": "Skyscraper Viewpoint", "duration_minutes": 90, "entry_fee_inr": 3800, "indoor_outdoor": "Indoor", "description": "Legendary art deco skyscraper providing 360-degree views of Manhattan."}
        ]
    },
    "bangkok": {
        "name": "Bangkok",
        "country": "Thailand",
        "country_code": "TH",
        "continent": "Asia",
        "region": "Central Thailand",
        "latitude": 13.7563,
        "longitude": 100.5018,
        "vibe": "Ornate Royal Temples, Chao Phraya Ferries & Michelin Street Stalls",
        "best_months": "Nov - Feb",
        "budget_inr": 6500,
        "image_url": "https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=1200&auto=format&fit=crop&q=80",
        "attractions": [
            {"name": "The Grand Palace & Wat Phra Kaew", "category": "Royal Temple", "duration_minutes": 180, "entry_fee_inr": 1200, "indoor_outdoor": "Both", "description": "Splendid complex of official royal residences housing the sacred Emerald Buddha."},
            {"name": "Wat Arun (Temple of Dawn)", "category": "Buddhist Temple", "duration_minutes": 90, "entry_fee_inr": 250, "indoor_outdoor": "Outdoor", "description": "Porcelain-encrusted spire towering over the Chao Phraya River bank."},
            {"name": "Chatuchak Weekend Market", "category": "Bazaar & Food", "duration_minutes": 240, "entry_fee_inr": 0, "indoor_outdoor": "Both", "description": "One of the world's largest open-air markets with over 15,000 distinct stalls."}
        ]
    },
    "sydney": {
        "name": "Sydney",
        "country": "Australia",
        "country_code": "AU",
        "continent": "Oceania",
        "region": "New South Wales",
        "latitude": -33.8688,
        "longitude": 151.2093,
        "vibe": "Iconic Opera House Sails, Bondi Surfing, Coastal Walks & Harbour Cruises",
        "best_months": "Sep - Nov, Mar - May",
        "budget_inr": 21000,
        "image_url": "https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?w=1200&auto=format&fit=crop&q=80",
        "attractions": [
            {"name": "Sydney Opera House", "category": "Architectural Icon", "duration_minutes": 120, "entry_fee_inr": 2800, "indoor_outdoor": "Both", "description": "World Heritage-listed performing arts center famous for its shell-like design."},
            {"name": "Bondi to Coogee Coastal Walk", "category": "Scenic Trail", "duration_minutes": 180, "entry_fee_inr": 0, "indoor_outdoor": "Outdoor", "description": "Breathtaking 6km coastal cliff walk passing beaches, ocean pools, and bays."},
            {"name": "Sydney Harbour Bridge Climb", "category": "Adventure Viewpoint", "duration_minutes": 180, "entry_fee_inr": 16000, "indoor_outdoor": "Outdoor", "description": "Guided summit climb offering panoramic views 134 meters above the harbor."}
        ]
    },
    "rome": {
        "name": "Rome",
        "country": "Italy",
        "country_code": "IT",
        "continent": "Europe",
        "region": "Lazio",
        "latitude": 41.9028,
        "longitude": 12.4964,
        "vibe": "Ancient Roman Ruins, Vatican Sistine Chapel & Authentic Trastevere Pasta",
        "best_months": "Apr - Jun, Sep - Oct",
        "budget_inr": 21000,
        "image_url": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=1200&auto=format&fit=crop&q=80",
        "attractions": [
            {"name": "The Colosseum & Roman Forum", "category": "Ancient Monument", "duration_minutes": 240, "entry_fee_inr": 1800, "indoor_outdoor": "Outdoor", "description": "Largest ancient amphitheater built under the Flavian emperors in 80 AD."},
            {"name": "Vatican Museums & Sistine Chapel", "category": "Art & Religion", "duration_minutes": 210, "entry_fee_inr": 2500, "indoor_outdoor": "Indoor", "description": "Immense papal art collection capped by Michelangelo's famous ceiling frescoes."},
            {"name": "Trevi Fountain & Spanish Steps", "category": "Baroque Landmark", "duration_minutes": 60, "entry_fee_inr": 0, "indoor_outdoor": "Outdoor", "description": "Magnificent baroque fountain and lively historic gathering place."}
        ]
    },
    "barcelona": {
        "name": "Barcelona",
        "country": "Spain",
        "country_code": "ES",
        "continent": "Europe",
        "region": "Catalonia",
        "latitude": 41.3879,
        "longitude": 2.1699,
        "vibe": "Gaudi Masterpieces, Gothic Quarter Tapas, Barceloneta Beaches & Sun",
        "best_months": "May - Jun, Sep - Oct",
        "budget_inr": 18000,
        "image_url": "https://images.unsplash.com/photo-1583422409516-2895a77efded?w=1200&auto=format&fit=crop&q=80",
        "attractions": [
            {"name": "Basilica de la Sagrada Familia", "category": "Architectural Marvel", "duration_minutes": 150, "entry_fee_inr": 2600, "indoor_outdoor": "Both", "description": "Antoni Gaudi's soaring unfinished basilica with nature-inspired stained-glass vaults."},
            {"name": "Park Guell", "category": "Mosaic Garden", "duration_minutes": 120, "entry_fee_inr": 1200, "indoor_outdoor": "Outdoor", "description": "Whimsical hilltop public park featuring serpentine mosaic benches."},
            {"name": "Gothic Quarter (Barri Gotic)", "category": "Historic District", "duration_minutes": 180, "entry_fee_inr": 0, "indoor_outdoor": "Outdoor", "description": "Atmospheric labyrinth of narrow medieval streets lined with tapas bars."}
        ]
    },
    "istanbul": {
        "name": "Istanbul",
        "country": "Turkey",
        "country_code": "TR",
        "continent": "Europe",
        "region": "Marmara",
        "latitude": 41.0082,
        "longitude": 28.9784,
        "vibe": "Crossroads of Continents, Byzantine Domes, Ottoman Palaces & Spice Bazaars",
        "best_months": "Apr - May, Sep - Nov",
        "budget_inr": 11000,
        "image_url": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=1200&auto=format&fit=crop&q=80",
        "attractions": [
            {"name": "Hagia Sophia (Ayasofya)", "category": "Historic Monument", "duration_minutes": 90, "entry_fee_inr": 2200, "indoor_outdoor": "Indoor", "description": "Magnificent 6th-century cathedral turned mosque featuring soaring golden domes."},
            {"name": "Topkapi Palace Museum", "category": "Ottoman Palace", "duration_minutes": 180, "entry_fee_inr": 3500, "indoor_outdoor": "Both", "description": "Imperial residence of Ottoman sultans for four centuries with scenic Bosphorus views."},
            {"name": "Grand Bazaar (Kapalicarsi)", "category": "Historic Market", "duration_minutes": 180, "entry_fee_inr": 0, "indoor_outdoor": "Indoor", "description": "One of the oldest covered markets in the world with 4,000 shops."}
        ]
    },
    "cairo": {
        "name": "Cairo",
        "country": "Egypt",
        "country_code": "EG",
        "continent": "Africa",
        "region": "Greater Cairo",
        "latitude": 30.0444,
        "longitude": 31.2357,
        "vibe": "Great Pyramids of Giza, Ancient Pharaoh Treasures, Nile Feluccas & Khan el-Khalili",
        "best_months": "Oct - Apr",
        "budget_inr": 8000,
        "image_url": "https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=1200&auto=format&fit=crop&q=80",
        "attractions": [
            {"name": "Pyramids of Giza & The Great Sphinx", "category": "Ancient Wonder", "duration_minutes": 240, "entry_fee_inr": 1500, "indoor_outdoor": "Outdoor", "description": "Sole surviving ancient wonder of the world including Khufu, Khafre, and Menkaure."},
            {"name": "The Grand Egyptian Museum", "category": "Museum & Antiquities", "duration_minutes": 210, "entry_fee_inr": 2200, "indoor_outdoor": "Indoor", "description": "World-class modern museum complex housing King Tutankhamun's complete treasures."},
            {"name": "Khan el-Khalili Bazaar", "category": "Historic Souk", "duration_minutes": 150, "entry_fee_inr": 0, "indoor_outdoor": "Outdoor", "description": "Lively 14th-century marketplace filled with spices, brass lamps, and coffee houses."}
        ]
    },
    "seoul": {
        "name": "Seoul",
        "country": "South Korea",
        "country_code": "KR",
        "continent": "Asia",
        "region": "Seoul Capital Area",
        "latitude": 37.5665,
        "longitude": 126.9780,
        "vibe": "K-Wave Hub, Joseon Royal Palaces, Cyberpunk Skylines & Korean BBQ",
        "best_months": "Apr - Jun, Sep - Nov",
        "budget_inr": 16000,
        "image_url": "https://images.unsplash.com/photo-1538485399081-7191377e8241?w=1200&auto=format&fit=crop&q=80",
        "attractions": [
            {"name": "Gyeongbokgung Palace", "category": "Royal Palace", "duration_minutes": 150, "entry_fee_inr": 200, "indoor_outdoor": "Both", "description": "Main royal palace of the Joseon Dynasty featuring changing of the royal guard ceremonies."},
            {"name": "N Seoul Tower & Namsan Mountain", "category": "Scenic Viewpoint", "duration_minutes": 120, "entry_fee_inr": 1100, "indoor_outdoor": "Both", "description": "Iconic observation tower offering 360-degree views across the Seoul metropolis."},
            {"name": "Bukchon Hanok Village", "category": "Traditional Quarter", "duration_minutes": 120, "entry_fee_inr": 0, "indoor_outdoor": "Outdoor", "description": "Historic residential neighborhood with hundreds of traditional Korean wooden homes."}
        ]
    },
    "kathmandu": {
        "name": "Kathmandu",
        "country": "Nepal",
        "country_code": "NP",
        "continent": "Asia",
        "region": "Kathmandu Valley",
        "latitude": 27.7172,
        "longitude": 85.3240,
        "vibe": "Himalayan Gateway, Ancient Buddhist Stupas, Hindu Shrines & Thamel Crafts",
        "best_months": "Oct - Nov, Mar - Apr",
        "budget_inr": 5500,
        "image_url": "https://images.unsplash.com/photo-1544735716-392fe2489ffa?w=1200&auto=format&fit=crop&q=80",
        "attractions": [
            {"name": "Boudhanath Stupa", "category": "Buddhist Stupa", "duration_minutes": 90, "entry_fee_inr": 250, "indoor_outdoor": "Outdoor", "description": "One of the largest spherical stupas in the world and center of Tibetan Buddhism in Nepal."},
            {"name": "Pashupatinath Temple", "category": "Sacred Hindu Temple", "duration_minutes": 120, "entry_fee_inr": 600, "indoor_outdoor": "Outdoor", "description": "UNESCO World Heritage Hindu temple complex situated on the banks of the Bagmati River."},
            {"name": "Swayambhunath (Monkey Temple)", "category": "Ancient Shrine", "duration_minutes": 120, "entry_fee_inr": 150, "indoor_outdoor": "Outdoor", "description": "Ancient hilltop religious architecture offering panoramic views across Kathmandu Valley."}
        ]
    },
    "male": {
        "name": "Male",
        "country": "Maldives",
        "country_code": "MV",
        "continent": "Asia",
        "region": "Kaafu Atoll",
        "latitude": 4.1755,
        "longitude": 73.5093,
        "vibe": "Turquoise Ocean Gateways, Island Ferries, Coral Architecture & Fresh Seafood",
        "best_months": "Nov - Apr",
        "budget_inr": 22000,
        "image_url": "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?w=1200&auto=format&fit=crop&q=80",
        "attractions": [
            {"name": "Grand Friday Mosque & Islamic Centre", "category": "Architecture & Heritage", "duration_minutes": 60, "entry_fee_inr": 0, "indoor_outdoor": "Indoor", "description": "Prominent landmark featuring golden dome and intricate coral stone carvings."},
            {"name": "Male Fish Market & Local Produce Souk", "category": "Cultural Market", "duration_minutes": 60, "entry_fee_inr": 0, "indoor_outdoor": "Both", "description": "Vibrant daily seafood and tropical fruit hub beside the harbor."},
            {"name": "Hulhumale Beach Lagoon", "category": "Lagoon & Water Sports", "duration_minutes": 180, "entry_fee_inr": 0, "indoor_outdoor": "Outdoor", "description": "Calm crystal turquoise waters perfect for snorkeling, paddle boarding, and boat departures."}
        ]
    }
}


# =====================================================================
# LOCATION PROVIDER ABSTRACTION
# =====================================================================

class LocationProvider(ABC):
    @abstractmethod
    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def autocomplete(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def resolve(self, identifier: str) -> Optional[Dict[str, Any]]:
        pass


# =====================================================================
# 1. LOCAL DATABASE PROVIDER
# =====================================================================

class LocalDatabaseProvider(LocationProvider):
    def __init__(self, db: Session):
        self.db = db

    def autocomplete(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        search_str = query.strip().lower()
        results = []

        # Matching Cities in DB
        cities = self.db.query(City).filter(City.name.ilike(f"%{search_str}%")).limit(limit).all()
        for city in cities:
            region_name = city.region.name if city.region else ""
            country_name = city.region.country.name if city.region and city.region.country else "India"
            country_code = city.region.country.code if city.region and city.region.country else "IN"
            
            canonical_val = f"{city.name}, {region_name}, {country_name}".replace(" ,", "").strip(", ")
            results.append({
                "id": city.id,
                "type": "city",
                "title": clean_ascii(city.name),
                "region": clean_ascii(region_name),
                "country": clean_ascii(country_name),
                "country_code": country_code,
                "subtitle": clean_ascii(f"{region_name}, {country_name}".strip(", ")),
                "canonical_value": clean_ascii(canonical_val),
                "canonical_id": f"city:{city.id}",
                "city_id": city.id,
                "latitude": city.latitude,
                "longitude": city.longitude,
                "image_url": city.image_url,
                "vibe": city.vibe,
                "avg_daily_budget_inr": city.avg_daily_budget_inr,
                "source": "local"
            })

        # Matching Countries in DB
        countries = self.db.query(Country).filter(
            Country.name.ilike(f"%{search_str}%") | Country.code.ilike(search_str)
        ).limit(4).all()
        for c in countries:
            results.append({
                "id": c.id,
                "type": "country",
                "title": clean_ascii(c.name),
                "region": clean_ascii(c.continent),
                "country": clean_ascii(c.name),
                "country_code": c.code,
                "subtitle": f"Country • {clean_ascii(c.continent)}",
                "canonical_value": clean_ascii(c.name),
                "canonical_id": f"country:{c.name.lower()}:{c.code.lower()}",
                "latitude": None,
                "longitude": None,
                "image_url": c.hero_image,
                "vibe": "Country Destination",
                "avg_daily_budget_inr": 8000,
                "source": "local"
            })

        # Matching Attractions in DB
        pois = self.db.query(AttractionPOI).filter(AttractionPOI.name.ilike(f"%{search_str}%")).limit(4).all()
        for poi in pois:
            city_name = poi.city.name if poi.city else ""
            country_name = poi.city.region.country.name if poi.city and poi.city.region and poi.city.region.country else "India"
            country_code = poi.city.region.country.code if poi.city and poi.city.region and poi.city.region.country else "IN"
            results.append({
                "id": poi.id,
                "type": "attraction",
                "title": clean_ascii(poi.name),
                "region": clean_ascii(poi.city.region.name if poi.city and poi.city.region else ""),
                "country": clean_ascii(country_name),
                "country_code": country_code,
                "subtitle": f"Attraction in {clean_ascii(city_name)}",
                "canonical_value": clean_ascii(f"{poi.name}, {city_name}"),
                "canonical_id": f"poi:{poi.id}",
                "city_id": poi.city.id if poi.city else None,
                "latitude": None,
                "longitude": None,
                "image_url": poi.image_url or (poi.city.image_url if poi.city else None),
                "vibe": poi.category,
                "avg_daily_budget_inr": 0,
                "source": "local"
            })

        return results

    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        return self.autocomplete(query, limit)

    def resolve(self, identifier: str) -> Optional[Dict[str, Any]]:
        raw = identifier.strip()
        city = None

        # Check by city:id
        if raw.lower().startswith("city:"):
            parts = raw.split(":")
            if len(parts) >= 2 and parts[1].isdigit():
                city = self.db.query(City).filter(City.id == int(parts[1])).first()
            elif len(parts) >= 2:
                city_name = parts[1].replace("-", " ")
                city = self.db.query(City).filter(City.name.ilike(city_name)).first()
        elif raw.isdigit():
            city = self.db.query(City).filter(City.id == int(raw)).first()
        else:
            clean_name = raw.split(",")[0].strip()
            city = self.db.query(City).filter(City.name.ilike(clean_name)).first()

        if city:
            region_name = city.region.name if city.region else ""
            country_name = city.region.country.name if city.region and city.region.country else "India"
            country_code = city.region.country.code if city.region and city.region.country else "IN"
            return {
                "id": city.id,
                "name": city.name,
                "type": "city",
                "region_name": region_name,
                "country_name": country_name,
                "country_code": country_code,
                "latitude": city.latitude,
                "longitude": city.longitude,
                "vibe": city.vibe,
                "image_url": city.image_url,
                "best_months": city.best_months,
                "avg_daily_budget_inr": city.avg_daily_budget_inr,
                "source": "local",
                "city_obj": city
            }
        return None


# =====================================================================
# 2. EXTERNAL GEOCODING & GLOBAL REPOSITORY PROVIDER
# =====================================================================

class ExternalGeocodingProvider(LocationProvider):
    """Provides worldwide location search across all 195+ countries and global cities
    using high-speed memory cache and OpenStreetMap Nominatim live geocoding."""

    def __init__(self):
        self._cache: Dict[str, Any] = {}
        self._last_request_time = 0.0

    def _normalize(self, q: str) -> str:
        clean = q.strip().lower()
        return COUNTRY_ALIASES.get(clean, clean)

    def autocomplete(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        norm_q = self._normalize(query)
        if len(norm_q) < 2:
            return []

        if norm_q in self._cache:
            return self._cache[norm_q][:limit]

        results: List[Dict[str, Any]] = []

        # 1. Search Worldwide Countries
        for country_key, cdata in WORLD_COUNTRIES_DATA.items():
            if norm_q in country_key or norm_q == cdata["code"].lower() or norm_q in cdata["name"].lower():
                results.append({
                    "id": f"country_{cdata['code'].lower()}",
                    "type": "country",
                    "title": cdata["name"],
                    "region": cdata["continent"],
                    "country": cdata["name"],
                    "country_code": cdata["code"],
                    "subtitle": f"Country • {cdata['continent']}",
                    "canonical_value": cdata["name"],
                    "canonical_id": f"country:{cdata['name'].lower()}:{cdata['code'].lower()}",
                    "latitude": cdata["latitude"],
                    "longitude": cdata["longitude"],
                    "image_url": cdata["image_url"],
                    "vibe": cdata["vibe"],
                    "avg_daily_budget_inr": cdata["budget_inr"],
                    "source": "external"
                })

        # 2. Search Worldwide Cities Knowledge Base
        for city_key, cdata in WORLD_CITIES_DATA.items():
            if norm_q in city_key or norm_q in cdata["name"].lower() or norm_q in cdata["country"].lower():
                results.append({
                    "id": f"city_{city_key}",
                    "type": "city",
                    "title": cdata["name"],
                    "region": cdata["region"],
                    "country": cdata["country"],
                    "country_code": cdata["country_code"],
                    "subtitle": f"{cdata['region']}, {cdata['country']}",
                    "canonical_value": f"{cdata['name']}, {cdata['country']}",
                    "canonical_id": f"city:{city_key}:{cdata['country_code'].lower()}",
                    "latitude": cdata["latitude"],
                    "longitude": cdata["longitude"],
                    "image_url": cdata["image_url"],
                    "vibe": cdata["vibe"],
                    "avg_daily_budget_inr": cdata["budget_inr"],
                    "source": "external"
                })

        # 3. If results < 3 and query looks like a specific city/place, query Nominatim live with rate limit
        if len(results) < 3 and len(norm_q) >= 3:
            nominatim_results = self._fetch_nominatim(norm_q, limit=4)
            for nr in nominatim_results:
                if not any(r["title"].lower() == nr["title"].lower() for r in results):
                    results.append(nr)

        self._cache[norm_q] = results
        return results[:limit]

    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        return self.autocomplete(query, limit)

    def resolve(self, identifier: str) -> Optional[Dict[str, Any]]:
        raw = identifier.strip().lower()

        # Handle canonical prefixes
        if raw.startswith("country:"):
            parts = raw.split(":")
            c_name = parts[1] if len(parts) > 1 else raw
            norm_c = self._normalize(c_name)
            if norm_c in WORLD_COUNTRIES_DATA:
                return self._build_country_destination_intelligence(WORLD_COUNTRIES_DATA[norm_c])
            for k, v in WORLD_COUNTRIES_DATA.items():
                if norm_c in k or norm_c == v["code"].lower() or norm_c in v["name"].lower():
                    return self._build_country_destination_intelligence(v)

        if raw.startswith("city:"):
            parts = raw.split(":")
            c_name = parts[1] if len(parts) > 1 else raw
            norm_c = c_name.replace("-", " ")
            if norm_c in WORLD_CITIES_DATA:
                return self._build_city_destination_intelligence(WORLD_CITIES_DATA[norm_c])
            for k, v in WORLD_CITIES_DATA.items():
                if norm_c in k or norm_c in v["name"].lower():
                    return self._build_city_destination_intelligence(v)

        # Direct name match
        norm = self._normalize(raw.split(",")[0].strip())
        if norm in WORLD_COUNTRIES_DATA:
            return self._build_country_destination_intelligence(WORLD_COUNTRIES_DATA[norm])
        for k, v in WORLD_COUNTRIES_DATA.items():
            if norm in k or norm == v["code"].lower() or norm in v["name"].lower():
                return self._build_country_destination_intelligence(v)

        if norm in WORLD_CITIES_DATA:
            return self._build_city_destination_intelligence(WORLD_CITIES_DATA[norm])
        for k, v in WORLD_CITIES_DATA.items():
            if norm in k or norm in v["name"].lower():
                return self._build_city_destination_intelligence(v)

        # Fallback to live Nominatim resolution
        nominatim_res = self._fetch_nominatim(norm, limit=1)
        if nominatim_res:
            item = nominatim_res[0]
            synthetic_city = {
                "name": item["title"],
                "country": item["country"],
                "country_code": item["country_code"],
                "continent": "Global",
                "region": item["region"] or item["country"],
                "latitude": item["latitude"],
                "longitude": item["longitude"],
                "vibe": f"Worldwide destination in {item['country']} with scenic landmarks and rich heritage.",
                "best_months": "Year-round",
                "budget_inr": 12000,
                "image_url": "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=1200&auto=format&fit=crop&q=80",
                "attractions": [
                    {"name": f"Historic Center of {item['title']}", "category": "Heritage", "duration_minutes": 180, "entry_fee_inr": 0, "indoor_outdoor": "Outdoor", "description": f"Explore iconic landmarks and scenic plazas across {item['title']}."},
                    {"name": f"{item['title']} Cultural Museum", "category": "Museum", "duration_minutes": 120, "entry_fee_inr": 500, "indoor_outdoor": "Indoor", "description": f"Discover local traditions and artifacts of {item['country']}."},
                    {"name": f"{item['title']} Scenic Lookout", "category": "Viewpoint", "duration_minutes": 60, "entry_fee_inr": 0, "indoor_outdoor": "Outdoor", "description": f"Panoramic vistas overlooking {item['title']} and surrounding landscapes."}
                ]
            }
            return self._build_city_destination_intelligence(synthetic_city)

        return None

    def _build_country_destination_intelligence(self, cdata: Dict[str, Any]) -> Dict[str, Any]:
        """Constructs a rich destination intelligence payload for a country."""
        attractions = [
            {
                "id": idx + 1,
                "name": clean_ascii(att_name),
                "category": "Top Landmark",
                "duration_minutes": 180,
                "entry_fee_inr": 1000,
                "indoor_outdoor": "Both",
                "opening_hours": "08:30 - 18:00",
                "best_time_of_day": "Morning",
                "description": f"Must-visit global attraction in {clean_ascii(cdata['name'])}.",
                "image_url": cdata["image_url"]
            }
            for idx, att_name in enumerate(cdata.get("top_attractions", []))
        ]

        return {
            "id": f"country_{cdata['code'].lower()}",
            "name": clean_ascii(cdata["name"]),
            "type": "country",
            "region_name": clean_ascii(cdata["continent"]),
            "country_name": clean_ascii(cdata["name"]),
            "country_code": cdata["code"],
            "currency_code": cdata["currency"],
            "timezone": cdata["timezone"],
            "latitude": cdata["latitude"],
            "longitude": cdata["longitude"],
            "avg_daily_budget_inr": cdata["budget_inr"],
            "best_months": cdata["best_months"],
            "vibe": clean_ascii(cdata["vibe"]),
            "description": clean_ascii(f"Experience the majestic wonders of {cdata['name']}. From world-famous cultural icons to pristine landscapes, discover {', '.join(cdata.get('top_cities', []))}."),
            "image_url": cdata["image_url"],
            "attractions": attractions,
            "stays": [
                {
                    "id": 101,
                    "name": clean_ascii(f"The Luxury Grand {cdata['capital']}"),
                    "property_type": "5-Star Luxury Resort",
                    "price_per_night_inr": cdata["budget_inr"] * 2,
                    "rating": 4.9,
                    "review_count": 840,
                    "location_area": clean_ascii(f"{cdata['capital']} Prime Center"),
                    "distance_to_attraction": "0.8 km",
                    "amenities": ["Infinity Pool", "Luxury Spa", "Michelin Dining", "Airport Limousine"],
                    "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=600&auto=format&fit=crop&q=80",
                    "description": clean_ascii(f"Premier 5-star sanctuary located in the heart of {cdata['name']}."),
                    "is_demo_availability": True
                },
                {
                    "id": 102,
                    "name": clean_ascii(f"Heritage Boutique Villa {cdata['name']}"),
                    "property_type": "Boutique Hotel",
                    "price_per_night_inr": int(cdata["budget_inr"] * 1.2),
                    "rating": 4.8,
                    "review_count": 420,
                    "location_area": "Historic Cultural Quarter",
                    "distance_to_attraction": "1.2 km",
                    "amenities": ["Rooftop Garden", "Artisan Breakfast", "Concierge"],
                    "image_url": "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=600&auto=format&fit=crop&q=80",
                    "description": clean_ascii(f"Charming boutique hotel reflecting traditional {cdata['name']} architecture."),
                    "is_demo_availability": True
                }
            ],
            "restaurants": [
                {
                    "id": 201,
                    "name": clean_ascii(f"Signature Culinary Atelier {cdata['capital']}"),
                    "cuisine_type": clean_ascii(f"Authentic {cdata['name']} Fine Dining"),
                    "category": "Fine Dining",
                    "price_level": "$$$",
                    "avg_meal_cost_inr": 2800,
                    "rating": 4.9,
                    "review_count": 650,
                    "location_area": "Downtown Gourmet Boulevard",
                    "popular_dishes": ["Chef Tasting Menu", "National Heritage Special"],
                    "dietary_tags": ["Vegetarian Options", "Organic"],
                    "opening_hours": "12:00 - 23:00",
                    "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600&auto=format&fit=crop&q=80",
                    "description": clean_ascii(f"Celebrated gastronomy showcasing the finest regional flavors of {cdata['name']}."),
                    "is_demo_reservation": True
                }
            ],
            "videos": [],
            "guides": [],
            "experiences": [],
            "travel_requirement": {
                "passport_validity": "Valid for at least 6 months beyond intended stay",
                "visa_requirement": clean_ascii(cdata.get("visa_guidelines", "Standard tourist visa or electronic authorization")),
                "customs_advisory": "Declare currency exceeding $10,000 USD and restricted agricultural products.",
                "currency_regulations": f"National Currency is {cdata['currency']}. Credit cards widely accepted in major cities.",
                "official_portal_url": f"https://www.worldtravelholic.com/visas/{cdata['code'].lower()}",
                "disclaimer": "Travel and visa guidelines are for reference. Verify current requirements with the official embassy."
            }
        }

    def _build_city_destination_intelligence(self, cdata: Dict[str, Any]) -> Dict[str, Any]:
        """Constructs a rich destination intelligence payload for a city."""
        country_meta = WORLD_COUNTRIES_DATA.get(cdata["country"].lower(), {})
        currency = country_meta.get("currency", "USD")
        timezone = country_meta.get("timezone", "UTC")
        visa_guide = country_meta.get("visa_guidelines", "Standard tourist visa required")

        attractions = [
            {
                "id": idx + 1,
                "name": clean_ascii(att["name"]),
                "category": clean_ascii(att.get("category", "Landmark")),
                "duration_minutes": att.get("duration_minutes", 120),
                "entry_fee_inr": att.get("entry_fee_inr", 500),
                "indoor_outdoor": att.get("indoor_outdoor", "Both"),
                "opening_hours": "09:00 - 18:00",
                "best_time_of_day": "Morning",
                "description": clean_ascii(att.get("description", f"Iconic highlight in {cdata['name']}.")),
                "image_url": cdata["image_url"]
            }
            for idx, att in enumerate(cdata.get("attractions", []))
        ]

        return {
            "id": f"city_{cdata['name'].lower()}",
            "name": clean_ascii(cdata["name"]),
            "type": "city",
            "region_name": clean_ascii(cdata.get("region", cdata["country"])),
            "country_name": clean_ascii(cdata["country"]),
            "country_code": cdata.get("country_code", "XX"),
            "currency_code": currency,
            "timezone": timezone,
            "latitude": cdata["latitude"],
            "longitude": cdata["longitude"],
            "avg_daily_budget_inr": cdata["budget_inr"],
            "best_months": cdata["best_months"],
            "vibe": clean_ascii(cdata["vibe"]),
            "description": clean_ascii(f"Welcome to {cdata['name']}, {cdata['country']}. {cdata['vibe']}. Explore world-renowned landmarks, vibrant cultural districts, and culinary delights."),
            "image_url": cdata["image_url"],
            "attractions": attractions,
            "stays": [
                {
                    "id": 301,
                    "name": clean_ascii(f"The Grand {cdata['name']} Palace Hotel"),
                    "property_type": "5-Star Luxury Resort",
                    "price_per_night_inr": cdata["budget_inr"] * 2,
                    "rating": 4.9,
                    "review_count": 920,
                    "location_area": clean_ascii(f"Central {cdata['name']}"),
                    "distance_to_attraction": "0.5 km",
                    "amenities": ["Rooftop Pool", "Spa & Wellness", "Michelin Dining", "Panoramic Views"],
                    "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=600&auto=format&fit=crop&q=80",
                    "description": clean_ascii(f"Luxury oasis with supreme hospitality in {cdata['name']}."),
                    "is_demo_availability": True
                },
                {
                    "id": 302,
                    "name": clean_ascii(f"{cdata['name']} Boutique Heritage Suites"),
                    "property_type": "Boutique Hotel",
                    "price_per_night_inr": int(cdata["budget_inr"] * 1.1),
                    "rating": 4.8,
                    "review_count": 480,
                    "location_area": "Historic Arts District",
                    "distance_to_attraction": "1.0 km",
                    "amenities": ["Free High-Speed Wi-Fi", "Artisan Coffee", "City View Balcony"],
                    "image_url": "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=600&auto=format&fit=crop&q=80",
                    "description": clean_ascii(f"Stylish boutique comfort close to top attractions in {cdata['name']}."),
                    "is_demo_availability": True
                }
            ],
            "restaurants": [
                {
                    "id": 401,
                    "name": clean_ascii(f"L'Atelier de {cdata['name']}"),
                    "cuisine_type": clean_ascii(f"Signature {cdata['country']} Cuisine"),
                    "category": "Fine Dining",
                    "price_level": "$$$",
                    "avg_meal_cost_inr": 2400,
                    "rating": 4.9,
                    "review_count": 780,
                    "location_area": "Downtown Gourmet Row",
                    "popular_dishes": ["Chef Signature Platter", "Local Tasting Flight"],
                    "dietary_tags": ["Vegetarian Options", "Gluten-Free Options"],
                    "opening_hours": "11:30 - 22:30",
                    "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600&auto=format&fit=crop&q=80",
                    "description": clean_ascii(f"Authentic award-winning gastronomy celebrating {cdata['name']}'s local harvest."),
                    "is_demo_reservation": True
                }
            ],
            "videos": [],
            "guides": [],
            "experiences": [],
            "travel_requirement": {
                "passport_validity": "Valid for 6 months beyond travel dates",
                "visa_requirement": clean_ascii(visa_guide),
                "customs_advisory": "Standard customs declaration applies at entry checkpoints.",
                "currency_regulations": f"Official currency is {currency}. International cards widely accepted.",
                "official_portal_url": f"https://www.worldtravelholic.com/visas/{cdata.get('country_code', 'xx').lower()}",
                "disclaimer": "Travel rules and advisories are updated regularly. Check with official authorities."
            }
        }

    def _fetch_nominatim(self, query: str, limit: int = 4) -> List[Dict[str, Any]]:
        """Queries OpenStreetMap Nominatim API with rate limiting and timeout safeguards."""
        now = time.time()
        if now - self._last_request_time < 0.5:
            time.sleep(0.5)
        self._last_request_time = time.time()

        url = "https://nominatim.openstreetmap.org/search"
        headers = {
            "User-Agent": "WorldTravelholic/1.0 (contact: info@worldtravelholic.internal)"
        }
        params = {
            "q": query,
            "format": "json",
            "addressdetails": 1,
            "limit": limit
        }

        try:
            with httpx.Client(timeout=3.0) as client:
                resp = client.get(url, params=params, headers=headers)
                if resp.status_code != 200:
                    return []
                data = resp.json()
                results = []
                for item in data:
                    addr = item.get("address", {})
                    raw_city = (
                        addr.get("city") or
                        addr.get("town") or
                        addr.get("village") or
                        addr.get("state") or
                        item.get("name") or
                        query.title()
                    )
                    city_name = clean_ascii(raw_city)
                    country_name = clean_ascii(addr.get("country", ""))
                    country_code = addr.get("country_code", "").upper()
                    state_name = clean_ascii(addr.get("state", ""))
                    place_type = "city" if addr.get("city") or addr.get("town") else (
                        "country" if item.get("type") == "administrative" and not addr.get("city") else "place"
                    )

                    lat = float(item.get("lat", 0))
                    lon = float(item.get("lon", 0))
                    canonical_val = f"{city_name}, {country_name}".strip(", ")
                    subtitle_val = f"{state_name + ', ' if state_name else ''}{country_name}".strip(", ")
                    results.append({
                        "id": f"geo_{item.get('osm_id', int(time.time()))}",
                        "type": place_type,
                        "title": city_name,
                        "region": state_name or country_name,
                        "country": country_name,
                        "country_code": country_code,
                        "subtitle": subtitle_val,
                        "canonical_value": canonical_val,
                        "canonical_id": f"place:{city_name.lower().replace(' ', '-')}:{country_code.lower()}",
                        "latitude": lat,
                        "longitude": lon,
                        "image_url": "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=800&auto=format&fit=crop&q=80",
                        "vibe": f"Scenic destination in {country_name}",
                        "avg_daily_budget_inr": 10000,
                        "source": "external_geocoder"
                    })
                return results
        except Exception as e:
            logger.debug(f"Nominatim lookup skipped or timed out: {e}")
            return []


# =====================================================================
# 3. GLOBAL LOCATION SERVICE (AGGREGATOR & RESOLVER)
# =====================================================================

class GlobalLocationService:
    def __init__(self):
        self.external_provider = ExternalGeocodingProvider()

    def autocomplete(self, db: Session, query: str, limit: int = 12) -> List[Dict[str, Any]]:
        """1. Search local database first.
           2. If insufficient, query external global provider.
           3. Merge and deduplicate by canonical value.
        """
        clean_q = query.strip()
        if not clean_q or len(clean_q) < 1:
            return []

        local_provider = LocalDatabaseProvider(db)
        local_results = local_provider.autocomplete(clean_q, limit=limit)

        # Query external provider
        external_results = self.external_provider.autocomplete(clean_q, limit=limit)

        # Merge results, prioritizing local database
        seen_titles = set()
        combined: List[Dict[str, Any]] = []

        for item in local_results:
            key = (item["title"].lower(), item["type"].lower())
            if key not in seen_titles:
                seen_titles.add(key)
                combined.append(item)

        for item in external_results:
            key = (item["title"].lower(), item["type"].lower())
            if key not in seen_titles:
                seen_titles.add(key)
                combined.append(item)

        return combined[:limit]

    def search(self, db: Session, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        return self.autocomplete(db, query, limit)

    def resolve(self, db: Session, identifier: str) -> Optional[Dict[str, Any]]:
        """Resolves any destination (local DB, worldwide country, or worldwide city)."""
        clean_id = identifier.strip()
        
        # 1. Try local DB provider first
        local_provider = LocalDatabaseProvider(db)
        local_res = local_provider.resolve(clean_id)
        if local_res:
            return local_res

        # 2. Try global external provider
        return self.external_provider.resolve(clean_id)

    def get_map_destinations(self, db: Session) -> List[Dict[str, Any]]:
        """Combines local database destinations + major world capitals/destinations
        to power a truly global Leaflet map."""
        local_cities = db.query(City).all()
        results: List[Dict[str, Any]] = []
        seen_names = set()

        for city in local_cities:
            region_name = city.region.name if city.region else ""
            country_name = city.region.country.name if city.region and city.region.country else "India"
            country_code = city.region.country.code if city.region and city.region.country else "IN"
            continent = city.region.country.continent if city.region and city.region.country else "Asia"

            rating = 4.9
            if city.hotels:
                ratings = [h.rating for h in city.hotels if h.rating]
                if ratings:
                    rating = round(sum(ratings) / len(ratings), 2)

            seen_names.add(city.name.lower())
            results.append({
                "id": city.id,
                "city": city.name,
                "name": city.name,
                "region": region_name,
                "country": country_name,
                "country_code": country_code,
                "continent": continent,
                "latitude": city.latitude,
                "longitude": city.longitude,
                "image_url": city.image_url or "https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=600&auto=format&fit=crop&q=80",
                "vibe": city.vibe,
                "category": city.vibe.split(",")[0].strip() if city.vibe else "Heritage & Culture",
                "avg_daily_budget_inr": city.avg_daily_budget_inr,
                "best_months": city.best_months,
                "rating": rating,
                "poi_count": len(city.pois),
                "canonical_id": f"city:{city.id}",
                "canonical_name": f"{city.name}, {region_name}, {country_name}".replace(" ,", "").strip(", "),
                "source": "local"
            })

        # Add top global world cities to populate all continents
        for city_key, cdata in WORLD_CITIES_DATA.items():
            if cdata["name"].lower() not in seen_names:
                seen_names.add(cdata["name"].lower())
                results.append({
                    "id": f"global_{city_key}",
                    "city": cdata["name"],
                    "name": cdata["name"],
                    "region": cdata["region"],
                    "country": cdata["country"],
                    "country_code": cdata["country_code"],
                    "continent": cdata["continent"],
                    "latitude": cdata["latitude"],
                    "longitude": cdata["longitude"],
                    "image_url": cdata["image_url"],
                    "vibe": cdata["vibe"],
                    "category": cdata["vibe"].split(",")[0].strip(),
                    "avg_daily_budget_inr": cdata["budget_inr"],
                    "best_months": cdata["best_months"],
                    "rating": 4.9,
                    "poi_count": len(cdata.get("attractions", [])),
                    "canonical_id": f"city:{city_key}:{cdata['country_code'].lower()}",
                    "canonical_name": f"{cdata['name']}, {cdata['country']}",
                    "source": "global"
                })

        return results


# Global Singleton Instance
global_location_service = GlobalLocationService()
