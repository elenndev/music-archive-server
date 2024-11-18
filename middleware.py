from jose import JWTError, jwt
from datetime import datetime, timezone
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from fastapi import Depends
import requests
import os
AUTH_API_URL = os.environ.get('AUTH_API_URL')


def validate_auth(token):
    headers = {
        "Authorization": f"Bearer {token}"}
    response = requests.get(f"{AUTH_API_URL}/check-token", headers = headers)
    return response