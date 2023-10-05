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
APP_FILES = json.dumps(getenv('APP_FILES'))

def set_sql_pwd():
    """Sets the root password of MySQL"""
    run(f'echo "mysql-server mysql-server/root_password password {SQL_ROOT_PWD}" | debconf-set-selections')
    run(f'echo "mysql-server mysql-server/root_password_again password {SQL_ROOT_PWD}" | debconf-set-selections')

def do_pack():
    """Packs the application file in a .tgz archive"""
    local("mkdir -p versions")

    dateString = datetime.utcnow().strftime("%Y:%m:%d:%H:%M:%S")
    path = f"versions/{PSN}.tgz"

    status = local(f"tar -cvzf {path} {' '.join(APP_FILES)}")
