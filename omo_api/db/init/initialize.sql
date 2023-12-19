-- This sql file is automated executed when the postgres container is first created
-- These values are hardcoded and doesn't use env variables :(
CREATE USER omoai WITH PASSWORD 'CHANGE_ME';
CREATE DATABASE omoai;

-- grant necessary privileges to user
GRANT ALL PRIVILEGES ON DATABASE omoai TO omoai;
GRANT ALL ON SCHEMA public TO omoai;

-- ensure owner can make changes
ALTER DATABASE omoai OWNER TO omoai;