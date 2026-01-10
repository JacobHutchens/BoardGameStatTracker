-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema boardgametracker
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `boardgametracker` DEFAULT CHARACTER SET utf8mb3 ;
USE `boardgametracker` ;

-- -----------------------------------------------------
-- Table `boardgametracker`.`data_type`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `boardgametracker`.`data_type` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `data_type` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `data_type_UNIQUE` (`data_type` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `boardgametracker`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `boardgametracker`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `password_hash` VARCHAR(45) NOT NULL,
  `created_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `user_id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 51
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `boardgametracker`.`follower`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `boardgametracker`.`follower` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `following_user_id` INT NOT NULL,
  `followed_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_follower_user1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_follower_user2_idx` (`following_user_id` ASC) VISIBLE,
  CONSTRAINT `fk_follower_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `boardgametracker`.`user` (`id`),
  CONSTRAINT `fk_follower_user2`
    FOREIGN KEY (`following_user_id`)
    REFERENCES `boardgametracker`.`user` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 101
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `boardgametracker`.`game`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `boardgametracker`.`game` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `game_name` VARCHAR(45) NOT NULL,
  `max_player_count` INT NULL DEFAULT NULL,
  `min_player_count` INT NULL DEFAULT NULL,
  `description` TEXT NOT NULL,
  `can_win` TINYINT NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `game_id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `game_name_UNIQUE` (`game_name` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 51
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `boardgametracker`.`game_tracked_stat_set`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `boardgametracker`.`game_tracked_stat_set` (
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
    REFERENCES `boardgametracker`.`game` (`id`),
  CONSTRAINT `fk_game_tracked_stat_set_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `boardgametracker`.`user` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 51
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `boardgametracker`.`scope`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `boardgametracker`.`scope` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `scope` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `scope_UNIQUE` (`scope` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `boardgametracker`.`game_tracked_stat`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `boardgametracker`.`game_tracked_stat` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `game_tracked_stat_set_id` INT NOT NULL,
  `stat_name` VARCHAR(45) NOT NULL,
  `data_type_id` INT NOT NULL,
  `scope_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_table2_game_tracked_stat_set1_idx` (`game_tracked_stat_set_id` ASC) VISIBLE,
  INDEX `fk_table2_scope1_idx` (`scope_id` ASC) VISIBLE,
  INDEX `fk_table2_data_type1_idx` (`data_type_id` ASC) VISIBLE,
  CONSTRAINT `fk_table2_data_type1`
    FOREIGN KEY (`data_type_id`)
    REFERENCES `boardgametracker`.`data_type` (`id`),
  CONSTRAINT `fk_table2_game_tracked_stat_set1`
    FOREIGN KEY (`game_tracked_stat_set_id`)
    REFERENCES `boardgametracker`.`game_tracked_stat_set` (`id`),
  CONSTRAINT `fk_table2_scope1`
    FOREIGN KEY (`scope_id`)
    REFERENCES `boardgametracker`.`scope` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 151
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `boardgametracker`.`session`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `boardgametracker`.`session` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `game_id` INT NOT NULL,
  `session_key` VARCHAR(6) NOT NULL,
  `time_started` DATETIME NOT NULL,
  `time_ended` DATETIME NULL DEFAULT NULL,
  `current_round` INT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `live_session_id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `session_key_UNIQUE` (`session_key` ASC) VISIBLE,
  INDEX `fk_live_session_game1_idx` (`game_id` ASC) VISIBLE,
  CONSTRAINT `fk_live_session_game1`
    FOREIGN KEY (`game_id`)
    REFERENCES `boardgametracker`.`game` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 51
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `boardgametracker`.`session_player`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `boardgametracker`.`session_player` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `session_id` INT NOT NULL,
  `user_id` INT NULL DEFAULT NULL,
  `player_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `live_session_user_id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_live_session_player_user1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_live_session_player_session1_idx` (`session_id` ASC) VISIBLE,
  CONSTRAINT `fk_live_session_player_session1`
    FOREIGN KEY (`session_id`)
    REFERENCES `boardgametracker`.`session` (`id`),
  CONSTRAINT `fk_live_session_player_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `boardgametracker`.`user` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 151
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `boardgametracker`.`session_tracked_stat`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `boardgametracker`.`session_tracked_stat` (
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
  CONSTRAINT `fk_live_session_tracked_stat_data_type1`
    FOREIGN KEY (`data_type_id`)
    REFERENCES `boardgametracker`.`data_type` (`id`),
  CONSTRAINT `fk_session_tracked_stat_scope1`
    FOREIGN KEY (`scope_id`)
    REFERENCES `boardgametracker`.`scope` (`id`),
  CONSTRAINT `fk_session_tracked_stat_session1`
    FOREIGN KEY (`session_id`)
    REFERENCES `boardgametracker`.`session` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 151
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `boardgametracker`.`player_stat_value`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `boardgametracker`.`player_stat_value` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `session_tracked_stat_id` INT NOT NULL,
  `session_player_id` INT NOT NULL,
  `stat_value` VARCHAR(45) NOT NULL,
  `recorded_at` DATETIME NOT NULL,
  `round_number` INT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_player_stat_value_session_tracked_stat1_idx` (`session_tracked_stat_id` ASC) VISIBLE,
  INDEX `fk_player_stat_value_session_player1_idx` (`session_player_id` ASC) VISIBLE,
  CONSTRAINT `fk_player_stat_value_session_player1`
    FOREIGN KEY (`session_player_id`)
    REFERENCES `boardgametracker`.`session_player` (`id`),
  CONSTRAINT `fk_player_stat_value_session_tracked_stat1`
    FOREIGN KEY (`session_tracked_stat_id`)
    REFERENCES `boardgametracker`.`session_tracked_stat` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 163
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `boardgametracker`.`table_stat_value`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `boardgametracker`.`table_stat_value` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `session_tracked_stat_id` INT NOT NULL,
  `session_id` INT NOT NULL,
  `stat_value` VARCHAR(45) NOT NULL,
  `recorded_at` DATETIME NOT NULL,
  `round_number` INT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_table_stat_value_session_tracked_stat1_idx` (`session_tracked_stat_id` ASC) VISIBLE,
  INDEX `fk_table_stat_value_session1_idx` (`session_id` ASC) VISIBLE,
  CONSTRAINT `fk_table_stat_value_session1`
    FOREIGN KEY (`session_id`)
    REFERENCES `boardgametracker`.`session` (`id`),
  CONSTRAINT `fk_table_stat_value_session_tracked_stat1`
    FOREIGN KEY (`session_tracked_stat_id`)
    REFERENCES `boardgametracker`.`session_tracked_stat` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 64
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `boardgametracker`.`user_game_stats_cache`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `boardgametracker`.`user_game_stats_cache` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `game_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `total_times_played` INT NOT NULL,
  `wins` INT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `user_game_id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_user_game_stats_game1_idx` (`game_id` ASC) VISIBLE,
  INDEX `fk_user_game_stats_user1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_user_game_stats_game1`
    FOREIGN KEY (`game_id`)
    REFERENCES `boardgametracker`.`game` (`id`),
  CONSTRAINT `fk_user_game_stats_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `boardgametracker`.`user` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 58
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `boardgametracker`.`token_type`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `boardgametracker`.`token_type` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `token_type` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `token_type_UNIQUE` (`token_type` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `boardgametracker`.`user_tokens`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `boardgametracker`.`user_tokens` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `token_type_id` INT NOT NULL,
  `token` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_user_tokens_user1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_user_tokens_token_type1_idx` (`token_type_id` ASC) VISIBLE,
  CONSTRAINT `fk_user_tokens_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `boardgametracker`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_tokens_token_type1`
    FOREIGN KEY (`token_type_id`)
    REFERENCES `boardgametracker`.`token_type` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
