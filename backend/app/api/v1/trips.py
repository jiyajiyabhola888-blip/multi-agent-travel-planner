import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.trip import TripCreateRequest, TripResponse, AgentMessageSchema, ItineraryDaySchema, ActivityItemSchema
from app.models.trip import Trip, ItineraryDay, ItineraryActivity, AgentDebateLog
from app.models.destination import City, AttractionPOI
from app.agents.orchestrator import MultiAgentOrchestrator
from app.services.currency_service import CurrencyService

router = APIRouter(prefix="/trips", tags=["Trips & Multi-Agent Planning"])
orchestrator = MultiAgentOrchestrator()


@router.post("/generate", response_model=TripResponse)
def generate_trip_plan(req: TripCreateRequest, db: Session = Depends(get_db)):
    """Executes the full 15-agent debate, reality checks, budget allocation, and generates the golden smart itinerary."""
    context = req.model_dump()

    # 1. Fetch available POIs from database if destination matches
    dest_name = req.destination.split(",")[0].strip()
    matching_city = db.query(City).filter(City.name.ilike(f"%{dest_name}%")).first()
    pois_list = []
    if matching_city and matching_city.pois:
        pois_list = [
            {
                "name": p.name,
                "cat": p.category,
                "duration": p.avg_duration_minutes,
                "fee": p.entry_fee_inr,
                "in_out": p.indoor_outdoor,
                "desc": p.description,
            }
            for p in matching_city.pois
        ]

    # 2. Run 15-Agent Debate
    debate_results = orchestrator.run_debate(context)

    # 3. Generate Day-by-Day Smart Itinerary
    itinerary_days_raw = orchestrator.generate_smart_itinerary(context, pois_list)

    # 4. Calculate Budget Breakdown
    budget_agent_out = next((d for d in debate_results if d.agent_name == "Budget Agent"), None)
    breakdown = budget_agent_out.metadata.get("breakdown", {}) if budget_agent_out and budget_agent_out.metadata else {
        "stay": req.total_budget * 0.35,
        "transport": req.total_budget * 0.28,
        "food": req.total_budget * 0.17,
        "activities": req.total_budget * 0.12,
        "guide": req.total_budget * 0.04,
        "misc_emergency": req.total_budget * 0.04,
    }

    # 5. Persist Trip to Database
    try:
        start_d = datetime.date.fromisoformat(req.start_date)
        end_d = datetime.date.fromisoformat(req.end_date)
    except Exception:
        start_d = datetime.date.today()
        end_d = start_d + datetime.timedelta(days=req.num_days)

    new_trip = Trip(
        title=f"{req.trip_type} Trip to {req.destination}",
        trip_type=req.trip_type,
        start_location=req.start_location,
        destination=req.destination,
        start_date=start_d,
        end_date=end_d,
        num_days=req.num_days,
        num_travelers=req.num_travelers,
        total_budget=req.total_budget,
        currency=req.currency,
        travel_style=req.travel_style,
        travel_pace=req.travel_pace,
        interests=req.interests,
        food_preferences=req.food_preferences,
        accommodation_pref=req.accommodation_preference,
        transport_pref=req.transportation_preference,
        special_requirements=req.special_requirements,
        budget_breakdown=breakdown,
        readiness_score=8,
        status="planned"
    )
    db.add(new_trip)
    db.flush()

    # Save debate logs
    for round_idx, agent_out in enumerate(debate_results, start=1):
        log_entry = AgentDebateLog(
            trip_id=new_trip.id,
            round_number=round_idx,
            agent_name=agent_out.agent_name,
            agent_role=agent_out.agent_role,
            stance=agent_out.stance,
            message=agent_out.message,
            proposed_adjustment=", ".join(agent_out.proposed_adjustments) if agent_out.proposed_adjustments else None,
        )
        db.add(log_entry)

    # Save Days & Activities
    days_response = []
    for day_raw in itinerary_days_raw:
        try:
            day_d = datetime.date.fromisoformat(day_raw["date"])
        except Exception:
            day_d = start_d

        day_db = ItineraryDay(
            trip_id=new_trip.id,
            day_number=day_raw["day_number"],
            date=day_d,
            theme=day_raw["theme"],
            city_name=day_raw["city_name"],
            weather_summary=day_raw["weather_summary"],
            daily_budget_allocated=day_raw["daily_budget_allocated"],
            daily_cost_estimated=day_raw["daily_cost_estimated"],
        )
        db.add(day_db)
        db.flush()

        activities_resp = []
        for act_raw in day_raw["activities"]:
            act_db = ItineraryActivity(
                day_id=day_db.id,
                order_index=act_raw["order_index"],
                time_slot=act_raw["time_slot"],
                start_time=act_raw["start_time"],
                end_time=act_raw["end_time"],
                activity_name=act_raw["activity_name"],
                category=act_raw["category"],
                location_name=act_raw["location_name"],
                estimated_cost=act_raw["estimated_cost"],
                transit_time_from_prev_mins=act_raw["transit_time_from_prev_mins"],
                transit_mode=act_raw["transit_mode"],
                buffer_security_mins=act_raw["buffer_security_mins"],
                booking_required=act_raw["booking_required"],
                why_explanation=act_raw["why_explanation"],
                is_indoor=act_raw["is_indoor"],
            )
            db.add(act_db)
            activities_resp.append(ActivityItemSchema(**act_raw))

        day_dict = {**day_raw, "activities": activities_resp}
        days_response.append(ItineraryDaySchema(**day_dict))

    db.commit()
    db.refresh(new_trip)

    return TripResponse(
        id=new_trip.id,
        title=new_trip.title,
        trip_type=new_trip.trip_type,
        destination=new_trip.destination,
        start_location=new_trip.start_location,
        start_date=str(new_trip.start_date),
        end_date=str(new_trip.end_date),
        num_days=new_trip.num_days,
        num_travelers=new_trip.num_travelers,
        total_budget=new_trip.total_budget,
        currency=new_trip.currency,
        travel_style=new_trip.travel_style,
        travel_pace=new_trip.travel_pace,
        budget_breakdown=breakdown,
        readiness_score=new_trip.readiness_score,
        debate_log=[
            AgentMessageSchema(
                agent_name=d.agent_name,
                agent_role=d.agent_role,
                stance=d.stance,
                message=d.message,
                proposed_adjustments=d.proposed_adjustments,
                metadata=d.metadata
            )
            for d in debate_results
        ],
        itinerary_days=days_response,
        created_at=str(new_trip.created_at)
    )


