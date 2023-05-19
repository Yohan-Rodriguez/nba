USE analysis_basketball_test_2;
USE test_mis_marcadores;


# ----------------------------------------------------------------------------------------------  
# Buscar si existe la liga de los equipos que estan jugando ------------------------------------  
SELECT *
FROM leagues
ORDER BY name_league;
# ----------------------------------------------------------------------------------------------  


# ----------------------------------------------------------------------------------------------  
# Nombre de los quipos en la liga encontrada ↑↑↑ -----------------------------------------------
SELECT teams.id_team AS ID_TEAM, teams.name_team AS NAME_TEAM
FROM teams
JOIN teams_has_leagues ON teams.id_team = teams_has_leagues.teams_id_team
WHERE teams_has_leagues.leagues_id_league = 6093
ORDER BY teams.name_team ASC;
# ---------------------------------------------------------------------------------------------- 

SET @home = 'Obras';
SET @away = 'Olimpico';


# AVERAGE, DEPENDIENDO SI ES LOCAL O VISITANTE, POR EQUIPO: ------------------------------------
SELECT teams.name_team AS NAME_TEAM, 	   
	   AVG(q_1) AS AVG_Q1, 
       AVG(q_2) AS AVG_Q2, 
       AVG(q_3) AS AVG_Q3, 
       AVG(q_4) AS AVG_Q4, 
       AVG(total_points) AS AVG_TOTAL,
       matches.is_home AS IS_HOME
FROM matches 
JOIN teams_has_matches ON matches.id_match = teams_has_matches.matches_id_match
JOIN teams ON teams_has_matches.teams_id_team = teams.id_team
WHERE (teams.name_team = @home AND is_home = 1)
   OR (teams.name_team = @away AND is_home = 0)
GROUP BY NAME_TEAM, IS_HOME;
# ------------------------------------------------------

# MÁXIMO: ----------------------------------------------
SELECT teams.name_team AS NAME_TEAM,
	   MAX(q_1) as MAX_Q1, 
	   MAX(q_2) as MAX_Q2,
       MAX(q_3) as MAX_Q3,
       MAX(q_4) as MAX_Q4,
       MAX(total_points) as MAX_TOTAL_POINTS
FROM matches 
JOIN teams_has_matches ON matches.id_match = teams_has_matches.matches_id_match
JOIN teams ON teams_has_matches.teams_id_team = teams.id_team
WHERE (teams.name_team = @home AND is_home = 1)
   OR (teams.name_team = @away AND is_home = 0)
GROUP BY NAME_TEAM;

# MÍNIMO:-----------------------------------------------
SELECT teams.name_team AS NAME_TEAM,
	   MIN(q_1) as MIN_Q1, 
	   MIN(q_2) as MIN_Q2,
       MIN(q_3) as MIN_Q3,
       MIN(q_4) as MIN_Q4,
       MIN(total_points) as MIN_TOTAL_POINTS
FROM matches 
JOIN teams_has_matches ON matches.id_match = teams_has_matches.matches_id_match
JOIN teams ON teams_has_matches.teams_id_team = teams.id_team
WHERE (teams.name_team = @home AND is_home = 1)
   OR (teams.name_team = @away AND is_home = 0)
GROUP BY NAME_TEAM;
# ------------------------------------------------------


# ----------------------------------------------------------------------------------------------  
# Puntajes de los equipos en el cuarto 4 -------------------------------------------------------
SELECT q_4 AS Home_Q_4
FROM matches
JOIN teams_has_matches ON matches.id_match = teams_has_matches.matches_id_match
JOIN teams ON teams_has_matches.teams_id_team = teams.id_team
WHERE name_team = @home AND matches.is_home = 1
ORDER BY Q_4 ASC;

SELECT q_4 AS Away_Q_4
FROM matches
JOIN teams_has_matches ON matches.id_match = teams_has_matches.matches_id_match
JOIN teams ON teams_has_matches.teams_id_team = teams.id_team
WHERE name_team = @away AND matches.is_home = 0
ORDER BY Q_4 ASC;
# ----------------------------------------------------------------------------------------------  









# CRETE Vista: -----------------------------------------
CREATE VIEW view_q1 AS (
SELECT q_1
FROM matches
JOIN teams_has_matches ON teams_has_matches.matches_id_match = matches.id_match
JOIN teams ON teams_has_matches.teams_id_team = teams.id_team
WHERE name_team = 'Bilbao' AND is_home = 1)
;
# ------------------------------------------------------
# SELECT * FROM view_q1;
# ------------------------------------------------------

# CRETE Vista: -----------------------------------------
CREATE VIEW view_q2 AS
SELECT q_2
FROM matches
JOIN teams_has_matches ON teams_has_matches.matches_id_match = matches.id_match
JOIN teams ON teams_has_matches.teams_id_team = teams.id_team
WHERE name_team = 'Bilbao' AND is_home = 1;
# ------------------------------------------------------
# SELECT * FROM view_q2;
# ------------------------------------------------------
# CRETE Vista: -----------------------------------------
CREATE VIEW view_q3 AS
SELECT q_3
FROM matches
JOIN teams_has_matches ON teams_has_matches.matches_id_match = matches.id_match
JOIN teams ON teams_has_matches.teams_id_team = teams.id_team
WHERE name_team = 'Bilbao' AND is_home = 1;
# ------------------------------------------------------
# SELECT * FROM view_q3;
# ------------------------------------------------------
# CRETE Vista: -----------------------------------------
CREATE VIEW view_q4 AS
SELECT q_4
FROM matches
JOIN teams_has_matches ON teams_has_matches.matches_id_match = matches.id_match
JOIN teams ON teams_has_matches.teams_id_team = teams.id_team
WHERE name_team = 'Bilbao' AND is_home = 1;
# ------------------------------------------------------
# SELECT * FROM view_q4;
# ------------------------------------------------------

