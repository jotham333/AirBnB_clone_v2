-- Create a database named 'hbnb_test_db' if it doesn't already exist
CREATE DATABASE IF NOT EXISTS 'hbnb_test_db';

-- Create a user named 'hbnb_test' with the password 'hbnb_test_pwd' that can only connect from 'localhost'
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Grant all privileges on the 'hbnb_test_db' database to the 'hbnb_test' user from 'localhost'
GRANT ALL PRIVILEGES ON 'hbnb_test_db'.* TO 'hbnb_test'@'localhost';

-- Grant the SELECT privilege on the 'performance_schema' database to the 'hbnb_test' user from 'localhost'
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';

-- Flush the privileges to ensure the changes take effect
FLUSH PRIVILEGES;