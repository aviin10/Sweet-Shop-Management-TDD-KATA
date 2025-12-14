from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.db.init_indexes import init_indexes
from app.routes.protected import router as protected_router
from app.routes.admin import router as admin_router
from app.routes.sweets import router as sweets_router

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init_indexes()

app.include_router(auth_router)
app.include_router(protected_router)
app.include_router(admin_router)
app.include_router(sweets_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