# MEDIANA: ---------------------------------------------
SELECT CAST(AVG(q_1) AS DECIMAL(10,2)) AS MDN_Q1
FROM (
  SELECT q_1, ROW_NUMBER() OVER (ORDER BY q_1) AS row_num_q1, COUNT(*) OVER () AS total_rows_q1
  FROM view_q1
) ranked
WHERE row_num_q1 IN (FLOOR((total_rows_q1 + 1) / 2), CEIL((total_rows_q1 + 1) / 2));
# ------------------------------------------------------

# DELETE VISTA: ----------------------------------------
DROP VIEW view_q1;
# ------------------------------------------------------






# ----------------------------------------------------------------------------------------------  
# El equipo SI supera su media del Q_4 CUANDO: -------------------------------------------------
SET @home = 'Philadelphia 76ers';
SET @away = 'Boston Celtics';


# ----------------------------------------------------------------------------------------------  
# AVG(Q_4): ------------------------------------------------------------------------------------
SELECT AVG(q_4) AS AVG_Q4
				FROM matches 
				JOIN teams_has_matches ON matches.id_match = teams_has_matches.matches_id_match
				JOIN teams ON teams_has_matches.teams_id_team = teams.id_team
				WHERE (teams.name_team = @home AND is_home = 1);

# ----------------------------------------------------------------------------------------------  
# Puntos en Q_1 > AVG(Q_4): --------------------------------------------------------------------
SELECT q_1 AS Q1_HOME_MAYOR_A_AVG_Q4_HOME
FROM matches
JOIN teams_has_matches ON matches.id_match = teams_has_matches.matches_id_match
JOIN teams ON teams_has_matches.teams_id_team = teams.id_team
WHERE teams.name_team = @home 
  AND matches.q_4 > (
					SELECT AVG(q_4) AS AVG_Q4
					FROM matches 
					JOIN teams_has_matches ON matches.id_match = teams_has_matches.matches_id_match
					JOIN teams ON teams_has_matches.teams_id_team = teams.id_team
					WHERE (teams.name_team = @home AND is_home = 1)
					GROUP BY teams.name_team)
ORDER BY q_1 ASC;

# ----------------------------------------------------------------------------------------------  
# Puntos en Q_2 > AVG(Q_4): --------------------------------------------------------------------
SELECT q_2 AS Q2_HOME_MAYOR_A_AVG_Q4_HOME
FROM matches
JOIN teams_has_matches ON matches.id_match = teams_has_matches.matches_id_match
JOIN teams ON teams_has_matches.teams_id_team = teams.id_team
WHERE teams.name_team = @home 
  AND matches.q_4 > (
					SELECT AVG(q_4) AS AVG_Q4
					FROM matches 
					JOIN teams_has_matches ON matches.id_match = teams_has_matches.matches_id_match
					JOIN teams ON teams_has_matches.teams_id_team = teams.id_team
					WHERE (teams.name_team = @home AND is_home = 1)
					GROUP BY teams.name_team)
ORDER BY q_2 ASC;

# ----------------------------------------------------------------------------------------------  
# Puntos en Q_3 > AVG(Q_4): --------------------------------------------------------------------
SELECT q_3 AS Q3_HOME_MAYOR_A_AVG_Q4_HOME
FROM matches
JOIN teams_has_matches ON matches.id_match = teams_has_matches.matches_id_match
JOIN teams ON teams_has_matches.teams_id_team = teams.id_team
WHERE teams.name_team = @home 
  AND matches.q_4 > (
					SELECT AVG(q_4) AS AVG_Q4
					FROM matches 
					JOIN teams_has_matches ON matches.id_match = teams_has_matches.matches_id_match
					JOIN teams ON teams_has_matches.teams_id_team = teams.id_team
					WHERE (teams.name_team = @home AND is_home = 1)
					GROUP BY teams.name_team)
ORDER BY q_3 ASC;













# ----------------------------------------------------------------------------------------------  
# DIFERENCIA DE PUNTOS EN Q_3 ES POSITIVA Y ES > AVG(Q_4): -------------------------------------
SELECT q_3 AS Q_3_HOME
FROM matches
JOIN teams_has_matches ON matches.id_match = teams_has_matches.matches_id_match
JOIN teams ON teams_has_matches.teams_id_team = teams.id_team
WHERE (teams.name_team = @home AND is_home = 1)
;#ORDER BY Q_3_HOME;

SELECT q_3 AS Q_3_AWAY
FROM matches
JOIN teams_has_matches ON matches.id_match = teams_has_matches.matches_id_match
JOIN teams ON teams_has_matches.teams_id_team = teams.id_team
WHERE (teams.name_team = @away AND is_home = 0)
;#ORDER BY Q_3_AWAY;
