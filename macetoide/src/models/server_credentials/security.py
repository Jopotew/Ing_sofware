from datetime import datetime, timezone, timedelta
import bcrypt
from fastapi import Request, HTTPException, status
import jwt
import os
from dotenv import load_dotenv

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))







