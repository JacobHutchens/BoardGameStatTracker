-- MySQL Schema: Board Game Stat Tracker
-- Updated to align with REST API specification and documentation.

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema BoardGameTracker
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `BoardGameTracker` DEFAULT CHARACTER SET utf8;
USE `BoardGameTracker`;

-- -----------------------------------------------------
-- Table `BoardGameTracker`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `BoardGameTracker`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `password_hash` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL,
  `bio` TEXT NULL,
  `avatar_url` VARCHAR(255) NULL,
  `designer` TINYINT NOT NULL DEFAULT 0,
  `default_session_visibility` VARCHAR(45) NOT NULL DEFAULT 'public',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `user_id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `BoardGameTracker`.`game`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `BoardGameTracker`.`game` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `game_name` VARCHAR(45) NOT NULL,
  `max_player_count` INT NULL,
  `min_player_count` INT NULL,
  `description` TEXT NOT NULL,
  `can_win` TINYINT NOT NULL DEFAULT 1,
  `created_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `game_id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `game_name_UNIQUE` (`game_name` ASC) VISIBLE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `BoardGameTracker`.`scope`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `BoardGameTracker`.`scope` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `scope` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `scope_UNIQUE` (`scope` ASC) VISIBLE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `BoardGameTracker`.`data_type`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `BoardGameTracker`.`data_type` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `data_type` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `BoardGameTracker`.`game_tracked_stat_set`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `BoardGameTracker`.`game_tracked_stat_set` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `game_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `set_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_game_tracked_stat_set_game1_idx` (`game_id` ASC) VISIBLE,
  INDEX `fk_game_tracked_stat_set_user1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_game_tracked_stat_set_game1`
    FOREIGN KEY (`game_id`)
    REFERENCES `BoardGameTracker`.`game` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_game_tracked_stat_set_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `BoardGameTracker`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `BoardGameTracker`.`game_tracked_stat`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `BoardGameTracker`.`game_tracked_stat` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `game_tracked_stat_set_id` INT NOT NULL,
  `stat_name` VARCHAR(45) NOT NULL,
  `description` TEXT NULL,
  `data_type_id` INT NOT NULL,
  `scope_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_table2_game_tracked_stat_set1_idx` (`game_tracked_stat_set_id` ASC) VISIBLE,
  INDEX `fk_table2_scope1_idx` (`scope_id` ASC) VISIBLE,
  INDEX `fk_table2_data_type1_idx` (`data_type_id` ASC) VISIBLE,
  CONSTRAINT `fk_table2_game_tracked_stat_set1`
    FOREIGN KEY (`game_tracked_stat_set_id`)
    REFERENCES `BoardGameTracker`.`game_tracked_stat_set` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_table2_scope1`
    FOREIGN KEY (`scope_id`)
    REFERENCES `BoardGameTracker`.`scope` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_table2_data_type1`
    FOREIGN KEY (`data_type_id`)
    REFERENCES `BoardGameTracker`.`data_type` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `BoardGameTracker`.`session`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `BoardGameTracker`.`session` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `creator_user_id` INT NOT NULL,
  `game_id` INT NOT NULL,
  `stat_set_id` INT NOT NULL,
  `session_key` VARCHAR(6) NOT NULL,
  `time_started` DATETIME NOT NULL,
  `time_ended` DATETIME NULL,
  `current_round` INT NULL,
  `visibility_override` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `live_session_id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `session_key_UNIQUE` (`session_key` ASC) VISIBLE,
  INDEX `fk_live_session_game1_idx` (`game_id` ASC) VISIBLE,
  INDEX `fk_session_stat_set_idx` (`stat_set_id` ASC) VISIBLE,
  INDEX `fk_session_creator_user_idx` (`creator_user_id` ASC) VISIBLE,
  CONSTRAINT `fk_live_session_game1`
    FOREIGN KEY (`game_id`)
    REFERENCES `BoardGameTracker`.`game` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_session_stat_set`
    FOREIGN KEY (`stat_set_id`)
    REFERENCES `BoardGameTracker`.`game_tracked_stat_set` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_session_creator_user`
    FOREIGN KEY (`creator_user_id`)
    REFERENCES `BoardGameTracker`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `BoardGameTracker`.`session_player`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `BoardGameTracker`.`session_player` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `session_id` INT NOT NULL,
  `user_id` INT NULL,
  `player_name` VARCHAR(45) NOT NULL,
  `is_spectator` TINYINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `live_session_user_id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_live_session_player_user1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_live_session_player_session1_idx` (`session_id` ASC) VISIBLE,
  CONSTRAINT `fk_live_session_player_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `BoardGameTracker`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_live_session_player_session1`
    FOREIGN KEY (`session_id`)
    REFERENCES `BoardGameTracker`.`session` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `BoardGameTracker`.`session_invite`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `BoardGameTracker`.`session_invite` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `session_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `invited_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `session_user_UNIQUE` (`session_id` ASC, `user_id` ASC) VISIBLE,
  INDEX `fk_session_invite_user_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_session_invite_session`
    FOREIGN KEY (`session_id`)
    REFERENCES `BoardGameTracker`.`session` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_session_invite_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `BoardGameTracker`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `BoardGameTracker`.`session_tracked_stat`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `BoardGameTracker`.`session_tracked_stat` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `session_id` INT NOT NULL,
  `stat_name` VARCHAR(45) NOT NULL,
  `data_type_id` INT NOT NULL,
  `scope_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_session_tracked_stat_scope1_idx` (`scope_id` ASC) VISIBLE,
  INDEX `fk_live_session_tracked_stat_data_type1_idx` (`data_type_id` ASC) VISIBLE,
  INDEX `fk_session_tracked_stat_session1_idx` (`session_id` ASC) VISIBLE,
  CONSTRAINT `fk_session_tracked_stat_scope1`
    FOREIGN KEY (`scope_id`)
    REFERENCES `BoardGameTracker`.`scope` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_live_session_tracked_stat_data_type1`
    FOREIGN KEY (`data_type_id`)
    REFERENCES `BoardGameTracker`.`data_type` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_session_tracked_stat_session1`
    FOREIGN KEY (`session_id`)
    REFERENCES `BoardGameTracker`.`session` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `BoardGameTracker`.`player_stat_value`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `BoardGameTracker`.`player_stat_value` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `session_tracked_stat_id` INT NOT NULL,
  `session_player_id` INT NOT NULL,
  `stat_value` VARCHAR(45) NOT NULL,
  `recorded_at` DATETIME NOT NULL,
  `round_number` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_player_stat_value_session_tracked_stat1_idx` (`session_tracked_stat_id` ASC) VISIBLE,
  INDEX `fk_player_stat_value_session_player1_idx` (`session_player_id` ASC) VISIBLE,
  CONSTRAINT `fk_player_stat_value_session_tracked_stat1`
    FOREIGN KEY (`session_tracked_stat_id`)
    REFERENCES `BoardGameTracker`.`session_tracked_stat` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_player_stat_value_session_player1`
    FOREIGN KEY (`session_player_id`)
    REFERENCES `BoardGameTracker`.`session_player` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `BoardGameTracker`.`table_stat_value`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `BoardGameTracker`.`table_stat_value` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `session_tracked_stat_id` INT NOT NULL,
  `session_id` INT NOT NULL,
  `stat_value` VARCHAR(45) NOT NULL,
  `recorded_at` DATETIME NOT NULL,
  `round_number` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_table_stat_value_session_tracked_stat1_idx` (`session_tracked_stat_id` ASC) VISIBLE,
  INDEX `fk_table_stat_value_session1_idx` (`session_id` ASC) VISIBLE,
  CONSTRAINT `fk_table_stat_value_session_tracked_stat1`
    FOREIGN KEY (`session_tracked_stat_id`)
    REFERENCES `BoardGameTracker`.`session_tracked_stat` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_table_stat_value_session1`
    FOREIGN KEY (`session_id`)
    REFERENCES `BoardGameTracker`.`session` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `BoardGameTracker`.`user_game_stats_cache`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `BoardGameTracker`.`user_game_stats_cache` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `game_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `total_times_played` INT NOT NULL,
  `wins` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `user_game_id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_user_game_stats_game1_idx` (`game_id` ASC) VISIBLE,
  INDEX `fk_user_game_stats_user1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_user_game_stats_game1`
    FOREIGN KEY (`game_id`)
    REFERENCES `BoardGameTracker`.`game` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_game_stats_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `BoardGameTracker`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `BoardGameTracker`.`follower`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `BoardGameTracker`.`follower` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `following_user_id` INT NOT NULL,
  `followed_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `follower_user_following_UNIQUE` (`user_id` ASC, `following_user_id` ASC) VISIBLE,
  INDEX `fk_follower_user1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_follower_user2_idx` (`following_user_id` ASC) VISIBLE,
  CONSTRAINT `fk_follower_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `BoardGameTracker`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_follower_user2`
    FOREIGN KEY (`following_user_id`)
    REFERENCES `BoardGameTracker`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `BoardGameTracker`.`user_refresh_token`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `BoardGameTracker`.`user_refresh_token` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `token_hash` VARCHAR(255) NOT NULL,
  `expires_at` DATETIME NOT NULL,
  `revoked_at` DATETIME NULL,
  `created_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_user_refresh_token_user_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_user_refresh_token_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `BoardGameTracker`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `BoardGameTracker`.`publisher`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `BoardGameTracker`.`publisher` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password_hash` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `publisher_email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `BoardGameTracker`.`publisher_refresh_token`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `BoardGameTracker`.`publisher_refresh_token` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `publisher_id` INT NOT NULL,
  `token_hash` VARCHAR(255) NOT NULL,
  `expires_at` DATETIME NOT NULL,
  `revoked_at` DATETIME NULL,
  `created_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_publisher_refresh_token_publisher_idx` (`publisher_id` ASC) VISIBLE,
  CONSTRAINT `fk_publisher_refresh_token_publisher`
    FOREIGN KEY (`publisher_id`)
    REFERENCES `BoardGameTracker`.`publisher` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `BoardGameTracker`.`publisher_designer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `BoardGameTracker`.`publisher_designer` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `publisher_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `assigned_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `publisher_user_UNIQUE` (`publisher_id` ASC, `user_id` ASC) VISIBLE,
  INDEX `fk_publisher_designer_user_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_publisher_designer_publisher`
    FOREIGN KEY (`publisher_id`)
    REFERENCES `BoardGameTracker`.`publisher` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_publisher_designer_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `BoardGameTracker`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
