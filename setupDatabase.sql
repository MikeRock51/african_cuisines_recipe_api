DROP USER IF EXISTS 'recipe_dev'@'localhost';
CREATE USER IF NOT EXISTS 'recipe_dev'@'localhost' IDENTIFIED BY 'recipe_dev_pwd';
DROP DATABASE IF EXISTS recipe_db;
CREATE DATABASE IF NOT EXISTS recipe_db;
GRANT ALL PRIVILEGES ON `basecamp_db`.* TO 'recipe_dev'@'localhost';
GRANT SELECT ON `perfomance_schema`.* TO 'recipe_dev'@'localhost';
FLUSH PRIVILEGES;
