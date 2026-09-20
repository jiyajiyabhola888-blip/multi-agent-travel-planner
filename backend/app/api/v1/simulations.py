from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.trip import Trip
from app.models.simulation import TripSimulation
from app.schemas.trip import SimulationRequest

router = APIRouter(prefix="/simulations", tags=["What-If Trip Simulator & Trip Twin"])


@router.post("/run")
def run_trip_simulation(req: SimulationRequest, db: Session = Depends(get_db)):
    """Simulates What-If scenarios and produces a side-by-side Trip Twin without destroying the original plan."""
    trip = db.query(Trip).filter(Trip.id == req.trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found.")

    scenario = req.scenario_type.lower()
    budget_delta = 0.0
    time_delta = 0
    modifications = []

    if "rain" in scenario:
        title = "What if it rains heavily?"
        impact = "Outdoor heritage monuments & lake boat rides replaced with world-class indoor museums, palace interiors, and cozy artisanal cafes."
        budget_delta = 0.0
        time_delta = -30
        modifications = [
            {"change": "Replaced outdoor walking tour with National Heritage Museum visit", "status": "Substituted"},
            {"change": "Moved evening boat ride to next dry morning", "status": "Rescheduled"},
            {"change": "Added indoor spice market & high tea stop", "status": "Added"}
        ]
    elif "delay" in scenario or "flight" in scenario:
        title = "What if my transit/flight is delayed by 3 hours?"
        impact = "Surgically shifted morning sightseeing to evening sunset promenade; check-in expedited with direct hotel transfer."
        budget_delta = 0.0
        time_delta = +180
        modifications = [
            {"change": "Compressed Day 1 morning sightseeing into sunset photo-walk", "status": "Rescheduled"},
            {"change": "Pre-notified hotel of late check-in", "status": "Automated"}
        ]
    elif "budget" in scenario:
        title = "What if total budget is reduced by 20%?"
        impact = "Optimized stay from 5-star luxury to boutique 4-star heritage homestay and swapped paid private cab with high-speed express metro."
        budget_delta = -round(trip.total_budget * 0.20, 2)
        time_delta = 0
        modifications = [
            {"change": "Adjusted accommodation tier to verified boutique heritage homestay (Saved 15%)", "status": "Optimized"},
            {"change": "Replaced paid museum guided tour with free historical audio trail", "status": "Substituted"}
        ]
    elif "closed" in scenario or "unavailable" in scenario:
        title = "What if primary attraction is closed?"
        impact = "Auto-swapped with top-rated neighboring royal palace within 1.5 km radius; preserved meal and transit schedule."
        budget_delta = +50.0
        time_delta = -15
        modifications = [
            {"change": "Substituted closed monument with adjacent historic gallery", "status": "Substituted"}
        ]
    else:
        title = "What if 1 traveler cancels?"
        impact = "Recalculated per-person dining & ticket expenses; converted double occupancy into single private suite."
        budget_delta = -round(trip.total_budget * 0.35, 2)
        time_delta = 0
        modifications = [
            {"change": "Reduced restaurant reservations and activity tickets by 1 head", "status": "Adjusted"}
        ]

    sim_record = TripSimulation(
        trip_id=trip.id,
        scenario_name=title,
        scenario_type=req.scenario_type,
        impact_summary=impact,
        budget_delta=budget_delta,
        time_delta_mins=time_delta,
        modified_itinerary_json={"modifications": modifications}
    )
    db.add(sim_record)
    db.commit()

    return {
        "simulation_id": sim_record.id,
        "trip_id": trip.id,
        "scenario_name": title,
        "scenario_type": req.scenario_type,
        "impact_summary": impact,
        "budget_delta": budget_delta,
        "new_estimated_total": trip.total_budget + budget_delta,
        "currency": trip.currency,
        "time_delta_mins": time_delta,
        "modifications": modifications,
        "twin_status": "Ready for Side-by-Side Comparison"
    }
