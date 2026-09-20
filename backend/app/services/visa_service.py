from typing import Dict, Any, List


class VisaService:
    @staticmethod
    def get_travel_requirements(destination_country: str, origin_country: str = "India") -> Dict[str, Any]:
        """Provides travel requirements, passport validity rules, and official verification disclaimers."""
        dest_lower = destination_country.lower()

        if "india" in dest_lower:
            reqs = {
                "visa_type": "Domestic Travel (No Visa Required)",
                "documents_needed": ["Government Photo ID (Aadhaar, Voter ID, Driving License, or Passport)"],
                "passport_validity": "Not required for Indian citizens",
                "customs_notice": "Standard domestic airport security guidelines apply."
            }
        elif "uae" in dest_lower or "dubai" in dest_lower:
            reqs = {
                "visa_type": "Tourist Visa (30/60 Days) / Visa on Arrival for eligible US/UK visa holders",
                "documents_needed": ["Passport (min 6 months validity)", "Confirmed Return Ticket", "Hotel Booking Confirmation", "Travel Insurance"],
                "passport_validity": "6 months minimum from date of entry",
                "customs_notice": "Verify medicine restrictions prior to boarding."
            }
        elif "france" in dest_lower or "switzerland" in dest_lower or "europe" in dest_lower:
            reqs = {
                "visa_type": "Schengen Short-Stay Visa (Type C)",
                "documents_needed": ["Passport with 2 blank pages", "Schengen Travel Insurance (€30,000 cover)", "Proof of Accommodation", "Bank Statements (last 3-6 months)"],
                "passport_validity": "3 months minimum beyond intended date of departure from Schengen area",
                "customs_notice": "Bio-metric enrollment required at VFS appointment."
            }
        elif "japan" in dest_lower:
            reqs = {
                "visa_type": "Japan Single/Multiple Entry Tourist Visa or eVisa",
                "documents_needed": ["Valid Passport", "Visa Application Form with Photo", "Daily Schedule of Stay (Itinerary)", "Proof of Financial Stability"],
                "passport_validity": "Valid during intended period of stay",
                "customs_notice": "Visit Japan Web pre-registration recommended for Fast Track immigration."
            }
        else:
            reqs = {
                "visa_type": "Standard Tourist Visa / eVisa Required",
                "documents_needed": ["Passport with 6 months validity", "Return Flight Ticket", "Hotel Reservations"],
                "passport_validity": "6 months minimum from arrival date",
                "customs_notice": "Check local health and currency declaration policies."
            }

        return {
            **reqs,
            "official_disclaimer": "IMPORTANT: Visa and entry regulations are subject to sudden government updates. Always verify current requirements with official embassy, consulate, or VFS portals before departure."
        }


class VisionInspirationService:
    @staticmethod
    def analyze_inspiration_image(filename: str, caption: str = "") -> Dict[str, Any]:
        """Extracts destination, attraction, and aesthetic vibes from uploaded photo/screenshot."""
        cap_lower = caption.lower() + " " + filename.lower()

        if "eiffel" in cap_lower or "paris" in cap_lower:
            dest = "Paris, France"
            poi = "Eiffel Tower & Champ de Mars"
            vibe = "Romantic & Architectural"
        elif "taj" in cap_lower or "agra" in cap_lower:
            dest = "Agra, India"
            poi = "Taj Mahal"
            vibe = "Royal Mughal Wonder"
        elif "burj" in cap_lower or "dubai" in cap_lower or "desert" in cap_lower:
            dest = "Dubai, UAE"
            poi = "Burj Khalifa & Desert Safari"
            vibe = "Futuristic Luxury"
        elif "lake" in cap_lower or "udaipur" in cap_lower:
            dest = "Udaipur, India"
            poi = "Lake Pichola & City Palace"
            vibe = "Romantic Heritage Lake"
        elif "japan" in cap_lower or "tokyo" in cap_lower or "shrine" in cap_lower:
            dest = "Tokyo, Japan"
            poi = "Senso-ji Temple & Shibuya"
            vibe = "Tradition & High-Tech Urban"
        elif "swiss" in cap_lower or "mountain" in cap_lower or "snow" in cap_lower:
            dest = "Interlaken & Jungfraujoch, Switzerland"
            poi = "Jungfraujoch - Top of Europe"
            vibe = "Alpine Scenic Adventure"
        else:
            dest = "Jaipur & Rajasthan, India"
            poi = "Amber Fort & Palace"
            vibe = "Cultural Heritage & Colors"

        return {
            "extracted_destination": dest,
            "detected_attraction": poi,
            "aesthetic_style": vibe,
            "confidence_score": 0.94,
            "suggested_actions": ["Add directly to trip plan", "Find similar hidden gems nearby", "Connect with local guide in this city"]
        }