@router.get("/{trip_id}", response_model=TripResponse)
def get_trip_by_id(trip_id: int, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail=f"Trip with ID {trip_id} not found.")

    days_resp = []
    for day in trip.days:
        acts = [
            ActivityItemSchema(
                id=f"act_{day.day_number}_{a.id}",
                order_index=a.order_index,
                time_slot=a.time_slot,
                start_time=a.start_time,
                end_time=a.end_time,
                activity_name=a.activity_name,
                category=a.category,
                location_name=a.location_name,
                estimated_cost=a.estimated_cost,
                transit_time_from_prev_mins=a.transit_time_from_prev_mins,
                transit_mode=a.transit_mode,
                buffer_security_mins=a.buffer_security_mins,
                booking_required=a.booking_required,
                why_explanation=a.why_explanation or "",
                is_indoor=a.is_indoor
            )
            for a in day.activities
        ]
        days_resp.append(
            ItineraryDaySchema(
                day_number=day.day_number,
                date=str(day.date),
                theme=day.theme,
                city_name=day.city_name,
                weather_summary=day.weather_summary,
                daily_budget_allocated=day.daily_budget_allocated,
                daily_cost_estimated=day.daily_cost_estimated,
                activities=acts
            )
        )

    debate_log_resp = [
        AgentMessageSchema(
            agent_name=log.agent_name,
            agent_role=log.agent_role,
            stance=log.stance,
            message=log.message,
            proposed_adjustments=[log.proposed_adjustment] if log.proposed_adjustment else [],
        )
        for log in trip.debate_logs
    ]

    return TripResponse(
        id=trip.id,
        title=trip.title,
        trip_type=trip.trip_type,
        destination=trip.destination,
        start_location=trip.start_location,
        start_date=str(trip.start_date),
        end_date=str(trip.end_date),
        num_days=trip.num_days,
        num_travelers=trip.num_travelers,
        total_budget=trip.total_budget,
        currency=trip.currency,
        travel_style=trip.travel_style,
        travel_pace=trip.travel_pace,
        budget_breakdown=trip.budget_breakdown or {},
        readiness_score=trip.readiness_score or 8,
        debate_log=debate_log_resp,
        itinerary_days=days_resp,
        created_at=str(trip.created_at)
    )
