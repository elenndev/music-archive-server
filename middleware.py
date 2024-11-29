from jose import JWTError, jwt
from datetime import datetime, timezone
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from fastapi import Depends
import requests
import os
AUTH_API_URL = os.environ.get('AUTH_API_URL')


def validate_auth(cookies):
    response = requests.get(f"{AUTH_API_URL}/check-token", cookies = cookies)
    print(cookies)
    print(response)
    print(response.json())
    return response.json()
