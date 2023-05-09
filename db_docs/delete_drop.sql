use analysis_basketball_2;

# ----------------------------------  
# DROP DATABASE statistics_test;
# ----------------------------------  

# ----------------------------------  
# DROP SCHEMA analysis_basketball;
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
# DELETE teams
# FROM teams
# WHERE name_team IN ('U de Concepción', 'Leones Quilpué', 'ABA Ancud', 'Puente Alto',
# 					'Deportivo Valdivia', 'CD Las Ánimas', 'Español Osorno', 'Quilicura Basket',
#                     'Deportes Castro', 'Puerto Varas', 'Puerto Montt', 'Universidad Católica', 'Español de Talca',
#                     'Tinguiririca', 'Temuco');
# ----------------------------------------------------------------------------------------------  
# DELETE leagues
# FROM leagues
# WHERE id_league = 466;



# ----------------------------------------------------------------------------------------------  
# Eliminar resgistros en una tabala unión aplicando consicional----------------------------------  
# DELETE teams_has_leagues
# FROM teams_has_leagues
# JOIN teams ON teams_has_leagues.teams_id_team = teams.id_team
# WHERE teams.id_team IN (35059, 188010, 282684, 591619, 727679, 778563, 811987, 959604);
# ----------------------------------------------------------------------------------------------
# DELETE teams_has_matches
# FROM teams_has_matches
# JOIN teams ON teams_has_matches.teams_id_team = teams.id_team
# WHERE name_team IN ('U de Concepción', 'Leones Quilpué', 'ABA Ancud', 'Puente Alto',
# 					'Deportivo Valdivia', 'CD Las Ánimas', 'Español Osorno', 'Quilicura Basket',
#                     'Deportes Castro', 'Puerto Varas', 'Puerto Montt', 'Universidad Católica', 'Español de Talca',
#                     'Tinguiririca', 'Temuco');
