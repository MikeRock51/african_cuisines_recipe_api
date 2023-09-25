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

class SessionAuth():
    """Handles Session Authentication"""

    _tokenKey = 'auth_{}'

    def __init__(self) -> None:
        """Initializes a new redis client"""
        self._client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    def createSession(self, userID: str = None) -> str:
        """Creates and stores a new session token"""
        if not userID:
            raise ValueError('Missing User ID')

        token = str(uuid4())
        self._client.setex(self._tokenKey.format(token), int(TOKEN_TTL), userID)
        return token

    def getSession(self, token: str):
        """Retrieves a session based on token"""
        if not token:
            raise ValueError('Missing token')
        
        userID = self._client.get(self._tokenKey.format(token))
        if not userID:
            raise ValueError('Unauthorized')

        return userID



if __name__ == '__main__':
    session = SessionAuth()
 #   mikeID = session.createSession('Mike-Rock')
 #   print(mikeID)
    print(session.getSession('b088df9e-8147-488d-b7c2-c46a313c0fa5'))
