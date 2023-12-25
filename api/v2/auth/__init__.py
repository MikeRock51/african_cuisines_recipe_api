#!/usr/bin/env python3
"""Initializes authentication class"""

from dotenv import load_dotenv
from os import getenv
from api.v2.config import Configs 


auth = Configs.AUTH
