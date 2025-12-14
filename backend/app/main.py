from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.db.init_indexes import init_indexes

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init_indexes()

app.include_router(auth_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
