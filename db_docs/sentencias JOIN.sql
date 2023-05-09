USE ANALYSIS_BASKETBALL_2;
# ----------------------------------------------------------------------------------------------------------
# CANTIDAD DE EQUIPOS POR LIGA -----------------------------------------------------------------------------
SELECT leagues.name_league AS NAME_LEAGUE, leagues.id_league AS ID_LEAGUE, COUNT(teams.id_team) AS AMOUNT_TEAM
FROM leagues
INNER JOIN teams_has_leagues AS t_l ON leagues.id_league =  t_l.leagues_id_league
INNER JOIN teams ON teams.id_team = t_l.teams_id_team
GROUP BY leagues.id_league;
# ----------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------
# NOMBRE DE LOS EQUIPOS EN UNA LIGA EN PARTÍCULAR ----------------------------------------------------------
SELECT teams.name_team AS NAME_TEAM, teams.id_team AS ID_TEAM, leagues.name_league AS NAME_LEAGUE, leagues.id_league AS ID_LEAGUE
FROM leagues
INNER JOIN teams_has_leagues ON leagues.id_league = teams_has_leagues.leagues_id_league
INNER JOIN teams ON teams.id_team = teams_has_leagues.teams_id_team
WHERE leagues.name_league = 'brazil - nbb';
# ----------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------
SELECT * FROM team_has_leagues
WHERE teams_id_team = 262035;
# ----------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------
# ??????????????????????????????????????????????? ----------------------------------------------------------
SELECT teams.id_team AS ID_TEAM, teams.name_team AS NAME_TEAM
FROM teams
LEFT JOIN teams_has_leagues ON teams.id_team = teams_has_leagues.teams_id_team
WHERE teams_has_leagues.teams_id_team IS NULL;
# ----------------------------------------------------------------------------------------------------------


SELECT team.id_team
FROM team
FULL JOIN team_has_leagues ON team; 

SELECT  *
FROM teams
WHERE name_team = 'Helios';

SELECT teams.name_team AS TEAM, COUNT(teams_has_leagues.leagues_id_league) AS AMOUNT_LEAGUE
FROM teams
INNER JOIN teams_has_leagues ON teams.id_team = teams_has_leagues.teams_id_team
GROUP BY TEAM
HAVING AMOUNT_LEAGUE > 0;

DELETE FROM teams_has_matches
WHERE teams_id_team = 35059 OR 188010 OR 282684 OR 591619 OR 727679 OR 778563 OR 811987 OR 959604;

DELETE teams
FROM teams
JOIN teams_has_matches ON teams.id_team = teams_has_matches.teams_id_team
WHERE teams_has_matches.teams_id_team = 35059 OR 188010 OR 282684 OR 591619 OR 727679 OR 778563 OR 811987 OR 959604;

DELETE teams_has_leagues
FROM teams_has_leagues
JOIN teams ON teams_has_leagues.teams_id_team = teams.id_team
WHERE teams.id_team IN (35059, 188010, 282684, 591619, 727679, 778563, 811987, 959604);



