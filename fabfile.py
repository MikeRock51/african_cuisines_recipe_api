#!/usr/bin/env python3
"""Deploys """
# import collections.abc
# collections.Mapping = collections.abc.Mapping

from fabric.api import *
from dotenv import load_dotenv
from os import getenv, path
from datetime import datetime
import json

load_dotenv()

SQL_ROOT_PWD = getenv("SQL_ROOT_PWD")
PSN = getenv("PSN")
APP_FILES = json.loads(getenv('APP_FILES'))


def configureSQL():
    """Installs and sets the root password of MySQL"""
    run("sudo apt install -y mysql-server")
    run("sudo apt update")
    sudo("service mysql stop")
    sudo("mysqld_safe --skip-grant-tables &")
    run("sleep 5")
    sudo("service mysql start")
    sudo(
        f"mysql -u root -e \"ALTER USER 'root'@'localhost' IDENTIFIED WITH 'mysql_native_password' BY '{SQL_ROOT_PWD}';\"")
    sudo("service mysql start")
    print("MySQL root password changed successfully.")


def installPackages():
    """Installs project required packages on the server"""
    sudo("apt update")
    sudo("apt install -y python3")
    sudo("apt install -y python3-pip")
    sudo("apt-get install -y pkg-config")
    sudo("apt-get install -y libmysqlclient-dev")
    sudo("apt install -y nginx")
    sudo("apt install redis-server")
    sudo("sed -i /'s/supervised no'/'supervised systemd/' /etc/redis/redis.conf")
    sudo("systemctl restart redis.service")


def deployServiceFile():
    """Deploys the systemd service unit for the app"""
    put(f"serverConfigurations/{PSN}.service", use_sudo=True)
    sudo("systemctl daemon-reload")
    sudo(f"systemctl enable {PSN}.service")


def startUnitService():
    """Starts the apps unit service"""
    sudo(f"systemctl enable {PSN}.service")
    sudo(f"systemctl status {PSN}.service")


def stopUnitService():
    """Stopsthe apps unit service"""
    sudo(f"systemctl stop {PSN}.service")
    sudo(f"systemctl status {PSN}.service")


def restartUnitService():
    """Restarts the apps unit service"""
    sudo(f"systemctl restart {PSN}.service")
    sudo(f"systemctl status {PSN}.service")


def deployNginxConfig():
    """Deploys Nginx configuration and restarts Nginx"""
    put('serverConfigurations/{PSN}-nginx',
        '/etc/nginx/sites-available/', use_sudo=True)
    sudo('systemctl restart nginx')
    sudo('systemctl status nginx')


def packFiles():
    """Packs the application file in a .tgz archive"""
    dateString = datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")
    archivePath = f"versions/{PSN}_{dateString}.tgz"

    local("mkdir -p versions")
    local(f"tar -cvzf {archivePath} {' '.join(APP_FILES)}")
    return archivePath


def shipFiles(archivePath):
    """Unpacks the contents of an archive to the server(s)"""
    if not path.exists(archivePath):
        return False
    remoteVersionsPath = f"/tmp/{PSN}/versions"
    run(f"mkdir -p {remoteVersionsPath}")
    put(archivePath, remoteVersionsPath)
    run(f"mkdir -p {PSN}")
    archiveName = archivePath.split('/')[1]
    run(f"tar -xvzf {remoteVersionsPath}/{archiveName} -C {PSN}")


def installRequirements():
    """Install project dependencies"""
    with cd(PSN):
        run("python3 -m venv .venv")
        run("source .venv/bin/activate")
        run("pip3 install -r requirements.txt")


def setupDB():
    """(Re)Creates and prepopulates datatbase with data"""
    with cd({PSN}):
        run(f"cat setupDatabase.sql | mysql -uroot -p {SQL_ROOT_PWD}")
        run("python3 createRecipeDataDB.py")


def deployFiles():
    archivePath = packFiles()
    shipFiles(archivePath)


def fullDeploy():
    """Performs a full deploy to a new server"""
    deployFiles()
    installPackages()
    configureSQL()
    installRequirements()
    setupDB()
    deployNginxConfig()
    deployServiceFile()
    startUnitService()
