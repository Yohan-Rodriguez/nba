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
# ----------------------------------------------------------------------------------------------------------
INSERT INTO t_errors (league_error, description_error)
VALUES ('greece - elite-league', 'Incomplete data - There are matches without points per quarter');


DELETE teams_has_matches
FROM teams_has_matches
JOIN teams ON teams_has_matches.teams_id_team = teams.id_team
WHERE teams.id_team IN (964404, 963889, 948686, 941421, 936972, 803257, 689413, 686698, 541953, 407566, 290275, 250272, 13285, 5000);


DELETE matches 
FROM matches
LEFT JOIN teams_has_matches ON matches.id_match = teams_has_matches.matches_id_match
WHERE teams_has_matches.matches_id_match IS NULL;


DELETE teams_has_leagues
FROM teams_has_leagues
JOIN teams ON teams_has_leagues.teams_id_team = teams.id_team
WHERE teams_has_leagues.leagues_id_league = 4062;


DELETE teams 
FROM teams
LEFT JOIN teams_has_leagues ON teams.id_team = teams_has_leagues.teams_id_team
WHERE teams_has_leagues.teams_id_team IS NULL;

DELETE leagues
FROM leagues
WHERE id_league = 4062;