# Multi-Agent Travel Planner

> **"Generate → Debate → Optimize → Simulate → Explain → Adapt"**

A production-style global multi-agent travel planning and management platform supporting India (all 28 states & 8 UTs) and international multi-country travel.

---

## Architecture Highlights
- **15 Specialized AI Agents**:
  1. Preference Agent
  2. Destination Agent
  3. Route Agent
  4. Budget Agent
  5. Stay Agent
  6. Food Agent
  7. Weather Agent
  8. Local Experience Agent
  9. Risk Agent
  10. Group Conflict Agent
  11. Booking/Service Agent
  12. Simulation Agent
  13. Recovery Agent
  14. Explainability Agent
  15. Judge Agent (Arbiter)
- **CareNest-Inspired Aesthetic**: Soft professional blue (`#2563EB`), baby pink accents (`#EC4899`), crisp rounded cards (`rounded-2xl` / `rounded-3xl`), soft ambient shadows, and clean modern typography.
- **Realistic Time Engine**: Computes door-to-door transit, entry queues, security buffers, and dining stops.
- **Smart Budget Engine**: 6-bucket breakdown with multi-currency support and tradeoff rebalancing levers.
- **What-If Trip Simulator & Trip Twin**: Side-by-side scenario modeling (Rain, Flight Delays, Budget Cut, Closed Attractions).
- **Live Trip Recovery**: Dynamic in-trip incident replanning for affected segments.
- **Local Guides & Experiences Marketplace**: Direct connections with verified local guides and hosts.

---

## Tech Stack
- **Frontend**: React 18 + TypeScript + Vite + Tailwind CSS + Lucide Icons + Framer Motion
- **Backend**: Python 3.11+ with FastAPI, Pydantic v2, and SQLAlchemy 2.0
- **Database**: SQLite (local development) / PostgreSQL (production ready)

---

## Running the Application

### 1. Backend
```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```
API Documentation will be available at: `http://localhost:8000/api/v1/docs`

### 2. Frontend
```bash
cd frontend
npm install
npm run dev
```
Frontend will be running at: `http://localhost:5173`

---

## Phase Roadmap
- [x] **Phase 1**: Project Scaffolding & Core Architecture Blueprint
- [ ] **Phase 2**: Database Models & Seed Data (India & Global)
- [ ] **Phase 3**: Core Backend REST APIs & Services
- [ ] **Phase 4**: 15-Agent Multi-Agent Engine & Debate Arena
- [ ] **Phase 5**: Realistic Time, Smart Budget & Route Optimization
- [ ] **Phase 6**: What-If Simulation, Trip Twin & Live Recovery Engine
- [ ] **Phase 7**: CareNest-Style Design System & Complete Landing Page
- [ ] **Phase 8**: 15-Step Trip Wizard & Destination Discovery
- [ ] **Phase 9**: Interactive Itinerary & Explainable AI View
- [ ] **Phase 10**: Local Guides, Experience Marketplace & Inspiration Import
- [ ] **Phase 11**: Simulation Twin, Live Mode, Recovery UI & User/Admin Dashboards
- [ ] **Phase 12**: End-to-End Testing, Polish & Verification
