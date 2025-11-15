-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- Note: Tables are created by SQLAlchemy
-- This file can be used for additional database initialization

-- Create indexes for performance (will be created if they don't exist)
-- These indexes are created automatically by SQLAlchemy models

-- Function to create hypertable if it doesn't exist
-- This will be called from Python code after table creation
