from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    assert res.json()["agents_available"] == 15
    assert res.json()["brand"] == "WORLD TRAVELHOLIC"


def test_currency_conversion():
    res = client.get("/api/v1/currency/convert?amount=1000&from_curr=INR&to_curr=USD")
    assert res.status_code == 200
    data = res.json()
    assert data["converted_amount"] > 0
    assert data["to_currency"] == "USD"


def test_destinations_autocomplete():
    res = client.get("/api/v1/destinations/autocomplete?q=Jaip")
    assert res.status_code == 200
    data = res.json()
    assert len(data) > 0
    assert any("Jaipur" in item["title"] for item in data)

    res_par = client.get("/api/v1/destinations/autocomplete?q=Par")
    assert res_par.status_code == 200
    assert any("Paris" in item["title"] for item in res_par.json())


def test_destination_detail():
    res = client.get("/api/v1/destinations/Jaipur")
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "Jaipur"
    assert len(data["attractions"]) >= 3
    assert len(data["stays"]) >= 1
    assert len(data["restaurants"]) >= 1


def test_trip_generation_canonical_jaipur():
    """Verifies that selecting Jaipur strictly keeps destination as Jaipur."""
    payload = {
        "trip_type": "Family",
        "start_location": "Delhi, India",
        "destination": "Jaipur, Rajasthan, India",
        "start_date": "2026-10-15",
        "end_date": "2026-10-20",
        "num_days": 5,
        "num_travelers": 3,
        "total_budget": 55000,
        "currency": "INR",
        "travel_style": "Balanced",
        "travel_pace": "Balanced",
        "interests": ["Heritage & Palaces", "Street Food Crawls"],
        "food_preferences": ["Vegetarian", "Local Street Food"],
        "accommodation_preference": "Boutique Hotel / 4-Star",
        "transportation_preference": "Private Cab & Chauffeur"
    }
    res = client.post("/api/v1/trips/generate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "Jaipur" in data["destination"]
    assert "Udaipur" not in data["destination"]
    assert len(data["debate_log"]) >= 14
    assert len(data["itinerary_days"]) == 5

    # Check that day themes are unique and not repeating
    themes = [day["theme"] for day in data["itinerary_days"]]
    assert len(set(themes)) == len(themes), f"Duplicate day themes found: {themes}"

    # Test What-If simulation on created trip
    trip_id = data["id"]
    sim_res = client.post("/api/v1/simulations/run", json={"trip_id": trip_id, "scenario_type": "rain"})
    assert sim_res.status_code == 200
    assert "What if it rains" in sim_res.json()["scenario_name"]

    # Test Live Recovery
    recov_res = client.post("/api/v1/recovery/replan", json={"trip_id": trip_id, "incident_type": "cancelled_train"})
    assert recov_res.status_code == 200
    assert recov_res.json()["recovery_status"] == "Surgically Resolved"


def test_booking_and_sandbox_payment():
    booking_payload = {
        "booking_type": "Hotel",
        "title": "Samode Haveli Boutique Palace",
        "destination_name": "Jaipur, Rajasthan, India",
        "start_date": "2026-10-15",
        "end_date": "2026-10-18",
        "guests_count": 2,
        "amount": 19000,
        "currency": "INR"
    }
    b_res = client.post("/api/v1/bookings/create", json=booking_payload)
    assert b_res.status_code == 200
    b_data = b_res.json()
    assert b_data["success"] is True
    booking_id = b_data["booking_id"]

    # Execute sandbox checkout
    pay_res = client.post("/api/v1/payments/checkout", json={"booking_id": booking_id, "payment_method": "Sandbox Card"})
    assert pay_res.status_code == 200
    pay_data = pay_res.json()
    assert pay_data["success"] is True
    assert "WT-TXN-" in pay_data["transaction_id"]


def test_wander_ai_chat():
    res = client.post("/api/v1/chat/ask", json={"message": "What should I do in Jaipur?"})
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert "Jaipur" in data["reply"]
    assert len(data["actions"]) >= 1


def test_wishlist_and_notifications():
    # Toggle wishlist
    w_res = client.post("/api/v1/wishlist/toggle", json={
        "item_type": "destination",
        "item_id": "jaipur_city",
        "title": "Jaipur, Rajasthan, India",
        "location": "India",
        "rating": 4.9
    })
    assert w_res.status_code == 200

    # Get notifications
    n_res = client.get("/api/v1/notifications/")
    assert n_res.status_code == 200
    assert isinstance(n_res.json(), list)
