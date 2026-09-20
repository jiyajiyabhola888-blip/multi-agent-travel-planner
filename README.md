# 🌍 Multi-Agent Travel Planner

An AI-powered travel planning application that creates personalized trip plans based on a user's destination, budget, travel preferences, interests, food preferences, accommodation choices, transportation preferences, and trip type.

The project uses a **multi-agent architecture** where different AI agents handle different parts of the travel-planning process and a final planner combines their outputs into a complete itinerary.

---

## ✨ Key Features

- 🌍 Personalized travel planning
- 🤖 Multi-agent AI architecture
- 💰 Budget-aware trip planning
- 🏨 Accommodation recommendations
- 🚆 Transportation planning
- 📍 Destination and activity planning
- 🧭 Local experience / guide planning
- 📅 Day-wise itinerary generation
- ⚡ FastAPI backend
- 📚 Interactive Swagger API documentation
- 🖥️ Web frontend
- 🧪 API testing support

---

## 🎯 Problem

Planning a trip usually requires checking many different things separately:

- Where should I visit?
- What places should I explore?
- How much will the trip cost?
- Where should I stay?
- How should I travel?
- What activities match my interests?
- Can the complete plan fit my budget?

This can make travel planning time-consuming and difficult to personalize.

---

## 💡 Solution

The Multi-Agent Travel Planner brings these tasks together into one application.

The user provides their travel requirements, and the system processes them through multiple specialized agents. Each agent focuses on a specific planning area, and the final planner combines the results into a personalized travel itinerary.

---

# 🤖 Multi-Agent Architecture

