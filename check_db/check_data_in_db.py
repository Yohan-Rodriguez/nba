from random import randint
from conn import connections


# ==================================================================================================================== #
# Función para verificar la existencia de "t_team"                                                                     #
# ==================================================================================================================== #
def check_id_team():
    id_team_avaible = 0

    while True:
        # Generar id_team
        id_team_temp = randint(1000, 1000000)
        # Buscar si el ID generado aleatoriamente existe en la "t_team"
        query = f'''SELECT id_team FROM team
                    WHERE id_team =  {id_team_temp}'''

        # "id_team_exists" es una lista con una tupla que contiene el id_team
        id_team_exists = connections.select_row(query)
        # id_team_exists es:
        # id_team_exists = [(id_team,)] :: (id_team_exists[0][0] :: INT), o
        # id_team_exists = []. (No exsite "id_team" con valor "id_team_temp")

        if len(id_team_exists) == 0:
            id_team_avaible = id_team_temp
            break

    return id_team_avaible
# END --------- Función para verificar la existencia de "t_team" ===================================================== #
# ==================================================================================================================== #


# ==================================================================================================================== #
# Función para verificar la existencia de un equipo en "t_team"                                                        #
# ==================================================================================================================== #

def check_name_team(name_team, id_league, home_or_away):
    id_team = 0

    # Buscar si el ID generado aleatoriamente existe en la "t_team"
    query = f'''SELECT name_team FROM team
                WHERE name_team =  "{name_team}"'''

    # "id_name_exists" es una lista con una tupla que contiene el name_team
    id_name_exists = connections.select_row(query)
    # id_name_exists es:
    # id_name_exists = [(name_team,)] :: (id_team_exists[0][0] :: INT), o
    # id_name_exists = []. (No existe "id_team" con valor "id_team_temp")
    leagues_id_league = id_league

    if len(id_name_exists) == 0:
        # Evaluar sí el ID generado "id_team_temp", existe o no en "t_team"
        id_team = check_id_team()
        team_id_team = id_team

        # Enviar data de home a "t_team"
        print(f'Sending data to "analysis_basketball.team" for {home_or_away}.')
        connections.conn_db_table_team(id_team, name_team)

        # Enviar data a "t_team_has_leagues"
        print(f'Sending data to "analysis_basketball.team_has_leagues" for {home_or_away}.')
        connections.conn_db_table_team_has_leagues(team_id_team, leagues_id_league)

    else:
        print(f'El quipo {name_team} ya esta relacionado en "t_teams"')

        # Buscar el ID "id_team" en "t_team" de "name_team"
        query = f'''SELECT id_team FROM team
                    WHERE name_team =  "{name_team}"'''
        team_id_team = connections.select_row(query)[0][0]

    return team_id_team

# END --------- Función para verificar la existencia de un equipo en "t_team" ======================================== #
# ==================================================================================================================== #


# ==================================================================================================================== #
# Función para verificar la existencia de una liga en "t_leagues"                                                      #
# ==================================================================================================================== #
list_names_leagues = []


def check_name_league(name_league):
    # id de la liga (PK)
    id_league = randint(100, 1000)

    # Buscar si el nombre de la liga existe en la "t_leagues"
    query = f'''SELECT name_league FROM leagues
                WHERE name_league =  "{name_league}"'''

    # "id_name_exists" es una lista con una tupla que contiene el name_team
    id_name_exists = connections.select_row(query)
    # id_name_exists es:
    # id_name_exists = [(name_team,)] :: (id_team_exists[0][0] :: INT), o
    # id_name_exists = []. (No exsite "id_team" con valor "id_team_temp")

    if len(id_name_exists) == 0:
        # Enviar data a "t_league"
        print('Sending data to "analysis_basketball.leagues".')
        connections.conn_db_table_leagues(id_league, name_league)
        list_names_leagues.append(name_league)

    else:
        raise Exception(f'La liga {name_league} ya esta relacionado en "t_leagues"')
        # # Buscar el ID "id_league" en "t_team" de "name_team"
        # query = f'''SELECT name_league FROM leagues
        #             WHERE name_league =  "{name_league}"'''
        # name_league_temp = connections.select_row(query)
        # name_league = name_league_temp[0][0]
        # list_names_leagues.append(name_league)
# END --------- Función para verificar la existencia de una liga en "t_leagues" ====================================== #
# ==================================================================================================================== #

# ==================================================================================================================== #
# Función para verificar la existencia de id_match en "t_matches"                                                                     #
# ==================================================================================================================== #
def check_id_match():
    id_match_avaible = 0

    while True:
        id_match_temp = randint(1000, 1000000)
        # Buscar si el ID generado aleatoriamente existe en la "t_team"
        query = f'''SELECT id_match FROM matches
                    WHERE id_match =  {id_match_temp}'''

        # "id_team_exists" es una lista con una tupla que contiene el id_team
        id_team_exists = connections.select_row(query)
        # id_team_exists es:
        # id_team_exists = [(id_team,)] :: (id_team_exists[0][0] :: INT), o
        # id_team_exists = []. (No exsite "id_team" con valor "id_team_temp")

        if len(id_team_exists) == 0:
            id_match_avaible = id_match_temp
            break

    return id_match_avaible
# END --------- Función para verificar la existencia de "t_team" ===================================================== #
# ==================================================================================================================== #