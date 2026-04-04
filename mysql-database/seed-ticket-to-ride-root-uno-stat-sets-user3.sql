-- Stat sets for Ticket to Ride, Root, and Uno — owner user_id = 3
-- Requires scope: 1=Player, 2=Table; data_type: 1=Integer, 2=String, 3=Boolean, 4=Percent
-- Run against BoardGameTracker after `user` id 3 exists (adjust if your account has another id).

USE `BoardGameTracker`;

-- ---------------------------------------------------------------------------
-- Games (idempotent: only inserts if game_name is not already present)
-- ---------------------------------------------------------------------------
INSERT INTO `game` (`game_name`, `min_player_count`, `max_player_count`, `description`, `can_win`, `created_at`)
SELECT 'Ticket to Ride', 2, 5,
       'Route-building and set collection on a map; players claim train routes and complete tickets.',
       1, NOW()
WHERE NOT EXISTS (SELECT 1 FROM `game` g WHERE g.`game_name` = 'Ticket to Ride');

INSERT INTO `game` (`game_name`, `min_player_count`, `max_player_count`, `description`, `can_win`, `created_at`)
SELECT 'Root', 2, 4,
       'Asymmetric woodland factions competing for dominance; area control and hand management.',
       1, NOW()
WHERE NOT EXISTS (SELECT 1 FROM `game` g WHERE g.`game_name` = 'Root');

INSERT INTO `game` (`game_name`, `min_player_count`, `max_player_count`, `description`, `can_win`, `created_at`)
SELECT 'Uno', 2, 10,
       'Shedding card game: match color or number; first to empty hand wins the round.',
       1, NOW()
WHERE NOT EXISTS (SELECT 1 FROM `game` g WHERE g.`game_name` = 'Uno');

-- ---------------------------------------------------------------------------
-- Ticket to Ride — "generic train stat set"
-- ---------------------------------------------------------------------------
INSERT INTO `game_tracked_stat_set` (`game_id`, `user_id`, `set_name`)
SELECT g.`id`, 3, 'generic train stat set'
FROM `game` g WHERE g.`game_name` = 'Ticket to Ride' LIMIT 1;

SET @set_ttr = LAST_INSERT_ID();

INSERT INTO `game_tracked_stat` (`game_tracked_stat_set_id`, `stat_name`, `description`, `data_type_id`, `scope_id`) VALUES
(@set_ttr, 'Round', NULL, 1, 2),
(@set_ttr, 'Score', NULL, 1, 1),
(@set_ttr, 'completed tickets', NULL, 1, 1),
(@set_ttr, 'trains left', NULL, 1, 1),
(@set_ttr, 'cards in hand', NULL, 1, 1);

-- ---------------------------------------------------------------------------
-- Root — "generic root stat set"
-- ---------------------------------------------------------------------------
INSERT INTO `game_tracked_stat_set` (`game_id`, `user_id`, `set_name`)
SELECT g.`id`, 3, 'generic root stat set'
FROM `game` g WHERE g.`game_name` = 'Root' LIMIT 1;

SET @set_root = LAST_INSERT_ID();

INSERT INTO `game_tracked_stat` (`game_tracked_stat_set_id`, `stat_name`, `description`, `data_type_id`, `scope_id`) VALUES
(@set_root, 'Round', NULL, 1, 2),
(@set_root, 'Draw pile size', NULL, 1, 2),
(@set_root, 'Faction being played', NULL, 2, 1),
(@set_root, 'Score', NULL, 1, 1),
(@set_root, 'Buildings on map', NULL, 1, 1),
(@set_root, 'Tokens on map', NULL, 1, 1),
(@set_root, 'Cards in hand', NULL, 1, 1);

-- ---------------------------------------------------------------------------
-- Uno — "generic uno stat set"
-- ---------------------------------------------------------------------------
INSERT INTO `game_tracked_stat_set` (`game_id`, `user_id`, `set_name`)
SELECT g.`id`, 3, 'generic uno stat set'
FROM `game` g WHERE g.`game_name` = 'Uno' LIMIT 1;

SET @set_uno = LAST_INSERT_ID();

INSERT INTO `game_tracked_stat` (`game_tracked_stat_set_id`, `stat_name`, `description`, `data_type_id`, `scope_id`) VALUES
(@set_uno, 'number of cards played', NULL, 1, 1),
(@set_uno, 'number of cards in hand', NULL, 1, 1);