```text
                         👤 USER
                           │
                           ▼
                 🖥️ Travel Planner UI
                           │
                           ▼
                    ⚡ FastAPI API
                           │
                           ▼
                🧠 Trip Planning System
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
   📍 Destination     💰 Budget       🏨 Accommodation
      Agent              Agent              Agent
          │                │                │
          └────────────────┼────────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
   🚆 Transportation   🧭 Local          📅 Trip/
        Agent         Experience Agent    Planning Agent
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                  🧠 Final Planner
                           │
                           ▼
                 📋 Complete Itinerary
                           │
                           ▼
                  👤 User Dashboard
🔄 Complete Workflow
👤 User
   │
   │ Enter trip requirements
   ▼
📝 Trip Request
   │
   ├── Trip Type
   ├── Destination
   ├── Number of Travelers
   ├── Dates
   ├── Budget
   ├── Travel Style
   ├── Interests
   ├── Food Preference
   ├── Accommodation
   └── Transportation
   │
   ▼
⚡ FastAPI Backend
   │
   ▼
🤖 Multi-Agent Travel System
   │
   ├── 📍 Destination Planning
   ├── 💰 Budget Planning
   ├── 🏨 Accommodation Planning
   ├── 🚆 Transportation Planning
   └── 🧭 Local Experience Planning
   │
   ▼
🧠 Final Planner
   │
   ▼
📋 Personalized Itinerary
   │
   ▼
🖥️ Frontend
   │
   ▼
👤 User
🧠 AI Agents
📍 Destination Agent

Handles destination-related planning and activities according to the trip requirements.

💰 Budget Agent

Considers the user's available budget while preparing the trip plan.

🏨 Accommodation Agent

Handles accommodation-related planning according to the user's preferences.

🚆 Transportation Agent

Considers transportation preferences for the journey.

🧭 Local Experience Agent

Focuses on local experiences, activities, and guide/local-travel experiences.

📅 Trip Planning / Final Planner

Combines the information from the different planning components and generates the final itinerary.

🛠️ Tech Stack
Backend
Python
FastAPI
Pydantic
REST APIs
AI / LLM integration
Frontend
HTML
CSS
JavaScript
Development Tools
Git
GitHub
VS Code
Swagger / OpenAPI
📁 Project Structure
multi-agent-travel-planner/
│
├── backend/
│   ├── agents/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── services/
│   ├── tests/
│   ├── .env.example
│   └── ...
│
├── frontend/
│   ├── ...
│   └── ...
│
├── .gitignore
├── README.md
└── ...

The exact files and folders may change as the project continues to be developed.

🔌 API

The backend exposes REST APIs through FastAPI.

Generate a Trip
POST /api/v1/trips/generate

This endpoint accepts the user's travel requirements and generates a travel plan.

Get a Trip
GET /api/v1/trips/{trip_id}

This endpoint retrieves a generated trip using its trip ID.

API Documentation

FastAPI provides interactive API documentation at:

/api/v1/docs

You can use Swagger UI to test the backend APIs directly from the browser.

🧪 Testing

The backend has been tested through the FastAPI API documentation and endpoints.

Current API testing includes:

POST /api/v1/trips/generate
        ↓
Generate Trip
        ↓
Receive API Response
        ↓
GET /api/v1/trips/{trip_id}
        ↓
Retrieve Generated Trip

A successful API response uses HTTP status:

200 OK
⚙️ Local Setup
1. Clone the repository
git clone https://github.com/jiyajiyabhola888-blip/multi-agent-travel-planner.git
2. Open the project
cd multi-agent-travel-planner
3. Create and activate a virtual environment
Windows
python -m venv venv
venv\Scripts\activate
4. Install backend dependencies
cd backend
pip install -r requirements.txt
5. Configure environment variables

Create a .env file inside the backend directory and add the required API configuration.

Use .env.example as the reference.

Never upload API keys or other secrets to GitHub.

6. Start the backend

Use the project's configured FastAPI startup command.

For a standard FastAPI/Uvicorn setup:

uvicorn main:app --reload

If the project's entry file is different, use the startup command defined in the backend.

🖥️ Frontend

The frontend is maintained separately from the backend.

The basic application flow is:

Frontend
   │
   ▼
User enters travel requirements
   │
   ▼
Frontend sends API request
   │
   ▼
FastAPI Backend
   │
   ▼
Multi-Agent System
   │
   ▼
Generated Trip
   │
   ▼
Frontend displays itinerary
📊 Example Trip Request

Example:

Trip Type: Family
From: Delhi
To: Jaipur

Dates:
15 October 2026 → 20 October 2026

Travelers: 2
Budget: ₹50,000

Travel Style: Balanced

Interests:
- Heritage
- Photography
- Food

Food Preference:
Vegetarian / Local Street Food

Accommodation:
Boutique / 4-Star

Transportation:
Private Cab / Train

The system uses these preferences as inputs while generating the travel plan.

🔐 Security

The project follows basic security practices during development:

API keys should be stored in environment variables.
.env files should not be committed to GitHub.
.env.example is provided as a configuration reference.
API input validation is handled through the backend.
Secrets should never be hardcoded into frontend code.
🚀 Current Project Status
✅ Currently Implemented
Travel planning application
FastAPI backend
Multi-agent planning architecture
Trip generation API
Trip retrieval API
Swagger/OpenAPI documentation
Frontend structure
Git/GitHub repository
Basic API testing
🔄 Planned / Future Improvements

The following features can be added in future development phases:

🔐 User signup/login
👤 User profiles
💾 Persistent database
🧠 Long-term user preferences
📚 Trip history
❤️ Saved trips
👍 User feedback and recommendation improvement
🎯 More advanced personalization
🌐 Production deployment
📱 Improved mobile experience
🗺️ Maps and location services
💳 Booking integrations
🧑‍🤝‍🧑 Local guide/traveler connections

These are planned improvements and are not represented as currently completed features.

🔮 Future Personalization Architecture
                👤 USER
                   │
                   ▼
          👤 User Preferences
                   │
                   ▼
             📝 Trip Request
                   │
                   ▼
             🤖 AI Agents
                   │
                   ▼
            📋 Travel Plan
                   │
          ┌────────┴────────┐
          ▼                 ▼
     💾 Save Trip       ❤️ Feedback
          │                 │
          └────────┬────────┘
                   ▼
             📚 Trip History
                   │
                   ▼
          🧠 Future Personalization
                   │
                   ▼
       More Relevant Trip Plans
🌟 Why This Project?

This project demonstrates practical concepts used in modern software and AI applications:

Multi-agent AI systems
Backend API development
Frontend-backend integration
API design
Input validation
AI-powered decision making
Modular software architecture
Git and GitHub workflow
Testing and documentation

The project is designed to grow from an initial working prototype into a more complete personalized travel platform.
