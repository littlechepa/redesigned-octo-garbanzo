"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path
from pydantic import BaseModel

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Soccer Club": {
        "description": "Soccer training and friendly matches",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["lucas@mergington.edu"]
        },
    "Volleyball Club": {
        "description": "Volleyball practice and intramural competitions",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 14,
        "participants": ["sarah@mergington.edu"]
    },
    "Drama Club": {
        "description": "Theater productions and acting workshops",
        "schedule": "Wednesdays and Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["maya@mergington.edu", "jacob@mergington.edu"]
    },
    "Photography Club": {
        "description": "Digital and film photography techniques and projects",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["elena@mergington.edu"]
    },
    "Math Club": {
        "description": "Advanced problem solving and math competitions",
        "schedule": "Mondays and Fridays, 3:30 PM - 4:30 PM",
        "max_participants": 18,
        "participants": ["ryan@mergington.edu", "zoe@mergington.edu"]
    },
    "Model United Nations": {
        "description": "International diplomacy simulations and conferences",
        "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["andrew@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Team basketball practice and games",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["james@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Tennis training and tournament participation",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 10,
        "participants": ["alex@mergington.edu"]
    },
    "Art Club": {
        "description": "Painting, drawing, and visual arts exploration",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
    },
    "Music Ensemble": {
        "description": "Band and orchestra performance group",
        "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["noah@mergington.edu"]
    },
    "Debate Club": {
        "description": "Competitive debate and public speaking",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["ava@mergington.edu", "ethan@mergington.edu"]
    },
    "Science Club": {
        "description": "Hands-on science experiments and research projects",
        "schedule": "Tuesdays, 3:30 PM - 4:45 PM",
        "max_participants": 20,
        "participants": ["mia@mergington.edu"]
    },
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]
    
    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")

    # Add student
    activity["participants"].append(email)

    return {"message": f"Signed up {email} for {activity_name}"}


# Request model for unregistering
class UnregisterRequest(BaseModel):
    name: str
    activity: str

# Unregister a participant from an activity
@app.post("/unregister")
async def unregister_participant(req: UnregisterRequest):
    activity_name = req.activity
    name = req.name
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    if name not in activities[activity_name]["participants"]:
        raise HTTPException(status_code=404, detail="Participant not found in this activity")
    activities[activity_name]["participants"].remove(name)
    return {"message": f"{name} unregistered from {activity_name}"}
