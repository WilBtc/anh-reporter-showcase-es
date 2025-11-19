-- ANH Reporter Database Initialization Script
-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- Create database (if not exists via environment variable)
-- The database is already created via POSTGRES_DB env var

\c anh_reporter;

-- Enable TimescaleDB for this database
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- Create users table will be handled by SQLAlchemy/Alembic
-- This script just sets up the TimescaleDB hypertable after table creation

-- Function to convert telemetry_readings to hypertable (run after table creation)
CREATE OR REPLACE FUNCTION setup_timescaledb()
RETURNS void AS $$
BEGIN
    -- Check if telemetry_readings table exists and convert to hypertable
    IF EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'telemetry_readings') THEN
        PERFORM create_hypertable('telemetry_readings', 'timestamp', if_not_exists => TRUE);

        -- Create retention policy (5 years = 1825 days)
        PERFORM add_retention_policy('telemetry_readings', INTERVAL '1825 days', if_not_exists => TRUE);

        -- Create compression policy (compress data older than 7 days)
        PERFORM add_compression_policy('telemetry_readings', INTERVAL '7 days', if_not_exists => TRUE);
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE anh_reporter TO anh_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO anh_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO anh_user;

-- Success message
SELECT 'ANH Reporter database initialized successfully!' AS status;
