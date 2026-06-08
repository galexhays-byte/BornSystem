# BornSystem Database Schema

This folder contains the database schema for the field operational threat database.

The database tracks:
- RF and signal signatures (`rf_signals`)
- firmware fingerprints for suspicious devices (`firmware_fingerprints`)
- field discovery audit logs (`discovered_hardware_log`)

Use `database/schema.sql` to create or migrate the SQLite database.
