-- This sql file is automated executed when the postgres container is first created
-- These values are hardcoded and doesn't use env variables :(
CREATE USER omolytics WITH PASSWORD 'CHANGE_ME';
CREATE DATABASE omolytics;

-- grant necessary privileges to user
GRANT ALL PRIVILEGES ON DATABASE omolytics TO omolytics;
GRANT ALL ON SCHEMA public TO omolytics;

-- ensure owner can make changes
ALTER DATABASE omolytics OWNER TO omolytics;