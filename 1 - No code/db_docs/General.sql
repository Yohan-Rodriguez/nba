USE analysis_basketball_2;

SELECT * FROM teams;
SELECT * FROM leagues;
SELECT * FROM matches;
SELECT * FROM gral_statistics;
SELECT * FROM match_statistics
LIMIT 1000;

SELECT * 
FROM matches
JOIN teams_has_matches ON matches.id_match = teams_has_matches.matches_id_match
WHERE teams_has_matches.teams_id_team = 644511;

select * 
FROM teams
WHERE id_team = 644511;

select * 
FROM teams
WHERE name_team = 'Decin';