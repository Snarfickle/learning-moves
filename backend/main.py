from fastapi import FastAPI
from authenticator import authenticator
from routers import (
    profile,
    account,
    appointments,
    certificates,
    courses,
    materials,
    resources,
)

app = FastAPI()

@app.get("/")
def read_root():
    return{"Welcome!": "To the main file!"}

app.include_router(profile.router)
app.include_router(account.router)
app.include_router(appointments.router)
app.include_router(certificates.router)
app.include_router(courses.router)
app.include_router(materials.router)
app.include_router(resources.router)
app.include_router(authenticator.router)
