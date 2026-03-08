-- Migration: Add optional time_zone to user table
-- Purpose: Session limit week (Sunday–Saturday) is computed in user timezone; default UTC-8 when null.
-- Run after create-tables.sql.

USE `BoardGameTracker`;

ALTER TABLE `BoardGameTracker`.`user`
  ADD COLUMN `time_zone` VARCHAR(64) NULL AFTER `default_session_visibility`;
