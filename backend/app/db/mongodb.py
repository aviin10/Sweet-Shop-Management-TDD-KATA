from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv("MONGODB_URL")
DB_NAME = os.getenv("MONGODB_DB_NAME")

client = AsyncIOMotorClient(MONGO_URL, tlsAllowInvalidCertificates=True)
database = client[DB_NAME]

async def get_database():
    return database
