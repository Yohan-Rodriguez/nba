USE test_mis_marcadores;


# ----------------------------------  
# DROP DATABASE test_mis_marcadores;
# ----------------------------------  

# ----------------------------------  
# DROP SCHEMA analysis_basketball;
# ----------------------------------  

# ----------------------------------  
# DROP TABLE links_leagues;
# ----------------------------------  

# ----------------------------------  
# TRUNCATE leagues;
# ----------------------------------  

# ----------------------------------  
# DELETE FROM t_errors;
# DELETE FROM leagues;
# WHERE link_league = 'https://www.sofascore.com/tournament/basketball/argentina/super-20/10701';
# ----------------------------------  



# ----------------------------------------------------------------------------------------------  
# Eliminar resgistros de una tabala aplicando condicional--------------------------------------- 
# DELETE teams_has_leagues
# FROM teams_has_leagues
# JOIN teams ON teams_has_leagues.teams_id_team = teams.id_team
# WHERE teams_has_leagues.leagues_id_league = 677;
# ----------------------------------------------------------------------------------------------  


# ----------------------------------------------------------------------------------------------  
# Eliminar resgistros en una tabala unión aplicando condicional---------------------------------  
# DELETE teams_has_leagues
# FROM teams_has_leagues
# JOIN teams ON teams_has_leagues.teams_id_team = teams.id_team
# WHERE teams.id_team IN (35059, 188010, 282684, 591619, 727679, 778563, 811987, 959604);

# DELETE teams_has_matches
# FROM teams_has_matches
# JOIN teams ON teams_has_matches.teams_id_team = teams.id_team
# WHERE teams.id_team IN (535364, 561469);
# ----------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------  
# Eliminar resgistros que ya no tiene su P.K. en la tabla unión----------------------------------  
# DELETE matches 
# FROM matches
# LEFT JOIN teams_has_matches ON matches.id_match = teams_has_matches.matches_id_match
# WHERE teams_has_matches.matches_id_match IS NULL;

# DELETE teams 
# FROM teams
# LEFT JOIN teams_has_leagues ON teams.id_team = teams_has_leagues.teams_id_team
# WHERE teams_has_leagues.teams_id_team IS NULL;
# ----------------------------------------------------------------------------------------------  
