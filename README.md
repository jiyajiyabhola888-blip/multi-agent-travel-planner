# Multi-Agent Travel Planner

An AI-powered travel planning application that creates personalized travel plans based on user requirements such as destination, budget, travel dates, interests, food preferences, accommodation, transportation, and trip type.

The project uses a Multi-Agent AI architecture where different agents handle different parts of travel planning and combine their results to generate a complete travel itinerary.

---

## **Features**

- Personalized travel planning
- Multi-Agent AI architecture
- Destination planning
- Budget planning
- Accommodation planning
- Transportation planning
- Local experience planning
- Day-wise itinerary generation
- FastAPI backend
- Swagger API documentation
- Web frontend
- API testing

---

## **Problem**

Planning a trip usually requires checking multiple things separately.

Users need to decide where to go, what places to visit, how much to spend, where to stay, how to travel, and which activities match their interests.

Managing all these requirements manually can be time-consuming and difficult to personalize.

---

## **Solution**

The Multi-Agent Travel Planner brings these travel-planning tasks together into one application.

The user provides their travel requirements, and the system processes them through multiple specialized AI agents.

Each agent focuses on a specific part of the planning process, and the final planner combines the results to generate a personalized travel itinerary.

---

## **How It Works**

**1. User Input**

The user enters travel details such as:

- Trip type
- Starting location
- Destination
- Number of travelers
- Travel dates
- Budget
- Travel style
- Interests
- Food preferences
- Accommodation preference
- Transportation preference

**2. Backend Processing**

The request is sent to the FastAPI backend.

**3. Multi-Agent Processing**

Different AI agents process different parts of the travel request.

**4. Final Planning**

The outputs from the agents are combined by the final planner.

**5. Travel Itinerary**

The system generates a complete personalized travel plan for the user.

---

## **Multi-Agent System**

**Destination Agent**

Handles destination-related planning and suggests places and activities according to the trip requirements.

**Budget Agent**

Considers the user's available budget while preparing the travel plan.

**Accommodation Agent**

Handles accommodation planning according to the user's preferences.

**Transportation Agent**

Considers transportation preferences for the journey.

**Local Experience Agent**

Focuses on local experiences, activities, and local guide/traveler experiences.

**Final Planner**

Combines the outputs from the different planning agents and generates the final travel itinerary.

---

## **Technology Stack**

**Backend**

Python  
FastAPI  
Pydantic  
REST APIs  
AI / LLM Integration

**Frontend**

HTML  
CSS  
JavaScript

**Development Tools**

Git  
GitHub  
VS Code  
Swagger / OpenAPI

---

## **Project Structure**

```text
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
API Endpoints

Generate Trip

POST /api/v1/trips/generate

Generates a travel plan based on the user's trip requirements.

Get Trip

GET /api/v1/trips/{trip_id}

Retrieves a generated trip using its trip ID.

Swagger Documentation

/api/v1/docs

FastAPI provides interactive API documentation where the backend APIs can be tested.

Example Trip Request

Trip Type: Family

From: Delhi

To: Jaipur

Dates: 15 October 2026 to 20 October 2026

Travelers: 2

Budget: ₹50,000

Travel Style: Balanced

Interests: Heritage, Photography, Food

Food Preference: Vegetarian / Local Street Food

Accommodation: Boutique / 4-Star

Transportation: Private Cab / Train

Testing

The backend APIs have been tested using FastAPI Swagger documentation.

The main testing flow is:

POST /api/v1/trips/generate
        ↓
Generate Travel Plan
        ↓
200 OK
        ↓
GET /api/v1/trips/{trip_id}
        ↓
Retrieve Generated Trip

The trip generation and trip retrieval endpoints have been tested successfully during development.

Local Setup

1. Clone the Repository

git clone https://github.com/jiyajiyabhola888-blip/multi-agent-travel-planner.git

2. Open the Project

cd multi-agent-travel-planner

3. Create Virtual Environment

For Windows:

python -m venv venv

Activate the environment:

venv\Scripts\activate

4. Install Dependencies

cd backend
pip install -r requirements.txt

5. Configure Environment Variables

Create a .env file inside the backend directory.

Use .env.example as a reference.

Do not upload API keys or other secrets to GitHub.

6. Run the Backend

uvicorn main:app --reload

Open the API documentation:

http://127.0.0.1:8000/api/v1/docs
Application Flow
User
  ↓
Travel Planner Frontend
  ↓
Trip Requirements
  ↓
FastAPI Backend
  ↓
Multi-Agent Travel System
  ↓
Destination Agent
Budget Agent
Accommodation Agent
Transportation Agent
Local Experience Agent
  ↓
Final Planner
  ↓
Personalized Travel Itinerary
  ↓
Frontend
  ↓
User
Security

The project follows basic security practices during development.

API keys should be stored in environment variables.
.env files should not be uploaded to GitHub.
.env.example is provided as a configuration reference.
Backend input validation is used for API requests.
Secrets should never be hardcoded into frontend code.
Current Project Status

Currently Implemented

Travel planning application
FastAPI backend
Multi-Agent architecture
Trip generation API
Trip retrieval API
Swagger/OpenAPI documentation
Frontend structure
GitHub repository
API testing

Future Improvements

User signup and login
User profiles
Persistent database
User preference memory
Trip history
Saved trips
User feedback system
Advanced personalization
Production deployment
Improved mobile experience
Maps and location services
Booking integrations
Local guide/traveler connections

These features are planned for future development and are not presented as currently completed features.

Future Personalization

The future version of the application can remember user preferences, previous trips, and feedback.

This can allow the system to create more personalized travel plans over time.

The future personalization flow can be:

User
  ↓
User Preferences
  ↓
New Trip Request
  ↓
AI Agents
  ↓
Travel Plan
  ↓
Save Trip / Feedback
  ↓
Trip History
  ↓
Personalization
  ↓
Future Travel Plans
Why This Project?

This project demonstrates practical concepts used in modern AI and software development.

Multi-Agent AI systems
Backend API development
Frontend-backend integration
REST API design
Input validation
AI-powered planning
Modular architecture
Git and GitHub
API testing
Technical documentation
