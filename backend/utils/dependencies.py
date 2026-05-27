from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from config.settings import settings

security = HTTPBearer()

def get_current_user(token=Depends(security)):
    try:
        payload = jwt.decode(token.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload  # contains user_id, role

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# 🔥 ROLE CHECK
def require_role(required_role: str):
    def role_checker(user=Depends(get_current_user)):
        if user["role"] != required_role:
            raise HTTPException(status_code=403, detail="Access denied")
        return user
    return role_checker