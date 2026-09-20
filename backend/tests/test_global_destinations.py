"""
Comprehensive Global Destination & Map Testing Suite
Validates:
1. All 21+ requested countries (China, India, Japan, France, USA, UK, Thailand, Australia, Canada, Italy, Germany, Singapore, Malaysia, Spain, Brazil, South Korea, Egypt, Turkey, Nepal, Bhutan, Maldives)
2. All requested cities (Beijing, Shanghai, Tokyo, Paris, London, New York, Dubai, Bangkok, Singapore, Sydney, Rome, Barcelona, Istanbul, Cairo, Seoul, Kathmandu, Male, Jaipur)
3. Canonical structured autocomplete and search results schema
4. Map endpoint coverage across continents
5. Dynamic country hub resolution and dynamic city resolution
6. Strict 404 on invalid destinations (Zero silent fallback to first city)
7. Jaipur identity preservation (Jaipur must never return Udaipur)
"""

import sys
import os

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

COUNTRIES_TO_TEST = [
    "China", "India", "Japan", "France", "USA", "UK", "Thailand", 
    "Australia", "Canada", "Italy", "Germany", "Singapore", "Malaysia", 
    "Spain", "Brazil", "South Korea", "Egypt", "Turkey", "Nepal", "Bhutan", "Maldives"
]

CITIES_TO_TEST = [
    "Beijing", "Shanghai", "Tokyo", "Paris", "London", "New York", 
    "Dubai", "Bangkok", "Singapore", "Sydney", "Rome", "Barcelona", 
    "Istanbul", "Cairo", "Seoul", "Kathmandu", "Male", "Jaipur"
]

def test_health():
    print("\n--- 1. Testing Health Endpoint ---")
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.json()
    print(f"Health check OK: status={data.get('status')}, agents={data.get('agents_available')}")

def test_countries_autocomplete():
    print("\n--- 2. Testing Autocomplete for 21 Countries ---")
    failed = []
    for country in COUNTRIES_TO_TEST:
        res = client.get("/api/v1/destinations/autocomplete", params={"q": country})
        assert res.status_code == 200
        results = res.json()
        assert len(results) > 0, f"No autocomplete results for country: {country}"
        
        # Verify schema
        top = results[0]
        assert "title" in top and "type" in top and "canonical_value" in top
        print(f"  ✓ {country:15} -> {top['title']} [{top['type']}] ({top.get('canonical_value')})")
    print("All 21 countries autocomplete passed!")

def test_cities_autocomplete():
    print("\n--- 3. Testing Autocomplete for Global Cities ---")
    for city in CITIES_TO_TEST:
        res = client.get("/api/v1/destinations/autocomplete", params={"q": city})
        assert res.status_code == 200
        results = res.json()
        assert len(results) > 0, f"No autocomplete results for city: {city}"
        top = results[0]
        print(f"  ✓ {city:15} -> {top['title']} [{top['type']}] ({top.get('canonical_value')})")
    print("All global cities autocomplete passed!")

def test_search_results():
    print("\n--- 4. Testing Global Search Endpoint ---")
    queries = ["China", "Paris", "Egypt", "Tokyo", "Maldives", "Jaipur"]
    for q in queries:
        res = client.get("/api/v1/destinations/search", params={"query": q})
        assert res.status_code == 200
        results = res.json()
        assert len(results) > 0, f"Search returned 0 results for '{q}'"
        print(f"  ✓ Search '{q}' -> {len(results)} items found (Top: {results[0]['title']} [{results[0]['type']}])")

def test_map_destinations():
    print("\n--- 5. Testing Map Endpoint Coverage ---")
    res = client.get("/api/v1/destinations/map")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 15, f"Expected at least 15 map hubs, got {len(data)}"
    
    continents = {item.get('continent') for item in data if item.get('continent')}
    print(f"  ✓ Map contains {len(data)} global hubs across continents: {continents}")
    for item in data[:5]:
        print(f"    • {item['city']}, {item['country']} ({item['latitude']}, {item['longitude']}) - ₹{item['avg_daily_budget_inr']}/day")

def test_destination_detail_resolution():
    print("\n--- 6. Testing Destination Resolution & Detail Generation ---")
    
    # Test Local DB city (Jaipur)
    res_jaipur = client.get("/api/v1/destinations/jaipur")
    assert res_jaipur.status_code == 200
    jaipur_data = res_jaipur.json()
    assert "Jaipur" in jaipur_data["name"]
    assert "Udaipur" not in jaipur_data["name"]
    assert len(jaipur_data["attractions"]) > 0
    assert len(jaipur_data["stays"]) > 0
    print(f"  ✓ Jaipur (Local DB): Name={jaipur_data['name']}, Stays={len(jaipur_data['stays'])}, Attractions={len(jaipur_data['attractions'])}")

    # Test Global Country (China)
    res_china = client.get("/api/v1/destinations/china")
    assert res_china.status_code == 200
    china_data = res_china.json()
    assert "China" in china_data["name"] or china_data["country_name"] == "China"
    assert len(china_data["attractions"]) > 0
    assert china_data["travel_requirement"] is not None
    print(f"  ✓ China (Global Country): Name={china_data['name']}, Attractions={len(china_data['attractions'])}, Visa={china_data['travel_requirement']['visa_requirement'][:40]}...")

    # Test Global City (Beijing)
    res_beijing = client.get("/api/v1/destinations/beijing")
    assert res_beijing.status_code == 200
    beijing_data = res_beijing.json()
    assert "Beijing" in beijing_data["name"]
    assert len(beijing_data["attractions"]) > 0
    print(f"  ✓ Beijing (Global City): Name={beijing_data['name']}, Country={beijing_data['country_name']}, Attractions={len(beijing_data['attractions'])}")

    # Test Global Country (Australia)
    res_aus = client.get("/api/v1/destinations/australia")
    assert res_aus.status_code == 200
    aus_data = res_aus.json()
    assert "Australia" in aus_data["name"]
    print(f"  ✓ Australia (Global Country): Name={aus_data['name']}, Season={aus_data['best_months']}")

    # Test Canonical ID resolution endpoint
    res_canon = client.get("/api/v1/destinations/resolve/country:eg")
    assert res_canon.status_code == 200
    egypt_data = res_canon.json()
    assert "Egypt" in egypt_data["name"]
    print(f"  ✓ Resolve 'country:eg': Name={egypt_data['name']}")

def test_invalid_destination_404():
    print("\n--- 7. Testing Strict 404 on Invalid Destination ---")
    res = client.get("/api/v1/destinations/non_existent_destination_xyz_12345")
    assert res.status_code == 404, f"Expected 404 for invalid destination, got {res.status_code}"
    print("  ✓ Correctly returned 404 for non-existent destination (Zero silent fallback to first city)")

if __name__ == "__main__":
    test_health()
    test_countries_autocomplete()
    test_cities_autocomplete()
    test_search_results()
    test_map_destinations()
    test_destination_detail_resolution()
    test_invalid_destination_404()
    print("\n========================================================")
    print(" ALL 7 TEST SUITES PASSED WITH 100% SUCCESS!")
    print("========================================================\n")
