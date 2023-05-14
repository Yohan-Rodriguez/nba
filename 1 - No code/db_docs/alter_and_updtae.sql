ALTER TABLE leagues ADD link_league VARCHAR(150) NOT NULL;

UPDATE t_errors 
SET league_error = 'tunisia - national-a-league'
WHERE id_error = 164;


INSERT INTO leagues (id_league, name_league)
VALUES (123, 'international - euroleague');

ALTER TABLE t_errors
MODIFY league_error VARCHAR(60);

