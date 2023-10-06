DROP USER IF EXISTS 'acr_dev'@'localhost';
CREATE USER IF NOT EXISTS 'acr_dev'@'localhost' IDENTIFIED BY 'acr_dev_pwd';
DROP DATABASE IF EXISTS acr_db;
CREATE DATABASE IF NOT EXISTS acr_db;
GRANT ALL PRIVILEGES ON `acr_db`.* TO 'acr_dev'@'localhost';
GRANT SELECT ON `perfomance_schema`.* TO 'acr_dev'@'localhost';
FLUSH PRIVILEGES;
