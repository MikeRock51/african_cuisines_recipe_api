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
    sudo("apt install -y python3-venv")
    sudo("apt-get install -y pkg-config")
    sudo("apt-get install -y libmysqlclient-dev")
    sudo("apt install -y nginx")
    sudo("apt install -y redis-server")
    sudo("sed -i 's/supervised no/supervised systemd/' /etc/redis/redis.conf")
    sudo("systemctl restart redis.service")
    print("Packages installed successfully!")


def deployServiceFile():
    """Deploys the systemd service unit for the app"""
    put(f"serverConfigurations/{PSN}.service",
        "/etc/systemd/system/", use_sudo=True)
    sudo("systemctl daemon-reload")
    sudo(f"systemctl enable {PSN}.service")
    print("Service file deployed successfully!")


def startUnitService():
    """Starts the apps unit service"""
    sudo(f"systemctl start {PSN}.service")
    print(f"{PSN} service started successfully!")


def stopUnitService():
    """Stops the apps unit service"""
    sudo(f"systemctl stop {PSN}.service")
    print(f"{PSN} service stopped successfully!")

def unitStatus():
    """Gets the status of the apps unit service"""
    sudo(f"systemctl status {PSN}.service")


def restartUnitService():
    """Restarts the apps unit service"""
    sudo(f"systemctl restart {PSN}.service")
    print(f"{PSN} service restarted successfully!")


def deployNginxConfig():
    """Deploys Nginx configuration and restarts Nginx"""
    put(f'serverConfigurations/{PSN}-nginx',
        '/etc/nginx/sites-available/', use_sudo=True)
    sudo(f"ln -s /etc/nginx/sites-available/{PSN}-nginx /etc/nginx/sites-enabled/")
    sudo('systemctl restart nginx')
    print("Nginx config deployed successfully!")


def restartNginx():
    """Restarts Nginx service"""
    sudo('systemctl restart nginx')
    print("Nginx service restarted successfully!")

def nginxStatus():
    """Checks the status of server's Nginx service"""
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
    put(archivePath, remoteVersionsPath, use_sudo=True)
    run(f"mkdir -p {PSN}")
    archiveName = archivePath.split('/')[1]
    run(f"tar -xvzf {remoteVersionsPath}/{archiveName} -C {PSN}")
    print("Files shipped successfully!")


def installRequirements():
    """Install project dependencies"""
    with cd(PSN):
        run("pip3 install -r requirements.txt")
        run("python3 -m venv .venv")
        run("source .venv/bin/activate && pip3 install -r requirements.txt")
    print("Requirements installed successfully!")


def setupDB():
    """(Re)Creates and prepopulates database with data"""
    with cd(PSN):
        run(f"cat setupDatabase.sql | mysql -uroot -p{SQL_ROOT_PWD}")
        run("python3 createRecipeDataDB.py")
    print("Database is ready!")

def removeOldFiles():
    """Deletes the old deployed project files"""
    run("rm -rf {PSN}")
    print("Files removed successfully!")


def deployFiles():
    archivePath = packFiles()
    shipFiles(archivePath)
    print("Files deployed successfully!")

def updateFiles():
    """Replaces old project files with current ones"""
    removeOldFiles()
    deployFiles()
    print("Files updated successfully!")


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
    print("Hurray!! Full deployment successful!")
