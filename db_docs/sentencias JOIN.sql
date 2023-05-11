USE ANALYSIS_BASKETBALL_2;

# ----------------------------------------------------------------------------------------------------------
# CANTIDAD DE EQUIPOS Y PARTIDOS POR LIGA -----------------------------------------------------------------------------
SELECT leagues.name_league AS NAME_LEAGUE, leagues.id_league AS ID_LEAGUE, COUNT(teams.id_team) AS AMOUNT_TEAM,
    (
        SELECT COUNT(matches.id_match) 
        FROM matches 
        JOIN teams_has_matches ON matches.id_match = teams_has_matches.matches_id_match 
        WHERE teams_has_matches.teams_id_team IN (
            SELECT teams_has_leagues.teams_id_team 
            FROM teams_has_leagues 
            WHERE teams_has_leagues.leagues_id_league = leagues.id_league
        )
    ) AS AMOUNT_MATCH
FROM leagues
INNER JOIN teams_has_leagues AS t_l ON leagues.id_league = t_l.leagues_id_league
INNER JOIN teams ON teams.id_team = t_l.teams_id_team
GROUP BY leagues.id_league
ORDER BY AMOUNT_TEAM, AMOUNT_MATCH ASC;
# ----------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------
# NOMBRE DE LOS EQUIPOS EN UNA LIGA EN PARTÍCULAR ----------------------------------------------------------
SELECT teams.name_team AS NAME_TEAM, teams.id_team AS ID_TEAM, leagues.name_league AS NAME_LEAGUE, leagues.id_league AS ID_LEAGUE
FROM leagues
INNER JOIN teams_has_leagues ON leagues.id_league = teams_has_leagues.leagues_id_league
INNER JOIN teams ON teams.id_team = teams_has_leagues.teams_id_team
WHERE leagues.name_league = 'brazil - nbb';
# ----------------------------------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------------------  
# Seleccionar valores nulos --------------------------------------------------------------------  
SELECT * 
FROM matches
LEFT JOIN teams_has_matches ON matches.id_match = teams_has_matches.matches_id_match
WHERE teams_has_matches.matches_id_match IS NULL;


SELECT * 
FROM teams
LEFT JOIN teams_has_leagues ON teams.id_team = teams_has_leagues.teams_id_team
WHERE teams_has_leagues.teams_id_team IS NULL;
# ----------------------------------------------------------------------------------------------  



# ----------------------------------------------------------------------------------------------  
# Seleccionar equipos de una liga seleccionada -------------------------------------------------  
SELECT teams.id_team AS ID_TEAM, teams.name_team AS NAME_TEAM 
FROM teams
JOIN teams_has_leagues ON teams.id_team = teams_has_leagues.teams_id_team
WHERE teams_has_leagues.leagues_id_league = 8368;
# ----------------------------------------------------------------------------------------------  



# ----------------------------------------------------------------------------------------------  
# Seleccionar equipos de una liga seleccionada --------------------------------------------------  
SELECT COUNT(*) 
FROM matches
JOIN teams_has_matches ON matches.id_match = teams_has_matches.matches_id_match
WHERE teams_has_matches.teams_id_team IN (964404, 963889, 948686, 941421, 936972, 803257, 689413, 686698, 541953, 407566, 290275, 250272, 13285, 5000);	
# ----------------------------------------------------------------------------------------------  





SELECT teams.name_team AS NAME_TEAM, COUNT(teams_has_leagues.leagues_id_league) AS AMOUNT_LEAGUE
FROM teams
JOIN teams_has_leagues ON teams.id_team = teams_has_leagues.teams_id_team
GROUP BY NAME_TEAM
HAVING AMOUNT_LEAGUE > 0;
