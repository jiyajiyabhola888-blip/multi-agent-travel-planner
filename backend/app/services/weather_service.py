import random
from typing import Dict, Any


class WeatherService:
    @staticmethod
    def get_forecast(city_name: str, start_date_str: str, num_days: int) -> Dict[str, Any]:
        """Provides weather analysis and identifies indoor/outdoor suitability."""
        city_lower = city_name.lower()

        # Simulated intelligent seasonal patterns
        if "delhi" in city_lower or "jaipur" in city_lower or "agra" in city_lower:
            base_temp = 24
            condition = "Pleasant & Clear"
            rain_chance = 5
        elif "mumbai" in city_lower or "kochi" in city_lower or "goa" in city_lower:
            base_temp = 29
            condition = "Warm & Coastal Breeze"
            rain_chance = 15
        elif "manali" in city_lower or "gulmarg" in city_lower or "leh" in city_lower or "switzerland" in city_lower:
            base_temp = 8
            condition = "Cool Alpine Skies"
            rain_chance = 10
        elif "dubai" in city_lower:
            base_temp = 27
            condition = "Sunny & Warm"
            rain_chance = 0
        elif "paris" in city_lower or "london" in city_lower:
            base_temp = 16
            condition = "Mild with Occasional Drizzle"
            rain_chance = 35
        elif "tokyo" in city_lower:
            base_temp = 18
            condition = "Clear & Crisp"
            rain_chance = 20
        else:
            base_temp = 22
            condition = "Sunny & Moderate"
            rain_chance = 10

        daily_forecasts = []
        for i in range(num_days):
            temp_var = random.randint(-2, 2)
            day_rain = min(100, max(0, rain_chance + random.randint(-5, 10)))
            daily_forecasts.append({
                "day": i + 1,
                "temperature_celsius": base_temp + temp_var,
                "condition": condition if day_rain < 40 else "Light Passing Showers",
                "rain_probability_pct": day_rain,
                "outdoor_comfort": "Optimal" if day_rain < 30 else "Moderate / Carry Umbrella",
            })

        return {
            "city": city_name,
            "overall_summary": f"{condition}, {base_temp}°C average",
            "daily_forecasts": daily_forecasts,
            "indoor_backup_recommended": rain_chance > 40
        }
