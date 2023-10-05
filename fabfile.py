#!/usr/bin/env python3
"""Deploys """
# import collections.abc
# collections.Mapping = collections.abc.Mapping

from fabric.api import *
from dotenv import load_dotenv
from os import getenv
from datetime import datetime
import json

load_dotenv()

SQL_ROOT_PWD = getenv("SQL_ROOT_PWD")
PSN = getenv("PSN") 
APP_FILES = json.loads(getenv('APP_FILES'))

def set_sql_pwd():
    """Sets the root password of MySQL"""
    run(f'echo "mysql-server mysql-server/root_password password {SQL_ROOT_PWD}" | debconf-set-selections')
    run(f'echo "mysql-server mysql-server/root_password_again password {SQL_ROOT_PWD}" | debconf-set-selections')

def packFiles():
    """Packs the application file in a .tgz archive"""
    dateString = datetime.utcnow().strftime("%Y:%m:%d:%H:%M:%S")
    archivePath = f"versions/{PSN}_{dateString}.tgz"

    local("mkdir -p versions")
    status = local(f"tar -cvzf {archivePath} {' '.join(APP_FILES)}")

    return archivePath
