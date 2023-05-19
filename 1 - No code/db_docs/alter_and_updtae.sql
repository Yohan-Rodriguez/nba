ALTER TABLE leagues ADD link_league VARCHAR(150) NOT NULL;

UPDATE t_errors 
SET league_error = 'tunisia - national-a-league'
WHERE id_error = 164;


INSERT INTO leagues (id_league, name_league)
VALUES (123, 'international - euroleague');

ALTER TABLE t_errors
MODIFY league_error VARCHAR(60);

ALTER TABLE statistics
CHANGE teams_has_leagues_leagues_id_league id_leagues_id_league INT;


SELECT name_team
                    FROM teams
                    JOIN teams_has_leagues ON teams.id_team = teams_has_leagues.teams_id_team
                    WHERE teams_has_leagues.leagues_id_league IN {tuple_get}
						IS NOT ???
                       OR teams_has_leagues.leagues_id_league = {tuple_get[0]}
                    ORDER BY teams_has_leagues.leagues_id_league, name_team
