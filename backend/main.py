from fastapi import FastAPI
from routers import (
    profile,
    account,
)

app = FastAPI()

@app.get("/")
def read_root():
    return{"Welcome!": "To the main file!"}

app.include_router(profile.router)
app.include_router(account.router)
