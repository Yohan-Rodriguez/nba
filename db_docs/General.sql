USE analysis_basketball_test;
USE analysis_basketball_test_2;
USE colombia_test;
USE test_mis_marcadores;

SELECT * FROM teams
LIMIT 0, 40000;
SELECT * FROM matches
LIMIT 0, 40000;
SELECT * FROM leagues;
SELECT * FROM teams_has_leagues;
SELECT * FROM teams_has_matches
LIMIT 0, 40000;
SELECT * FROM t_errors;
SELECT * FROM links_leagues;
# WHERE link_league = 'https://www.sofascore.com/tournament/basketball/argentina/super-20/10701';
SELECT * FROM statistics;

SELECT * FROM teams
WHERE id_team = 811872;

SELECT * FROM teams_has_matches 
WHERE teams_has_matches.matches_id_match =  171666;


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
FROM teams
WHERE name_team = 'Tinguiririca';

SELECT COUNT(is_win)
FROM matches
WHERE is_win = 0;

SELECT * 
FROM leagues
JOIN t_errors ON leagues.name_league = t_errors.league_error;

SELECT * 
FROM teams
JOIN teams_has_leagues ON teams.id_team = teams_has_leagues.teams_id_team
WHERE teams_has_leagues.leagues_id_league IN (250, 933);
