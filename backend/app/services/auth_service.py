from passlib.context import CryptContext
import hashlib

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    # Pre-hash password to avoid bcrypt 72-byte limit
    sha256_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return pwd_context.hash(sha256_hash)
