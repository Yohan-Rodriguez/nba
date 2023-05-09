from random import randint
from conn.connections import conn_db_table_teams_has_leagues as conn_db_teams_has_leagues
from history_match.functions_shared import select_row as fs_select_row
from conn.connections import conn_db_table_leagues as conn_db_leagues
from conn.connections import conn_db_table_teams as conn_db_teams


# ==================================================================================================================== #
# Función para verificar la existencia de "id_team" en "t_team"                                                        #
# ==================================================================================================================== #
# Esta función es llamada solo en este mismo archivo (check_data_in_db.py)
def check_id_team():
    id_team_avaible = 0

    while True:
        # Generar id_team
        id_team_temp = randint(1000, 1000000)
        # Buscar si el ID generado aleatoriamente existe en la "t_team"
        query = f'''SELECT id_team FROM teams
                    WHERE id_team =  {id_team_temp}'''

        # "id_team_exists" es una lista con una tupla que contiene el id_team
        id_team_exists = fs_select_row(query)
        # id_team_exists es:
        # id_team_exists = [(id_team,)] :: (id_team_exists[0][0] :: INT), o
        # id_team_exists = []. (No exsite "id_team" con valor "id_team_temp")

        if len(id_team_exists) == 0:
            id_team_avaible = id_team_temp
            break

    del id_team_exists
    del id_team_temp
    del query

    return id_team_avaible
# END --------- Función para verificar la existencia de "id_team" en "t_team" ======================================== #
# ==================================================================================================================== #


# ==================================================================================================================== #
# Función para verificar la existencia de un equipo en "t_team"                                                        #
# ==================================================================================================================== #
# Esta función es llamada en un arhivo externo (prepare_and_data_send_data.py)
def check_name_team(name_team, id_league, home_or_away):
    # Buscar si el ID generado aleatoriamente existe en la "t_team"
    query = f'''SELECT name_team FROM teams
                WHERE name_team =  "{name_team}"'''

    # "id_name_exists" es una lista con una tupla que contiene el name_team
    id_name_exists = fs_select_row(query)
    # id_name_exists es:
    # id_name_exists = [(name_team,)] :: (id_team_exists[0][0] :: INT), o
    # id_name_exists = []. (No existe "id_team" con valor "id_team_temp")
    leagues_id_league = id_league

    if len(id_name_exists) == 0:
        # Evaluar sí el ID generado "id_team_temp", existe o no en "t_team"
        id_team = check_id_team()
        teams_id_team = id_team

        # Enviar data de home a "t_team"
        print(f'Sending data to "analysis_basketball.team" for {home_or_away}.')
        conn_db_teams(id_team, name_team)

        # Enviar data a "t_teams_has_leagues"
        print(f'Sending data to "analysis_basketball.teams_has_leagues" for {home_or_away}.')
        conn_db_teams_has_leagues(teams_id_team, leagues_id_league)

    else:
        print(f'El quipo {name_team} ya esta relacionado en "t_teams"')

        # Buscar sí existe en "teams_has_leagues" el registro de
        # "leagues_id_league = liga actual" y
        # "teams_id_team = id_team del equipo que si existe (id_name_exists). Equipo actual"
        query = f'''SELECT * 
                    FROM teams_has_leagues
                    WHERE leagues_id_league = {id_league} AND teams_id_team = 
                    (
                        SELECT id_team FROM teams
                        WHERE name_team = '{id_name_exists[0][0]}'
                    );'''

        # "exists_id_teams_has_leagues" es una lista con una tupla que contiene la existencia o no
        # del registro en "teams_has_leagues" del "team actual con liga actual"
        exists_id_teams_has_leagues = fs_select_row(query)

        # Buscar el ID "id_team" en "t_team" de "name_team"
        # para posteriormente, guardar este valor en la tabla unión "team_has_matches".
        query = f'''SELECT id_team FROM teams
                    WHERE name_team =  "{name_team}"'''
        teams_id_team = fs_select_row(query)[0][0]

        if len(exists_id_teams_has_leagues) == 0:
            # Enviar data a "t_teams_has_leagues"
            print(f'Sending data to "analysis_basketball.teams_has_leagues" for {home_or_away}.')
            conn_db_teams_has_leagues(teams_id_team, leagues_id_league)

    del exists_id_teams_has_leagues
    del id_name_exists
    del leagues_id_league
    del query
    del id_team

    return teams_id_team

# END --------- Función para verificar la existencia de un equipo en "t_team" ======================================== #
# ==================================================================================================================== #


# ==================================================================================================================== #
# Función para verificar la existencia de una liga en "t_leagues"                                                      #
# ==================================================================================================================== #
list_names_leagues = []


# Esta función es llamada en un archivo externo (load_history.py)
def check_name_league(name_league):
    # id de la liga (PK)
    id_league = randint(100, 1000)

    # Buscar si el nombre de la liga existe en la "t_leagues"
    query = f'''SELECT name_league FROM leagues
                WHERE name_league =  "{name_league}"'''

    # "id_name_exists" es una lista con una tupla que contiene el name_team
    id_name_exists = fs_select_row(query)
    # id_name_exists es:
    # id_name_exists = [(name_team,)] :: (id_team_exists[0][0] :: INT), o
    # id_name_exists = []. (No exsite "id_team" con valor "id_team_temp")

    if len(id_name_exists) == 0:
        # Enviar data a "t_league"
        print('Sending data to "analysis_basketball.leagues".')
        conn_db_leagues(id_league, name_league)
        list_names_leagues.append(name_league)

    else:
        raise Exception(f'X*X*X*X* INTENTIONAL EXCEPTION X*X*X*X*\n\tLa liga {name_league} ya esta relacionado en "t_leagues"')
        # # Buscar el ID "id_league" en "t_team" de "name_team"
        # query = f'''SELECT name_league FROM leagues
        #             WHERE name_league =  "{name_league}"'''
        # name_league_temp = connections.fs_select_row(query)
        # name_league = name_league_temp[0][0]
        # list_names_leagues.append(name_league)

    del id_league
    del query
    del id_name_exists
# END --------- Función para verificar la existencia de una liga en "t_leagues" ====================================== #
# ==================================================================================================================== #

# ==================================================================================================================== #
# Función para verificar la existencia de id_match en "t_matches"                                                      #
# ==================================================================================================================== #
# Esta función es llamada en un archivo externo (prepare_and_data_send_data.py)
def check_id_match():
    id_match_avaible = 0

    while True:
        id_match_temp = randint(1000, 1000000)
        # Buscar si el ID generado aleatoriamente existe en la "t_team"
        query = f'''SELECT id_match FROM matches
                    WHERE id_match =  {id_match_temp}'''

        # "id_team_exists" es una lista con una tupla que contiene el id_team
        id_team_exists = fs_select_row(query)
        del query
        # id_team_exists es:
        # id_team_exists = [(id_team,)] :: (id_team_exists[0][0] :: INT), o
        # id_team_exists = []. (No existe "id_team" con valor "id_team_temp")

        if len(id_team_exists) == 0:
            id_match_avaible = id_match_temp
            break

    del query
    del id_match_temp
    del id_team_exists

    return id_match_avaible
# END --------- Función para verificar la existencia de "t_team" ===================================================== #
# ==================================================================================================================== #