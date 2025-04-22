"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import EmailStr
import os
from pathlib import Path

# Initialize FastAPI app
app = FastAPI(
    title="Mergington High School API",
    description="API for viewing and signing up for extracurricular activities"
)

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(current_dir, "static")),
    name="static"
)

# In-memory activity database
activities = {
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
    """Redirect to the static index page."""
    return RedirectResponse(url="/static/index.html")

@app.get("/activities")
def get_activities():
    """Retrieve all available activities."""
    return activities

@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: EmailStr = Query(..., description="Student's email address")):
    """
    Sign up a student for an activity.
    Validates the activity, checks for duplicate registrations, and ensures the participant limit is not exceeded.
    """
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail=f"Activity '{activity_name}' not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Check if email is already registered
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail=f"Email '{email}' is already signed up for {activity_name}")

    # Check if max participants limit is reached
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail=f"{activity_name} has reached the maximum number of participants")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
