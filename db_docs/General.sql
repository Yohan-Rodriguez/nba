USE analysis_basketball_test;
USE analysis_basketball_2;
USE analysis_basketball;

SELECT * FROM teams
LIMIT 0, 10000;
SELECT * FROM matches
LIMIT 0, 10000;
SELECT * FROM leagues;
SELECT * FROM teams_has_leagues;
SELECT * FROM teams_has_matches
LIMIT 0, 10000;
SELECT * FROM t_errors;
SELECT * FROM statistics;

SELECT * FROM teams
WHERE name = 'Olympi';

SELECT id_team FROM team
WHERE id_team =  125;


INSERT INTO team (id_team, name_team) VALUES (111, 'WART');

    
    
SELECT COUNT(leagues_id_league)
FROM team_has_leagues
GROUP BY leagues_id_league;

SELECT DISTINCT(team_id_team) 
FROM team_has_matches
LIMIT 10000;

SELECT leagues.name_league, COUNT(team.id_team)
FROM leagues
INNER JOIN team_has_leagues ON leagues.id_league = team_has_leagues.leagues_id_league
INNER JOIN team ON team_has_leagues.team_id_team = team.id_team
GROUP BY leagues.name_league;

SELECT team.name_team, leagues.name_league
FROM leagues
INNER JOIN team_has_leagues ON leagues.id_league = team_has_leagues.leagues_id_league
INNER JOIN team ON team.id_team = team_has_leagues.team_id_team
WHERE leagues.name_league = 'italy - serie-a';

SELECT team.name_team, matches.*
FROM team
INNER JOIN team_has_matches ON team.id_team = team_has_matches.team_id_team
INNER JOIN matches ON matches.id_match = team_has_matches.matches_id_match
WHERE name_team = 'Milano';

SELECT * FROM team
WHERE name_team =  '76ers';

SELECT * 
FROM team_has_leagues
WHERE leagues_id_league = 412 AND team_id_team = (
	SELECT id_team FROM team
    WHERE name_team = '76ers'
    );
    
SELECT *
FROM team;

SELECT COUNT(is_win)
FROM matches
WHERE is_win = 0;