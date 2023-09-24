DROP USER IF EXISTS 'afr_dev'@'localhost';
CREATE USER IF NOT EXISTS 'afr_dev'@'localhost' IDENTIFIED BY 'afr_dev_pwd';
DROP DATABASE IF EXISTS afr_db;
CREATE DATABASE IF NOT EXISTS afr_db;
GRANT ALL PRIVILEGES ON `afr_db`.* TO 'afr_dev'@'localhost';
GRANT SELECT ON `perfomance_schema`.* TO 'afr_dev'@'localhost';
FLUSH PRIVILEGES;
