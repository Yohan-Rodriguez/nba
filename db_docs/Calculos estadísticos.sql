USE analysis_basketball;

# AVERAGE: --------------------------------------------
SELECT AVG(q_1) AS Average
FROM teams 
WHERE name = "76ers" AND is_home = 1;
# ------------------------------------------------------

# MÁXIMO: ----------------------------------------------
SELECT MAX(q_1) as Max
FROM teams 
WHERE name = "76ers" AND is_home = 0;

# MÍNIMO:-----------------------------------------------
SELECT MIN(q_1) AS Min
FROM teams 
WHERE name = "76ers" AND is_home = 0;
#LIMIT 10000;
# ------------------------------------------------------

# CRETE Vista: -----------------------------------------
CREATE VIEW view_1 AS
SELECT q_1
FROM teams
WHERE name = '76ers' AND is_home = 0;
# ------------------------------------------------------
#SELECT * FROM view_1;
# ------------------------------------------------------

# MEDIANA: ---------------------------------------------
SELECT CAST(AVG(q_1) AS DECIMAL(10,2)) AS Mediana
FROM (
  SELECT q_1, ROW_NUMBER() OVER (ORDER BY q_1) AS row_num, COUNT(*) OVER () AS total_rows
  FROM view_1
) ranked
WHERE row_num IN (FLOOR((total_rows + 1) / 2), CEIL((total_rows + 1) / 2));
# ------------------------------------------------------

# DELETE VISTA: ----------------------------------------
DROP VIEW view_1;
# ------------------------------------------------------

SELECT DISTINCT (name)
FROM teams
WHERE leagues_id_league = 819;

SELECT name, is_home, total_points, q_1, q_2, q_3, q_4, is_win
FROM teams
WHERE leagues_id_league = 819
ORDER BY name ASC;
