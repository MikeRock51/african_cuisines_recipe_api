#!/usr/bin/env python3
"""Session Authentication module"""

from os import getenv
import redis
from dotenv import load_dotenv
from uuid import uuid4

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
        print(AUTH_HEADER)

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

    def destroySession(self, token: str) -> None:
        """Destroys a session based on token"""
        if not token:
            raise ValueError('Missing token')

        response = self._client.delete(self._key.format(token))
        if not response:
            raise ValueError('Token is not valid')

        return None

    def getAuthToken(self, request) -> str:
        """Extracts auth token from header"""
        token = request.header.get(AUTH_TOKEN)
        if not token:
            raise ValueError(f'{AUTH_TOKEN} is required');

        return token

if __name__ == '__main__':
    session = SessionAuth()
 #   mikeID = session.createSession('Mike-Rock')
 #   print(mikeID)
    # print(session.getSession('b088df9e-8147-488d-b7c2-c46a313c0fa5'))
    print(session.destroySession('b088df9e-8147-488d-b7c2-c46a313c0fa5'))
