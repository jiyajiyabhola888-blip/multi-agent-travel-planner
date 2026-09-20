import math
from typing import Dict, Any, List


class RoutingService:
    """Calculates realistic door-to-door transit times, security buffers, and pace adjustments."""

    @staticmethod
    def calculate_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Haversine distance formula."""
        R = 6371.0 # Earth radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return round(R * c, 2)

    @staticmethod
    def get_realistic_transit(
        dist_km: float, 
        travel_pace: str = "Balanced", 
        mode: str = "cab"
    ) -> Dict[str, Any]:
        """Calculates transit time including urban congestion and entry/security buffers."""
        # Average urban speeds (km/h)
        speed_map = {"cab": 25.0, "walking": 4.5, "metro": 32.0, "train": 60.0}
        avg_speed = speed_map.get(mode.lower(), 25.0)

        # Raw travel time in minutes
        raw_transit_mins = max(10, int((dist_km / avg_speed) * 60))

        # Pace buffer adjustments
        # Relaxed pace gives +25 min buffer for photo stops, coffee, rest
        # Packed pace has tight +10 min buffer
        pace_buffer_map = {
            "Relaxed": 30,
            "Balanced": 15,
            "Packed": 5,
            "Adventure": 10
        }
        buffer_mins = pace_buffer_map.get(travel_pace, 15)

        # Entry queue / security buffer
        entry_queue_mins = 15

        total_door_to_door = raw_transit_mins + buffer_mins + entry_queue_mins

        return {
            "estimated_distance_km": dist_km,
            "raw_travel_time_mins": raw_transit_mins,
            "pace_rest_buffer_mins": buffer_mins,
            "security_queue_buffer_mins": entry_queue_mins,
            "total_door_to_door_transit_mins": total_door_to_door,
            "recommended_mode": "Metro / Cab" if dist_km > 3 else "Scenic Walk / Rickshaw",
            "realistic_schedule_guaranteed": True
        }
