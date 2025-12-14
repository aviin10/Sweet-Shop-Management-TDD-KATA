from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health_check():
    """
    Basic health check endpoint.
    """
    return {"status": "ok"}
