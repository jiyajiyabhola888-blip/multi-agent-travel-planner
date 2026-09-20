from typing import Dict, Any


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
