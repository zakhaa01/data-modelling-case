-- TODO: test script

-- Create users
CREATE USER service_etl PASSWORD '$ETL_USER_PASSWORD';
-- CREATE USER admin WITH PASSWORD 'admin';

-- -- Create database
-- CREATE DATABASE '$PGDATABASE';

-- -- Connect to tmdb_dwh to create schemas
-- CONNECT '$PGDATABASE'

-- Create schemas
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS analytics_sandbox;
CREATE SCHEMA IF NOT EXISTS analytics_raw;
CREATE SCHEMA IF NOT EXISTS analytics_staging;
CREATE SCHEMA IF NOT EXISTS analytics_marts;

-- Grants
GRANT ALL PRIVILEGES ON SCHEMA analytics TO admin;
GRANT ALL PRIVILEGES ON SCHEMA analytics_sandbox TO admin;
GRANT ALL PRIVILEGES ON SCHEMA analytics_raw TO admin;
GRANT ALL PRIVILEGES ON SCHEMA analytics_staging TO admin;
GRANT ALL PRIVILEGES ON SCHEMA analytics_marts TO admin;

-- GRANT CONNECT ON DATABASE '$PGDATABASE' TO service_etl;

GRANT USAGE ON SCHEMA analytics TO service_etl;
GRANT USAGE ON SCHEMA analytics_sandbox TO service_etl;
GRANT USAGE ON SCHEMA analytics_raw TO service_etl;
GRANT USAGE ON SCHEMA analytics_staging TO service_etl;
GRANT USAGE ON SCHEMA analytics_marts TO service_etl;
