-- Schema for the FieldTasker hardware and threat database

CREATE TABLE IF NOT EXISTS rf_signals (
    id INTEGER PRIMARY KEY,
    identifier TEXT NOT NULL,
    frequency TEXT NOT NULL,
    type TEXT NOT NULL,
    vendor TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS firmware_fingerprints (
    id INTEGER PRIMARY KEY,
    device_type TEXT NOT NULL,
    vendor TEXT,
    model TEXT,
    firmware_hash TEXT NOT NULL UNIQUE,
    fingerprint_source TEXT,
    threat_level TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS discovered_hardware_log (
    id INTEGER PRIMARY KEY,
    discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    location TEXT,
    device_type TEXT,
    identifier TEXT,
    firmware_hash TEXT,
    match_status TEXT,
    notes TEXT
);

-- Indexes for fast lookups
CREATE INDEX IF NOT EXISTS idx_rf_signals_frequency ON rf_signals(frequency);
CREATE INDEX IF NOT EXISTS idx_rf_signals_type ON rf_signals(type);
CREATE INDEX IF NOT EXISTS idx_firmware_hash ON firmware_fingerprints(firmware_hash);
CREATE INDEX IF NOT EXISTS idx_firmware_vendor ON firmware_fingerprints(vendor);
CREATE INDEX IF NOT EXISTS idx_discovered_device_type ON discovered_hardware_log(device_type);
CREATE INDEX IF NOT EXISTS idx_discovered_location ON discovered_hardware_log(location);
