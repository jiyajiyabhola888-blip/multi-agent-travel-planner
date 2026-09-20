"""Comprehensive Global and Domestic Travel Database for WORLD TRAVELHOLIC 🌍.
Supports India (all states/UTs) and major global destinations with Stays, Restaurants, Attractions, Guides, Experiences, Videos, and Travel Requirements.
"""

COUNTRIES_DATA = [
    {
        "code": "IN",
        "name": "India",
        "continent": "Asia",
        "currency_code": "INR",
        "timezone": "Asia/Kolkata",
        "hero_image": "https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=1200&auto=format&fit=crop&q=80",
        "visa_guidelines": "Indian citizens travel with domestic photo ID. International travelers require an Indian e-Visa / Tourist Visa prior to departure.",
        "requirement": {
            "passport_validity": "Minimum 6 months validity from date of arrival.",
            "visa_requirement": "Online e-Tourist Visa (30-day, 1-year, or 5-year) available for 165+ nationalities.",
            "customs_advisory": "Declare foreign currency exceeding $5,000 USD or equivalent.",
            "currency_regulations": "Indian Rupee (INR). Digital UPI and cards accepted widely.",
            "official_portal_url": "https://indianvisaonline.gov.in"
        },
        "regions": [
            {
                "name": "Rajasthan",
                "is_ut": False,
                "cities": [
                    {
                        "name": "Jaipur",
                        "lat": 26.9124,
                        "lon": 75.7873,
                        "budget": 4200,
                        "best": "Oct-Mar",
                        "vibe": "Royal Palaces, Pink Stone & Vibrant Bazaars",
                        "image_url": "https://images.unsplash.com/photo-1599661046289-e31897846e41?w=800&auto=format&fit=crop&q=80",
                        "description": "The Pink City of India, world-famous for its majestic hill forts, intricate lattice palaces, block print textiles, and opulent Rajput hospitality.",
                        "pois": [
                            {"name": "Amber Fort & Sheesh Mahal", "cat": "Heritage", "duration": 180, "fee": 100, "in_out": "Outdoor", "desc": "16th-century hilltop fortress featuring mirror-inlaid palaces, ramparts, and Maota Lake views.", "image_url": "https://images.unsplash.com/photo-1599661046289-e31897846e41?w=600&auto=format&fit=crop&q=80"},
                            {"name": "Hawa Mahal (Palace of Winds)", "cat": "Heritage", "duration": 60, "fee": 50, "in_out": "Mixed", "desc": "Iconic five-story pink sandstone facade with 953 honeycombed jharokhas.", "image_url": "https://images.unsplash.com/photo-1606293926075-69a00dbfde81?w=600&auto=format&fit=crop&q=80"},
                            {"name": "City Palace & Chandra Mahal", "cat": "Heritage", "duration": 120, "fee": 200, "in_out": "Mixed", "desc": "Grand royal courtyard complex with fusion Rajput-Mughal architecture.", "image_url": "https://images.unsplash.com/photo-1599661046289-e31897846e41?w=600&auto=format&fit=crop&q=80"},
                            {"name": "Jantar Mantar Astronomical Observatory", "cat": "Heritage", "duration": 75, "fee": 50, "in_out": "Outdoor", "desc": "UNESCO World Heritage collection of 19 architectural astronomical instruments.", "image_url": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=600&auto=format&fit=crop&q=80"},
                            {"name": "Nahargarh Fort Golden Hour Viewpoint", "cat": "Romantic", "duration": 90, "fee": 50, "in_out": "Outdoor", "desc": "Panoramic ridge overlooking the entire Pink City lights at dusk.", "image_url": "https://images.unsplash.com/photo-1599661046289-e31897846e41?w=600&auto=format&fit=crop&q=80"},
                            {"name": "Johari & Bapu Bazaars Craft Walk", "cat": "Culinary", "duration": 120, "fee": 0, "in_out": "Outdoor", "desc": "Lively street bazaars famous for Jaipuri quilts, gemstones, and street snacks.", "image_url": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=600&auto=format&fit=crop&q=80"}
                        ],
                        "hotels": [
                            {"name": "The Oberoi Rajvilas", "property_type": "Luxury Resort", "price_per_night_inr": 28000, "rating": 4.95, "review_count": 310, "location_area": "Goner Road", "distance_to_attraction": "8 km from City Palace", "amenities": ["Luxury Tented Villas", "Ayurvedic Spa", "Royal Courtyard Dining", "Infinity Pool"], "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=600&auto=format&fit=crop&q=80", "description": "Set in 32 acres of landscaped gardens with traditional Rajasthani architecture and private pools."},
                            {"name": "Samode Haveli Boutique Palace", "property_type": "Heritage Stay", "price_per_night_inr": 9500, "rating": 4.88, "review_count": 220, "location_area": "Old Walled City", "distance_to_attraction": "1.2 km from Hawa Mahal", "amenities": ["Heritage Suites", "Courtyard Pool", "Traditional Rajasthani Music", "Free High-Speed WiFi"], "image_url": "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=600&auto=format&fit=crop&q=80", "description": "An intimate 225-year-old historic urban mansion converted into a luxury boutique heritage retreat."},
                            {"name": "Pearl Palace Heritage Boutique Stay", "property_type": "Boutique Hotel", "price_per_night_inr": 3800, "rating": 4.82, "review_count": 480, "location_area": "Hathroi Fort", "distance_to_attraction": "2.8 km from City Center", "amenities": ["Rooftop Cafe (Peacock Cafe)", "Artisan Decor", "AC Rooms", "Travel Desk"], "image_url": "https://images.unsplash.com/photo-1590490360182-c33d57733427?w=600&auto=format&fit=crop&q=80", "description": "Consistently rated one of the best value boutique hotels in Rajasthan with ornate hand-carved rooms."},
                            {"name": "Zostel Jaipur Walled City", "property_type": "Hostel", "price_per_night_inr": 1200, "rating": 4.75, "review_count": 640, "location_area": "Old City Bapu Bazaar", "distance_to_attraction": "500m from Hawa Mahal", "amenities": ["Rooftop Common Room", "Free Walking Tours", "High Speed WiFi", "Female-Only Dorms"], "image_url": "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?w=600&auto=format&fit=crop&q=80", "description": "Vibrant backpacker hub inside the heritage walled city with daily cultural workshops and hostel meetups."}
                        ],
                        "restaurants": [
                            {"name": "1135 AD - Amber Fort Royal Dining", "cuisine_type": "Royal Rajasthani & North Indian", "category": "Fine Dining", "price_level": "$$$$", "avg_meal_cost_inr": 2200, "rating": 4.9, "review_count": 190, "location_area": "Amber Fort Complex", "popular_dishes": ["Laal Maas", "Shahi Paneer", "Thal of Mewar", "Saffron Kheer"], "dietary_tags": ["Vegetarian Options", "Halal Friendly"], "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600&auto=format&fit=crop&q=80", "description": "Regal fine dining inside the historical ramparts of Amber Fort with silver cutlery and candlelight."},
                            {"name": "Laxmi Misthan Bhandar (LMB)", "cuisine_type": "Traditional Rajasthani & Sweets", "category": "Top Restaurant", "price_level": "$$", "avg_meal_cost_inr": 650, "rating": 4.8, "review_count": 820, "location_area": "Johari Bazaar", "popular_dishes": ["Rajasthani Royal Thali", "Pyaaz Kachori", "Ghewar", "Dal Baati Churma"], "dietary_tags": ["100% Pure Vegetarian", "Jain Friendly"], "image_url": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=600&auto=format&fit=crop&q=80", "description": "Iconic sweet shop and heritage restaurant serving authentic Marwari thalis since 1727 in Johari Bazaar."},
                            {"name": "Tapri Central - Tea & Bites", "cuisine_type": "Contemporary Indian Street Food & Chai", "category": "Popular Cafe", "price_level": "$", "avg_meal_cost_inr": 350, "rating": 4.85, "review_count": 1100, "location_area": "C-Scheme", "popular_dishes": ["Hand-pounded Masala Chai", "Khichiya Papad", "Tadka Maggi", "Cheese Corn Shots"], "dietary_tags": ["Vegetarian", "Vegan Friendly"], "image_url": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=600&auto=format&fit=crop&q=80", "description": "Rooftop terrace overlooking Central Park, celebrated for artisanal chais and creative street fusion snacks."}
                        ],
                        "videos": [
                            {"title": "Explore Jaipur: The Pink City Royal Guide", "duration_str": "4:45", "thumbnail_url": "https://images.unsplash.com/photo-1599661046289-e31897846e41?w=600&auto=format&fit=crop&q=80", "video_url": "https://www.youtube.com/watch?v=sample_jaipur", "category": "City Guide"},
                            {"title": "Top 10 Things to Do in Amber Fort & Old City", "duration_str": "6:10", "thumbnail_url": "https://images.unsplash.com/photo-1606293926075-69a00dbfde81?w=600&auto=format&fit=crop&q=80", "video_url": "https://www.youtube.com/watch?v=sample_amber", "category": "Attractions"}
                        ]
                    },
                    {
                        "name": "Udaipur",
                        "lat": 24.5854,
                        "lon": 73.7125,
                        "budget": 5200,
                        "best": "Sep-Mar",
                        "vibe": "City of Lakes, Palaces & Romance",
                        "image_url": "https://images.unsplash.com/photo-1615836245337-f5b9b2303f10?w=800&auto=format&fit=crop&q=80",
                        "description": "Venice of the East, famed for shimmering Lake Pichola, floating white marble palaces, and scenic rooftop restaurants.",
                        "pois": [
                            {"name": "City Palace Udaipur & Museum", "cat": "Heritage", "duration": 150, "fee": 300, "in_out": "Mixed", "desc": "Rajasthan's largest royal palace complex with panoramic lake balconies.", "image_url": "https://images.unsplash.com/photo-1615836245337-f5b9b2303f10?w=600&auto=format&fit=crop&q=80"},
                            {"name": "Lake Pichola Sunset Boat Cruise", "cat": "Romantic", "duration": 75, "fee": 450, "in_out": "Outdoor", "desc": "Serene cruise gliding past Jag Mandir and the Lake Palace at dusk.", "image_url": "https://images.unsplash.com/photo-1615836245337-f5b9b2303f10?w=600&auto=format&fit=crop&q=80"},
                            {"name": "Saheliyon-ki-Bari (Courtyard of Maidens)", "cat": "Nature", "duration": 60, "fee": 50, "in_out": "Outdoor", "desc": "Historic royal garden with marble fountains, lotus pools, and kiosks.", "image_url": "https://images.unsplash.com/photo-1615836245337-f5b9b2303f10?w=600&auto=format&fit=crop&q=80"},
                            {"name": "Bagore Ki Haveli Folk Dance Show", "cat": "Heritage", "duration": 75, "fee": 100, "in_out": "Indoor", "desc": "Vibrant Dharohar evening Rajasthani folk dance and puppet performance.", "image_url": "https://images.unsplash.com/photo-1615836245337-f5b9b2303f10?w=600&auto=format&fit=crop&q=80"}
                        ],
                        "hotels": [
                            {"name": "Taj Lake Palace Udaipur", "property_type": "Luxury Resort", "price_per_night_inr": 35000, "rating": 4.96, "review_count": 410, "location_area": "Lake Pichola", "distance_to_attraction": "Inside Lake Pichola", "amenities": ["Island Palace", "Royal Butler Service", "Jiva Spa Boat", "Fine Dining"], "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=600&auto=format&fit=crop&q=80", "description": "18th-century floating white marble palace set in the middle of tranquil Lake Pichola."},
                            {"name": "Jagat Niwas Palace Heritage Hotel", "property_type": "Heritage Stay", "price_per_night_inr": 7200, "rating": 4.86, "review_count": 280, "location_area": "Lal Ghat", "distance_to_attraction": "300m from City Palace", "amenities": ["Lakeview Jharokhas", "Rooftop Restaurant", "Heritage Decor"], "image_url": "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=600&auto=format&fit=crop&q=80", "description": "Authentic lakefront mansion with cushioned jharokhas overlooking the calm waters."}
                        ],
                        "restaurants": [
                            {"name": "Ambrai Restaurant at Amet Haveli", "cuisine_type": "Mughlai & Rajasthani", "category": "Top Restaurant", "price_level": "$$$", "avg_meal_cost_inr": 1400, "rating": 4.88, "review_count": 950, "location_area": "Hanuman Ghat", "popular_dishes": ["Mewari Govind Gatta", "Mutton Rogan Josh", "Paneer Lababdar"], "dietary_tags": ["Vegetarian Options"], "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600&auto=format&fit=crop&q=80", "description": "Unrivaled waterfront dining facing the floodlit City Palace and Lake Palace."}
                        ],
                        "videos": [
                            {"title": "Discover Udaipur: The Romantic City of Lakes", "duration_str": "5:15", "thumbnail_url": "https://images.unsplash.com/photo-1615836245337-f5b9b2303f10?w=600&auto=format&fit=crop&q=80", "video_url": "https://www.youtube.com/watch?v=sample_udaipur", "category": "City Guide"}
                        ]
                    }
                ]
            },
            {
                "name": "Delhi",
                "is_ut": True,
                "cities": [
                    {
                        "name": "New Delhi",
                        "lat": 28.6139,
                        "lon": 77.2090,
                        "budget": 4500,
                        "best": "Oct-Mar",
                        "vibe": "Heritage Monuments, Mughal Cuisine & Tree-lined Avenues",
                        "image_url": "https://images.unsplash.com/photo-1587474260584-136574528ed5?w=800&auto=format&fit=crop&q=80",
                        "description": "India's capital bridging historic Mughal architecture with grand colonial boulevards and world-class street food.",
                        "pois": [
                            {"name": "Qutub Minar Complex", "cat": "Heritage", "duration": 90, "fee": 50, "in_out": "Outdoor", "desc": "UNESCO World Heritage 73m brick minaret built in 1192 AD.", "image_url": "https://images.unsplash.com/photo-1587474260584-136574528ed5?w=600&auto=format&fit=crop&q=80"},
                            {"name": "Humayun's Tomb", "cat": "Heritage", "duration": 100, "fee": 50, "in_out": "Outdoor", "desc": "Mughal garden tomb architectural inspiration for the Taj Mahal.", "image_url": "https://images.unsplash.com/photo-1587474260584-136574528ed5?w=600&auto=format&fit=crop&q=80"},
                            {"name": "Old Delhi Chandni Chowk Food Trail", "cat": "Culinary", "duration": 150, "fee": 300, "in_out": "Mixed", "desc": "Legendary street food trail for paranthas, kebabs, and jalebis.", "image_url": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=600&auto=format&fit=crop&q=80"},
                            {"name": "India Gate & Kartavya Path", "cat": "Sightseeing", "duration": 60, "fee": 0, "in_out": "Outdoor", "desc": "War memorial arch and lush public lawns along the ceremonial axis.", "image_url": "https://images.unsplash.com/photo-1587474260584-136574528ed5?w=600&auto=format&fit=crop&q=80"}
                        ],
                        "hotels": [
                            {"name": "The Imperial New Delhi", "property_type": "Heritage Stay", "price_per_night_inr": 18000, "rating": 4.9, "review_count": 350, "location_area": "Janpath", "distance_to_attraction": "1 km from Connaught Place", "amenities": ["Victorian Decor", "Spa", "Heritage Gardens"], "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=600&auto=format&fit=crop&q=80", "description": "Legendary colonial-era heritage hotel with private art galleries and lush palms."},
                            {"name": "Bloomrooms @ Janpath", "property_type": "Boutique Hotel", "price_per_night_inr": 4200, "rating": 4.7, "review_count": 520, "location_area": "Central Delhi", "distance_to_attraction": "2 km from India Gate", "amenities": ["Crisp Clean Rooms", "Cafe", "Free WiFi"], "image_url": "https://images.unsplash.com/photo-1590490360182-c33d57733427?w=600&auto=format&fit=crop&q=80", "description": "Ultra-clean modern boutique rooms located centrally for easy sightseeing."}
                        ],
                        "restaurants": [
                            {"name": "Karim's Historic Old Delhi", "cuisine_type": "Mughlai", "category": "Top Restaurant", "price_level": "$$", "avg_meal_cost_inr": 600, "rating": 4.8, "review_count": 1400, "location_area": "Jama Masjid", "popular_dishes": ["Mutton Korma", "Seekh Kebab", "Tandoori Roti"], "dietary_tags": ["Halal"], "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600&auto=format&fit=crop&q=80", "description": "Legendary royal Mughal recipes preserved since 1913 near Jama Masjid."}
                        ],
                        "videos": [
                            {"title": "New Delhi Insider: Heritage & Food Trail", "duration_str": "5:30", "thumbnail_url": "https://images.unsplash.com/photo-1587474260584-136574528ed5?w=600&auto=format&fit=crop&q=80", "video_url": "https://www.youtube.com/watch?v=sample_delhi", "category": "City Guide"}
                        ]
                    }
                ]
            },
            {
                "name": "Maharashtra",
                "is_ut": False,
                "cities": [
                    {
                        "name": "Mumbai",
                        "lat": 18.9220,
                        "lon": 72.8347,
                        "budget": 6000,
                        "best": "Nov-Feb",
                        "vibe": "Coastal Metropolis, Art Deco & Bollywood",
                        "image_url": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?w=800&auto=format&fit=crop&q=80",
                        "description": "The City of Dreams, featuring historic Victorian gothic architecture, seaside promenades, and vibrant nightlife.",
                        "pois": [
                            {"name": "Gateway of India & Colaba", "cat": "Heritage", "duration": 90, "fee": 0, "in_out": "Outdoor", "desc": "Grand stone arch facing Mumbai harbor built to commemorate King George V.", "image_url": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?w=600&auto=format&fit=crop&q=80"},
                            {"name": "Marine Drive Queen's Necklace", "cat": "Sightseeing", "duration": 60, "fee": 0, "in_out": "Outdoor", "desc": "C-shaped 3.6-kilometer coastal boulevard illuminated by evening arc lights.", "image_url": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?w=600&auto=format&fit=crop&q=80"},
                            {"name": "Elephanta Caves UNESCO Ferry Excursion", "cat": "Heritage", "duration": 240, "fee": 40, "in_out": "Mixed", "desc": "Ancient rock-cut cave temples dedicated to Shiva on an island in Mumbai Harbor.", "image_url": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?w=600&auto=format&fit=crop&q=80"}
                        ],
                        "hotels": [
                            {"name": "The Taj Mahal Palace Mumbai", "property_type": "Luxury Resort", "price_per_night_inr": 26000, "rating": 4.97, "review_count": 650, "location_area": "Colaba", "distance_to_attraction": "Facing Gateway of India", "amenities": ["Harbor View", "Sea Lounge High Tea", "Jiva Spa"], "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=600&auto=format&fit=crop&q=80", "description": "India's most iconic heritage hotel overlooking the Arabian Sea since 1903."}
                        ],
                        "restaurants": [
                            {"name": "Britannia & Co. Irani Cafe", "cuisine_type": "Parsi & Irani", "category": "Top Restaurant", "price_level": "$$", "avg_meal_cost_inr": 700, "rating": 4.75, "review_count": 610, "location_area": "Ballard Estate", "popular_dishes": ["Berry Pulao", "Mutton Dhansak", "Caramel Custard"], "dietary_tags": ["Non-Veg", "Parsi Special"], "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600&auto=format&fit=crop&q=80", "description": "Vintage 1923 Irani cafe celebrated for its legendary Iranian Berry Pulao."}
                        ],
                        "videos": [
                            {"title": "Explore Mumbai: From Colaba to Bandra", "duration_str": "6:20", "thumbnail_url": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?w=600&auto=format&fit=crop&q=80", "video_url": "https://www.youtube.com/watch?v=sample_mumbai", "category": "City Guide"}
                        ]
                    }
                ]
            },
            {
                "name": "Goa",
                "is_ut": False,
                "cities": [
                    {
                        "name": "Goa",
                        "lat": 15.2993,
                        "lon": 74.1240,
                        "budget": 4800,
                        "best": "Nov-Apr",
                        "vibe": "Sun-Kissed Beaches, Portuguese Architecture & Seafood",
                        "image_url": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=800&auto=format&fit=crop&q=80",
                        "description": "Tropical paradise of golden beaches, UNESCO baroque churches, spice farms, and beach shacks.",
                        "pois": [
                            {"name": "Palolem & Agonda Crescent Beaches", "cat": "Relaxation", "duration": 180, "fee": 0, "in_out": "Outdoor", "desc": "Pristine white sand crescent beach surrounded by coconut palms.", "image_url": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=600&auto=format&fit=crop&q=80"},
                            {"name": "Basilica of Bom Jesus & Old Goa", "cat": "Heritage", "duration": 90, "fee": 0, "in_out": "Indoor", "desc": "16th-century UNESCO World Heritage baroque church holding St. Francis Xavier's relics.", "image_url": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=600&auto=format&fit=crop&q=80"},
                            {"name": "Fontainhas Latin Quarter Heritage Walk", "cat": "Sightseeing", "duration": 120, "fee": 0, "in_out": "Outdoor", "desc": "Colorful Portuguese heritage quarter with pastel villas, tiled roofs, and art galleries.", "image_url": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=600&auto=format&fit=crop&q=80"}
                        ],
                        "hotels": [
                            {"name": "Taj Exotica Resort & Spa Goa", "property_type": "Luxury Resort", "price_per_night_inr": 22000, "rating": 4.92, "review_count": 380, "location_area": "Benaulim Beach", "distance_to_attraction": "Direct Beach Access", "amenities": ["Private Beach", "Golf Course", "Ayurvedic Spa"], "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=600&auto=format&fit=crop&q=80", "description": "Mediterranean-style resort spread across 56 acres of lush gardens along Benaulim Beach."}
                        ],
                        "restaurants": [
                            {"name": "Fisherman's Wharf", "cuisine_type": "Goan Seafood & Portuguese", "category": "Top Restaurant", "price_level": "$$", "avg_meal_cost_inr": 900, "rating": 4.85, "review_count": 890, "location_area": "Cavelossim", "popular_dishes": ["Goan Prawn Curry", "Fish Recheado", "Bebinca"], "dietary_tags": ["Seafood Specialty"], "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600&auto=format&fit=crop&q=80", "description": "Riverside dining overlooking fishing trawlers with live music and authentic Goan spices."}
                        ],
                        "videos": [
                            {"title": "Goa Beyond Beaches: Food & Heritage", "duration_str": "4:50", "thumbnail_url": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=600&auto=format&fit=crop&q=80", "video_url": "https://www.youtube.com/watch?v=sample_goa", "category": "City Guide"}
                        ]
                    }
                ]
            }
        ]
    },
    {
        "code": "FR",
        "name": "France",
        "continent": "Europe",
        "currency_code": "EUR",
        "timezone": "Europe/Paris",
        "hero_image": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1200&auto=format&fit=crop&q=80",
        "visa_guidelines": "Schengen Visa required for non-EU travelers. Valid across 29 European countries for up to 90 days.",
        "requirement": {
            "passport_validity": "Valid for at least 3 months after intended departure date from the Schengen zone.",
            "visa_requirement": "Standard Schengen Visa (Short-stay type C) required for Indian passport holders.",
            "customs_advisory": "Duty-free allowance for non-EU travelers includes up to €430 of personal goods.",
            "currency_regulations": "Euro (€). Contactless card payment universal.",
            "official_portal_url": "https://france-visas.gouv.fr"
        },
        "regions": [
            {
                "name": "Île-de-France",
                "is_ut": False,
                "cities": [
                    {
                        "name": "Paris",
                        "lat": 48.8566,
                        "lon": 2.3522,
                        "budget": 18000,
                        "best": "Apr-Oct",
                        "vibe": "Artistic Monuments, Haute Cuisine & Romantic Lights",
                        "image_url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=800&auto=format&fit=crop&q=80",
                        "description": "The City of Light, world-renowned for the Eiffel Tower, the Louvre museum, sidewalk cafes, and Seine riverbanks.",
                        "pois": [
                            {"name": "Eiffel Tower & Champ de Mars", "cat": "Romantic", "duration": 150, "fee": 2800, "in_out": "Outdoor", "desc": "Global symbol of France offering 360-degree panoramic vistas of the Parisian skyline.", "image_url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=600&auto=format&fit=crop&q=80"},
                            {"name": "Louvre Museum Masterpieces Tour", "cat": "Heritage", "duration": 240, "fee": 2000, "in_out": "Indoor", "desc": "World's largest museum housing Mona Lisa, Venus de Milo, and Winged Victory of Samothrace.", "image_url": "https://images.unsplash.com/photo-1565099824688-e93eb20fe622?w=600&auto=format&fit=crop&q=80"},
                            {"name": "Seine River Evening Dinner Cruise", "cat": "Romantic", "duration": 150, "fee": 6500, "in_out": "Mixed", "desc": "Gourmet French three-course dinner cruising past illuminated monuments and bridges.", "image_url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=600&auto=format&fit=crop&q=80"},
                            {"name": "Montmartre & Sacré-Cœur Basilica Walk", "cat": "Sightseeing", "duration": 120, "fee": 0, "in_out": "Outdoor", "desc": "Historic bohemian artist quarter on the highest hill overlooking Paris.", "image_url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=600&auto=format&fit=crop&q=80"}
                        ],
                        "hotels": [
                            {"name": "Le Bristol Paris", "property_type": "Luxury Resort", "price_per_night_inr": 65000, "rating": 4.96, "review_count": 290, "location_area": "Rue du Faubourg Saint-Honoré", "distance_to_attraction": "1.5 km from Louvre", "amenities": ["3 Michelin-star Epicure", "Rooftop Pool", "Private French Garden"], "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=600&auto=format&fit=crop&q=80", "description": "Quintessential Parisian luxury palace hotel with classical 18th-century French refinement."},
                            {"name": "Hôtel Fabric Paris", "property_type": "Boutique Hotel", "price_per_night_inr": 16000, "rating": 4.85, "review_count": 340, "location_area": "Oberkampf", "distance_to_attraction": "2 km from Le Marais", "amenities": ["Boutique Design", "Honesty Bar", "Spa", "Free WiFi"], "image_url": "https://images.unsplash.com/photo-1590490360182-c33d57733427?w=600&auto=format&fit=crop&q=80", "description": "Former textile factory reimagined as a stylish boutique haven in trendy Oberkampf."}
                        ],
                        "restaurants": [
                            {"name": "Le Bouillon Chartier", "cuisine_type": "Classic French Bistro", "category": "Top Restaurant", "price_level": "$$", "avg_meal_cost_inr": 1800, "rating": 4.7, "review_count": 2100, "location_area": "Grands Boulevards", "popular_dishes": ["Boeuf Bourguignon", "Escargots", "Confit de Canard", "Profiteroles"], "dietary_tags": ["Traditional French"], "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600&auto=format&fit=crop&q=80", "description": "Historic 1896 Belle Époque dining hall offering authentic traditional French dining at accessible prices."}
                        ],
                        "videos": [
                            {"title": "Paris Travel Guide: Top 10 Things to Do", "duration_str": "6:45", "thumbnail_url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=600&auto=format&fit=crop&q=80", "video_url": "https://www.youtube.com/watch?v=sample_paris", "category": "City Guide"}
                        ]
                    }
                ]
            }
        ]
    },
    {
        "code": "JP",
        "name": "Japan",
        "continent": "Asia",
        "currency_code": "JPY",
        "timezone": "Asia/Tokyo",
        "hero_image": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=1200&auto=format&fit=crop&q=80",
        "visa_guidelines": "eVisa available online for eligible passport holders. Tourist visa available via VFS centers.",
        "requirement": {
            "passport_validity": "Valid for duration of intended stay.",
            "visa_requirement": "Japan eVisa or single/multiple entry tourist visa.",
            "customs_advisory": "Register on Visit Japan Web for smooth QR customs & immigration.",
            "currency_regulations": "Japanese Yen (¥). IC Cards (Suica/Pasmo) & cash widely used.",
            "official_portal_url": "https://www.mofa.go.jp/j_info/visit/visa/"
        },
        "regions": [
            {
                "name": "Kanto",
                "is_ut": False,
                "cities": [
                    {
                        "name": "Tokyo",
                        "lat": 35.6762,
                        "lon": 139.6503,
                        "budget": 15000,
                        "best": "Mar-May, Oct-Nov",
                        "vibe": "Cyberpunk Skylines, Shinto Shrines & Michelin Ramen",
                        "image_url": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=800&auto=format&fit=crop&q=80",
                        "description": "The world's most populous metropolis where ancient traditions blend seamlessly with cutting-edge robotics and culinary excellence.",
                        "pois": [
                            {"name": "Shibuya Crossing & Hachiko Monument", "cat": "Sightseeing", "duration": 60, "fee": 0, "in_out": "Outdoor", "desc": "World's busiest pedestrian scramble crossing and loyal dog Hachiko bronze memorial.", "image_url": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=600&auto=format&fit=crop&q=80"},
                            {"name": "Sensō-ji Temple & Asakusa Nakamise", "cat": "Heritage", "duration": 120, "fee": 0, "in_out": "Mixed", "desc": "Tokyo's oldest Buddhist temple founded in 645 AD with traditional sweet stalls.", "image_url": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=600&auto=format&fit=crop&q=80"},
                            {"name": "teamLab Planets Digital Art Immersion", "cat": "Sightseeing", "duration": 120, "fee": 2600, "in_out": "Indoor", "desc": "World-famous interactive body-immersive digital artwork where you walk through water and crystal gardens.", "image_url": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=600&auto=format&fit=crop&q=80"}
                        ],
                        "hotels": [
                            {"name": "Park Hyatt Tokyo", "property_type": "Luxury Resort", "price_per_night_inr": 48000, "rating": 4.93, "review_count": 310, "location_area": "Shinjuku", "distance_to_attraction": "1 km from Shinjuku Station", "amenities": ["New York Grill & Bar", "Club on the Park Spa", "Skyline Views of Mount Fuji"], "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=600&auto=format&fit=crop&q=80", "description": "High-altitude sanctuary atop the Shinjuku Park Tower with breathtaking views of Tokyo skyline and Mt. Fuji."}
                        ],
                        "restaurants": [
                            {"name": "Afuri Harajuku - Yuzu Ramen", "cuisine_type": "Japanese Ramen", "category": "Top Restaurant", "price_level": "$", "avg_meal_cost_inr": 850, "rating": 4.8, "review_count": 1400, "location_area": "Harajuku", "popular_dishes": ["Yuzu Shio Ramen", "Yuzu Ratanmen", "Pork Chashu Bowl"], "dietary_tags": ["Vegan Ramen Available"], "image_url": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=600&auto=format&fit=crop&q=80", "description": "Celebrated for refreshing citrus yuzu-infused dashi broth and charcoal-grilled chashu."}
                        ],
                        "videos": [
                            {"title": "Tokyo City Guide: Best Neighborhoods", "duration_str": "7:10", "thumbnail_url": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=600&auto=format&fit=crop&q=80", "video_url": "https://www.youtube.com/watch?v=sample_tokyo", "category": "City Guide"}
                        ]
                    }
                ]
            }
        ]
    },
    {
        "code": "AE",
        "name": "United Arab Emirates",
        "continent": "Middle East",
        "currency_code": "AED",
        "timezone": "Asia/Dubai",
        "hero_image": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=1200&auto=format&fit=crop&q=80",
        "visa_guidelines": "Pre-arranged 30/60 day tourist visas easily obtained online; 14-day visa on arrival for Indian passport holders with valid US/UK/Schengen visas.",
        "requirement": {
            "passport_validity": "Minimum 6 months validity.",
            "visa_requirement": "Online tourist visa or Visa on Arrival for eligible passport/visa holders.",
            "customs_advisory": "Strict medication laws; carry doctor prescription for prescription drugs.",
            "currency_regulations": "UAE Dirham (AED). Cards and Apple Pay accepted everywhere.",
            "official_portal_url": "https://smartservices.icp.gov.ae"
        },
        "regions": [
            {
                "name": "Dubai",
                "is_ut": False,
                "cities": [
                    {
                        "name": "Dubai",
                        "lat": 25.2048,
                        "lon": 55.2708,
                        "budget": 16000,
                        "best": "Nov-Apr",
                        "vibe": "Futuristic Architecture, Desert Safaris & Luxury Shopping",
                        "image_url": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=800&auto=format&fit=crop&q=80",
                        "description": "Global hub of futuristic engineering, record-breaking skyscrapers, tranquil desert safaris, and gold souks.",
                        "pois": [
                            {"name": "Burj Khalifa 124th & 125th Floor Observation Deck", "cat": "Sightseeing", "duration": 120, "fee": 3800, "in_out": "Indoor", "desc": "World's tallest building soaring 828 meters above Downtown Dubai.", "image_url": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=600&auto=format&fit=crop&q=80"},
                            {"name": "Dubai Desert Safari with Dune Bashing & BBQ", "cat": "Adventure", "duration": 360, "fee": 4200, "in_out": "Outdoor", "desc": "4x4 red dune thrill drive, sandboarding, camel rides, and starlit Bedouin feast.", "image_url": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=600&auto=format&fit=crop&q=80"},
                            {"name": "Museum of the Future", "cat": "Sightseeing", "duration": 120, "fee": 3400, "in_out": "Indoor", "desc": "Torus-shaped architectural wonder showcasing futuristic innovation for 2071.", "image_url": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=600&auto=format&fit=crop&q=80"}
                        ],
                        "hotels": [
                            {"name": "Atlantis The Royal", "property_type": "Luxury Resort", "price_per_night_inr": 55000, "rating": 4.95, "review_count": 420, "location_area": "Palm Jumeirah", "distance_to_attraction": "Palm Crescent", "amenities": ["Cloud 22 Sky Pool", "Celebrity Chef Restaurants", "Aquaventure Waterpark"], "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=600&auto=format&fit=crop&q=80", "description": "Ultra-luxury experiential resort redefining modern luxury on Palm Jumeirah."}
                        ],
                        "restaurants": [
                            {"name": "Al Ustad Special Kabab", "cuisine_type": "Iranian & Middle Eastern", "category": "Top Restaurant", "price_level": "$", "avg_meal_cost_inr": 650, "rating": 4.8, "review_count": 1800, "location_area": "Al Fahidi Heritage District", "popular_dishes": ["Kabab Khas", "Joojeh Kabab", "Saffron Rice"], "dietary_tags": ["Halal"], "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600&auto=format&fit=crop&q=80", "description": "Historic 1978 family kabab house famed for marinated melt-in-mouth meats."}
                        ],
                        "videos": [
                            {"title": "Dubai Complete Travel Guide: 48 Hours", "duration_str": "5:50", "thumbnail_url": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=600&auto=format&fit=crop&q=80", "video_url": "https://www.youtube.com/watch?v=sample_dubai", "category": "City Guide"}
                        ]
                    }
                ]
            }
        ]
    },
    {
        "code": "ID",
        "name": "Indonesia",
        "continent": "Asia",
        "currency_code": "IDR",
        "timezone": "Asia/Makassar",
        "hero_image": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=1200&auto=format&fit=crop&q=80",
        "visa_guidelines": "Electronic Visa on Arrival (e-VOA) available online for 90+ nationalities for 30 days.",
        "requirement": {
            "passport_validity": "Minimum 6 months validity.",
            "visa_requirement": "30-day e-VOA available online with extension option.",
            "customs_advisory": "Complete online Electronic Customs Declaration (e-CD) before boarding.",
            "currency_regulations": "Indonesian Rupiah (IDR). QRIS and Visa/Mastercard accepted in tourist areas.",
            "official_portal_url": "https://molina.imigrasi.go.id"
        },
        "regions": [
            {
                "name": "Bali",
                "is_ut": False,
                "cities": [
                    {
                        "name": "Bali",
                        "lat": -8.4095,
                        "lon": 115.1889,
                        "budget": 7500,
                        "best": "Apr-Oct",
                        "vibe": "Emerald Rice Terraces, Hindu Water Temples & Surfing",
                        "image_url": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=800&auto=format&fit=crop&q=80",
                        "description": "Island of the Gods, celebrated for lush rainforest waterfalls, sacred cliffside temples, and holistic wellness retreats.",
                        "pois": [
                            {"name": "Uluwatu Temple & Sunset Kecak Fire Dance", "cat": "Romantic", "duration": 150, "fee": 1500, "in_out": "Outdoor", "desc": "Ancient sea temple perched 70m above crashing waves with dramatic sunset choir dance.", "image_url": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=600&auto=format&fit=crop&q=80"},
                            {"name": "Tegallalang Rice Terraces & Jungle Swing", "cat": "Nature", "duration": 120, "fee": 800, "in_out": "Outdoor", "desc": "UNESCO cascading green valley rice fields with high-flying jungle swings.", "image_url": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=600&auto=format&fit=crop&q=80"},
                            {"name": "Tirta Empul Holy Water Temple Purification", "cat": "Spiritual", "duration": 90, "fee": 400, "in_out": "Outdoor", "desc": "Sacred Balinese water temple where travelers participate in traditional melukat blessing.", "image_url": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=600&auto=format&fit=crop&q=80"}
                        ],
                        "hotels": [
                            {"name": "Four Seasons Resort Bali at Sayan", "property_type": "Luxury Resort", "price_per_night_inr": 42000, "rating": 4.96, "review_count": 390, "location_area": "Ubud Ayung River", "distance_to_attraction": "10m from Ayung River", "amenities": ["Lotus Pond Rooftop", "Riverfront Villas", "Sacred River Spa"], "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=600&auto=format&fit=crop&q=80", "description": "Architectural masterpiece surrounded by lush Ayung river valley rainforests."}
                        ],
                        "restaurants": [
                            {"name": "Locavore NXT Ubud", "cuisine_type": "Hyper-Local Balinese Contemporary", "category": "Fine Dining", "price_level": "$$$$", "avg_meal_cost_inr": 3500, "rating": 4.92, "review_count": 310, "location_area": "Ubud", "popular_dishes": ["Fermented Duck", "Heritage Rice Degustation", "Wild Forest Mushrooms"], "dietary_tags": ["Sustainable", "Locally Sourced"], "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600&auto=format&fit=crop&q=80", "description": "Internationally acclaimed culinary lab highlighting 100% Indonesian ingredients."}
                        ],
                        "videos": [
                            {"title": "Discover Bali: Secret Waterfalls & Temples", "duration_str": "6:05", "thumbnail_url": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=600&auto=format&fit=crop&q=80", "video_url": "https://www.youtube.com/watch?v=sample_bali", "category": "City Guide"}
                        ]
                    }
                ]
            }
        ]
    },
    {
        "code": "CH",
        "name": "Switzerland",
        "continent": "Europe",
        "currency_code": "CHF",
        "timezone": "Europe/Zurich",
        "hero_image": "https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?w=1200&auto=format&fit=crop&q=80",
        "visa_guidelines": "Schengen Visa required for Indian travelers. Valid for 90 days across 29 European countries.",
        "requirement": {
            "passport_validity": "Valid for 3 months beyond Schengen stay.",
            "visa_requirement": "Schengen Visa required. Swiss Travel Pass recommended for transit.",
            "customs_advisory": "Standard customs limits apply.",
            "currency_regulations": "Swiss Franc (CHF). Cards accepted everywhere.",
            "official_portal_url": "https://www.eda.admin.ch"
        },
        "regions": [
            {
                "name": "Bernese Oberland",
                "is_ut": False,
                "cities": [
                    {
                        "name": "Interlaken",
                        "lat": 46.6863,
                        "lon": 7.8632,
                        "budget": 24000,
                        "best": "Year-round",
                        "vibe": "Alpine Lakes, Glacier Peaks & Adventure Sports",
                        "image_url": "https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?w=800&auto=format&fit=crop&q=80",
                        "description": "Gateway to the Jungfrau region nestled between turquoise Lake Thun and Lake Brienz.",
                        "pois": [
                            {"name": "Jungfraujoch - Top of Europe Cogwheel Train", "cat": "Adventure", "duration": 360, "fee": 16000, "in_out": "Mixed", "desc": "High altitude ice palace and Aletsch Glacier overlook at 3,454m altitude.", "image_url": "https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?w=600&auto=format&fit=crop&q=80"},
                            {"name": "Lake Brienz Turquoise Steamboat Cruise", "cat": "Relaxation", "duration": 120, "fee": 3200, "in_out": "Outdoor", "desc": "Glacial water cruise past Giessbach waterfalls and wooden chalets.", "image_url": "https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?w=600&auto=format&fit=crop&q=80"}
                        ],
                        "hotels": [
                            {"name": "Victoria-Jungfrau Grand Hotel & Spa", "property_type": "Luxury Resort", "price_per_night_inr": 52000, "rating": 4.94, "review_count": 280, "location_area": "Höheweg", "distance_to_attraction": "Overlooking Jungfrau meadow", "amenities": ["Nescens Spa", "Indoor Pool", "Gourmet Dining"], "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=600&auto=format&fit=crop&q=80", "description": "Historic grand luxury hotel with direct views of the snow-capped Jungfrau massif."}
                        ],
                        "restaurants": [
                            {"name": "Restaurant Taverne at Hotel Interlaken", "cuisine_type": "Swiss Alpine Fondue & Raclette", "category": "Top Restaurant", "price_level": "$$$", "avg_meal_cost_inr": 3200, "rating": 4.8, "review_count": 420, "location_area": "Postgasse", "popular_dishes": ["Gruyere Cheese Fondue", "Alpine Rosti", "Zurcher Geschnetzeltes"], "dietary_tags": ["Vegetarian Options"], "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600&auto=format&fit=crop&q=80", "description": "Traditional Swiss culinary specialties served in a 14th-century historic tavern."}
                        ],
                        "videos": [
                            {"title": "Swiss Alps Magic: Interlaken & Jungfrau Guide", "duration_str": "6:15", "thumbnail_url": "https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?w=600&auto=format&fit=crop&q=80", "video_url": "https://www.youtube.com/watch?v=sample_swiss", "category": "City Guide"}
                        ]
                    }
                ]
            }
        ]
    }
]

LOCAL_GUIDES_DATA = [
    {
        "full_name": "Mahipal Singh Rathore",
        "city_name": "Jaipur",
        "country_name": "India",
        "experience_years": 12,
        "languages_spoken": ["English", "Hindi", "German"],
        "hourly_rate": 850,
        "services_offered": ["Amber Forts & Palaces", "Royal Rajput Dynasty Stories", "Textile & Gem Bazaar Walk"],
        "rating": 4.98,
        "review_count": 142,
        "specialization": "Rajput Architecture & Royal History",
        "bio": "Certified Rajasthan tourism guide with a lineage of royal storytellers. Unlocks private areas and photo vantage points.",
        "avatar_url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80"
    },
    {
        "full_name": "Aarav Sharma",
        "city_name": "New Delhi",
        "country_name": "India",
        "experience_years": 8,
        "languages_spoken": ["English", "Hindi", "French"],
        "hourly_rate": 750,
        "services_offered": ["Old Delhi Food Safari", "Mughal Architecture Walk", "Photography Assist"],
        "rating": 4.96,
        "review_count": 84,
        "specialization": "Mughal Architecture & Street Food History",
        "bio": "Certified Delhi Tourism guide with a master's in Medieval Indian History. Passionate about uncovering Old Delhi secrets.",
        "avatar_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80"
    },
    {
        "full_name": "Jean-Pierre Laurent",
        "city_name": "Paris",
        "country_name": "France",
        "experience_years": 10,
        "languages_spoken": ["English", "French", "Spanish"],
        "hourly_rate": 3200,
        "services_offered": ["Louvre Masterpieces", "Montmartre Secret Walk", "Wine & Cheese Tasting"],
        "rating": 4.95,
        "review_count": 112,
        "specialization": "Impressionist Art & French Gastronomy",
        "bio": "Art Historian and licensed national museum curator in Paris.",
        "avatar_url": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&auto=format&fit=crop&q=80"
    },
    {
        "full_name": "Kenji Sato",
        "city_name": "Tokyo",
        "country_name": "Japan",
        "experience_years": 9,
        "languages_spoken": ["English", "Japanese"],
        "hourly_rate": 2800,
        "services_offered": ["Asakusa & Shinto Rituals", "Akihabara Tech Safari", "Tsukiji Outer Market Food Tour"],
        "rating": 4.99,
        "review_count": 96,
        "specialization": "Tokyo Traditions & Hidden Ramen Spots",
        "bio": "Tokyo native with deep love for Edo culture and the underground culinary scene.",
        "avatar_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80"
    },
    {
        "full_name": "Wayan Sukadana",
        "city_name": "Bali",
        "country_name": "Indonesia",
        "experience_years": 11,
        "languages_spoken": ["English", "Indonesian", "Balinese"],
        "hourly_rate": 1200,
        "services_offered": ["Sacred Temple Rituals", "Hidden Jungle Waterfalls", "Mount Batur Sunrise Trek"],
        "rating": 4.97,
        "review_count": 165,
        "specialization": "Balinese Spirituality & Eco-Trekking",
        "bio": "Lifelong Ubud local offering safe, insightful journeys into Bali's spiritual soul.",
        "avatar_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80"
    }
]

LOCAL_EXPERIENCES_DATA = [
    {
        "title": "Jaipur Royal Hand-Block Printing & Blue Pottery Workshop",
        "category": "Craft & Workshop",
        "city_name": "Jaipur",
        "duration_hours": 3.0,
        "price_per_person": 1200,
        "currency": "INR",
        "max_group_size": 6,
        "meeting_point": "Amber Heritage Workshop Hub",
        "rating": 4.95,
        "review_count": 52,
        "description": "Learn 300-year-old natural dye block printing from master artisans and print your own custom silk scarf to take home.",
        "highlights": ["Hands-on Crafting", "Take-Home Custom Scarf", "Masala Chai & Snacks"]
    },
    {
        "title": "Old Delhi 4-Hour Sunset Street Food & Spice Safari",
        "category": "Culinary Tour",
        "city_name": "New Delhi",
        "duration_hours": 4.0,
        "price_per_person": 1499,
        "currency": "INR",
        "max_group_size": 8,
        "meeting_point": "Jama Masjid Gate 3",
        "rating": 4.98,
        "review_count": 140,
        "description": "Taste 12+ iconic delicacies including stuffed paranthas, slow-cooked kebabs, Daulat ki Chaat, and vintage Jalebis with safety-checked hygienic vendors.",
        "highlights": ["12+ Tastings Included", "Heritage Spice Market Rooftop Access", "Cycle Rickshaw Ride"]
    },
    {
        "title": "Montmartre Bohemian Artists & Pastry Stroll",
        "category": "Walking Tour",
        "city_name": "Paris",
        "duration_hours": 3.0,
        "price_per_person": 4800,
        "currency": "INR",
        "max_group_size": 10,
        "meeting_point": "Abbesses Metro Station",
        "rating": 4.94,
        "review_count": 89,
        "description": "Walk the cobblestone paths where Picasso and Van Gogh painted, ending with warm artisanal croissants and macaron tastings.",
        "highlights": ["Secret Windmills & Vineyards", "3 Gourmet Pastry Tastings", "Sacré-Cœur Sunset View"]
    }
]
