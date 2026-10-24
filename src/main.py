from fastapi import FastAPI
from src.database.db import engine, Base
from src.routes import users, skills, exchanges, reviews

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SkillSwap API")

app.include_router(users.router)
app.include_router(skills.router)
app.include_router(exchanges.router)
app.include_router(reviews.router)

@app.get("/")
def root():
    return {"message": "Welcome to SkillSwap API!"}