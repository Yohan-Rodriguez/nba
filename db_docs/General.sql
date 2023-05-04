USE analysis_basketball_test;
#USE analysis_basketball_2;

SELECT * FROM team
LIMIT 0, 10000;
SELECT * FROM matches;
SELECT * FROM leagues;
SELECT * FROM team_has_leagues;
SELECT * FROM team_has_matches;
SELECT * FROM t_errors;
SELECT * FROM statistics;

SELECT * FROM teams
WHERE name = 'Olympi';

SELECT id_team FROM team
WHERE id_team =  125;

INSERT INTO team (id_team, name_team) VALUES (111, 'WART');

SELECT *
FROM team_has_matches
WHERE team_id_team  IN (
    SELECT team_id_team
    FROM team_has_leagues
);


SELECT *
FROM team_has_leagues
WHERE team_id_team  NOT IN (
    SELECT team_id_team
    FROM team_has_matches
);