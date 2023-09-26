#!/usr/bin/env python3
"""Session Authentication module"""

from os import getenv
import redis
from dotenv import load_dotenv
from uuid import uuid4
from models import storage
from models.user import User
from sqlalchemy.exc import NoResultFound

load_dotenv()

REDIS_HOST = getenv('REDIS_HOST')
REDIS_PORT = getenv('REDIS_PORT')
TOKEN_TTL = getenv('TOKEN_TTL')
AUTH_HEADER = getenv('AUTH_HEADER')

class SessionAuth():
    """Handles Session Authentication"""

    _key = 'auth_{}'

    def __init__(self) -> None:
        """Initializes a new redis client"""
        self._client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    def createSession(self, userID: str = None) -> str:
        """Creates and stores a new session token"""
        if not userID:
            raise ValueError('Missing User ID')

        token = str(uuid4())
        self._client.setex(self._key.format(token), int(TOKEN_TTL), userID)
        return token

    def getSession(self, token: str) -> str:
        """Retrieves a session based on token"""
        if not token:
            raise ValueError('Missing token')
        
        userID = self._client.get(self._key.format(token))
        if not userID:
            raise ValueError('Unauthorized')

        return userID

    def getUser(self, email: str) -> User:
        """Retrieves a user based on userID"""
        try:
            user = storage.getByEmail(email)
        except NoResultFound:
            raise ValueError('User does not exist')

        return user

    def destroySession(self, token: str) -> None:
        """Destroys a session based on token"""
        if not token:
            raise ValueError('Missing token')

        response = self._client.delete(self._key.format(token))
        if not response:
            raise ValueError('Token is not valid')

        return None

    def extractAuthToken(self, request) -> str:
        """Extracts auth token from header"""
        token = request.headers.get(AUTH_HEADER)
        if not token:
            raise ValueError(f'{AUTH_HEADER} is required');

        return token
