from datetime import datetime, timedelta
import hashlib
from jose import jwt
from passlib.context import CryptContext
from config.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔐 HASH PASSWORD
def _pre_hash(password: str) -> str:
    """
    SHA256 pre-hash (removes 72-byte limit)
    """
    return hashlib.sha256(password.encode()).hexdigest()

def hash_password(password: str) -> str:
    prehashed = _pre_hash(password)
    return pwd_context.hash(prehashed)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    prehashed = _pre_hash(plain_password)
    return pwd_context.verify(prehashed, hashed_password)

# 🔑 CREATE TOKEN
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except:
        return None