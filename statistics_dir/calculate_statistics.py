import pandas as pd
from conn.connections import conn_insert_table_gral_statistics as conn_insert_statistics
from conn.conn_functions_shared import select_row as fs_select_row
from check_db_and_controllers.check_data_in_db import check_id_statistics as check_id_statis
from statistics_dir.statistics_functions_shared import show_options

list_quarters = ['q_1', 'q_2', 'q_3', 'q_4']


def calc_statistics_quarters(df_data_teams, i_name, i_q, i_ishome):
    # ================================================================================================================ #
    # CALCULATE AVG                                                                                                    #
    # ================================================================================================================ #
    # AVG de un cuarto específico (i_q) del equipo específico ({i_name}),
    # y si es local o visitante (con máximo, 5 decimas).
    avg_q_i = round(df_data_teams.loc[(df_data_teams['name'] == f'{i_name}') & (df_data_teams['is_home'] == i_ishome), f'{i_q}'].mean(), 5)
    # END --------- CALCULATE AVG                                                                                  # # #
    # # ============================================================================================================== #

    # ================================================================================================================ #
    # CALCULATE MEDIAN                                                                                                 #
    # ================================================================================================================ #
    # MEDIANA de un cuarto específico (i_q) del equipo específico ({i_name}),
    # y si es local o visitante (con máximo, 5 decimas).
    mdn_q_i = round(df_data_teams.loc[(df_data_teams['name'] == f'{i_name}') & (df_data_teams['is_home'] == i_ishome), f'{i_q}'].median(), 5)
    # END --------- MEDIAN                                                                                         # # #
    # # ============================================================================================================== #

    # ================================================================================================================ #
    # CALCULATE MAX                                                                                                    #
    # ================================================================================================================ #
    # MÁXIMO de un cuarto específico (i_q) del equipo específico ({i_name}),
    # y si es local o visitante (con máximo, 5 decimas).
    max_q_i = round(df_data_teams.loc[(df_data_teams['name'] == f'{i_name}') & (df_data_teams['is_home'] == i_ishome), f'{i_q}'].max(), 5)
    # END --------- MAX                                                                                            # # #
    # # ============================================================================================================== #

    # ================================================================================================================ #
    # CALCULATE MIN                                                                                                    #
    # ================================================================================================================ #
    # MÍNIMO de un cuarto específico (i_q) del equipo específico ({i_name}),
    # y si es local o visitante (con máximo, 5 decimas).
    min_q_i = round(df_data_teams.loc[(df_data_teams['name'] == f'{i_name}') & (df_data_teams['is_home'] == i_ishome), f'{i_q}'].min(), 5)
    # END --------- MIN                                                                                            # # #
    # # ============================================================================================================== #
    
    return avg_q_i, mdn_q_i, max_q_i, min_q_i
    
    
def calc_statistics_total_is_home(df_data_teams, i_name, i_ishome):
    # ================================================================================================================ #
    # CALCULATE AVG                                                                                                    #
    # ================================================================================================================ #    
    # AVG total del equipo específico ({i_name}),
    # y si es local o visitante (con máximo, 5 decimas).
    avg_gral_ishome = round(df_data_teams.loc[(df_data_teams['name'] == f'{i_name}') & (df_data_teams['is_home'] == i_ishome), 'total_points'].mean(), 5)
    # END --------- CALCULATE AVG                                                                                  # # #
    # # ============================================================================================================== #

    # ================================================================================================================ #
    # CALCULATE MEDIAN                                                                                                 #
    # ================================================================================================================ #
    # MEDIANA total del equipo específico ({i_name}),
    # y si es local o visitante (con máximo, 5 decimas).
    mdn_gral_ishome = round(df_data_teams.loc[(df_data_teams['name'] == f'{i_name}') & (df_data_teams['is_home'] == i_ishome), 'total_points'].median(), 5)
    # END --------- MEDIAN                                                                                         # # #
    # # ============================================================================================================== #

    # ================================================================================================================ #
    # CALCULATE MAX                                                                                                    #
    # ================================================================================================================ #
    # MÁXIMO total del equipo específico ({i_name}),
    # y si es local o visitante (con máximo, 5 decimas).
    max_gral_ishome = round(df_data_teams.loc[(df_data_teams['name'] == f'{i_name}') & (df_data_teams['is_home'] == i_ishome), 'total_points'].max(), 5)
    # END --------- MAX                                                                                            # # #
    # # ============================================================================================================== #

    # ================================================================================================================ #
    # CALCULATE MIN                                                                                                    #
    # ================================================================================================================ #
    # MÍNIMO total del equipo específico ({i_name}),
    # y si es local o visitante (con máximo, 5 decimas).
    min_gral_ishome = round(df_data_teams.loc[(df_data_teams['name'] == f'{i_name}') & (df_data_teams['is_home'] == i_ishome), 'total_points'].min(), 5)
    # END --------- MIN                                                                                            # # #
    # # ============================================================================================================== #
    
    return avg_gral_ishome, mdn_gral_ishome, max_gral_ishome, min_gral_ishome
    

def calc_statistics_totals(df_data_teams, i_name):
    # ================================================================================================================ #
    # CALCULATE AVG                                                                                                    #
    # ================================================================================================================ #
    # AVG total del equipo específico ({i_name}), con máximo, 5 decimas.
    avg_gral = round(df_data_teams.loc[(df_data_teams['name'] == f'{i_name}'), 'total_points'].mean(), 5)        
    # END --------- CALCULATE AVG                                                                                  # # #
    # # ============================================================================================================== #

    # ================================================================================================================ #
    # CALCULATE MEDIAN                                                                                                 #
    # ================================================================================================================ #
    # MEDIANA total del equipo específico ({i_name}), con máximo, 5 decimas.
    mdn_gral = round(df_data_teams.loc[(df_data_teams['name'] == f'{i_name}'), 'total_points'].median(), 5)
    # END --------- MEDIAN                                                                                         # # #
    # # ============================================================================================================== #

    # ================================================================================================================ #
    # CALCULATE MAX                                                                                                    #
    # ================================================================================================================ #
    # MÁXIMO total del equipo específico ({i_name}), con máximo, 5 decimas.
    max_gral = round(df_data_teams.loc[(df_data_teams['name'] == f'{i_name}'), 'total_points'].max(), 5)
    # END --------- MAX                                                                                            # # #
    # # ============================================================================================================== #

    # ================================================================================================================ #
    # CALCULATE MIN                                                                                                    #
    # ================================================================================================================ #
    # MÍNIMO total del equipo específico ({i_name}), con máximo, 5 decimas.
    min_gral = round(df_data_teams.loc[(df_data_teams['name'] == f'{i_name}'), 'total_points'].min(), 5)
    # END --------- MIN                                                                                            # # #
    # # ============================================================================================================== #
    
    return avg_gral, mdn_gral, max_gral, min_gral


# ==================================================================================================================== #
# CALCULATE STATISTICS                                                                                                 #
# ==================================================================================================================== #
def calculate_statistics_all_teams_in_unique_league(result_data, id_league):
    # Lista para almacenar los datos a enviar a la DB
    list_statistics_teams = []

    # Crear el DataFrame a partir de la lista de tuplas recibida en la función.
    df_data_teams = pd.DataFrame(data=result_data, columns=['name', 'is_home', 'total_points', 'q_1', 'q_2', 'q_3', 'q_4', 'is_win']).dropna()
    print(df_data_teams)
    # Crear una lista con los nombres (sin repetir [.unique()]) de todos los equipos de la liga actual.
    names_teams = df_data_teams['name'].unique()
    print(names_teams)

    # Iterar sobre cada la lista de nombres de equipos.
    for i_name in names_teams:
        # Generar id nuevo del registro nuevo.
        id_statistics = check_id_statis()

        # Guardar el ID generado,
        # que será almacenado en la columna "id_statistics" de "t_statistics"
        list_statistics_teams.append(id_statistics)

        # Buscar ID del equipo actual "i_name"
        query = f'''SELECT id_team 
                    FROM teams
                    WHERE name_team = "{i_name}"'''
        current_id_team = fs_select_row(query)[0][0]

        # Guardar ID del equipo liga,
        # que será almacenado en la columna "teams_has_leagues_teams_id_team" de "t_statistics"
        list_statistics_teams.append(current_id_team)

        # Guardar ID de la liga,
        # que será almacenado en la columna "leagues_id_league" de "t_statistics"
        list_statistics_teams.append(id_league)

        # Iterar en 2 ocasiones:
        # 0 para is_home = 0
        # 0 para is_home = 1
        for i_ishome in range(2):
            # Iterar 4 veces "list_quarters = ['q_1', 'q_2', 'q_3', 'q_4']"
            for i_q in list_quarters:
                # Enviar datos para calcular las estadísticas por cuartos, condicionados a si es local o visitante.
                list_statistics_teams.append(calc_statistics_quarters(df_data_teams, i_name, i_q, i_ishome))

            # Enviar datos para calcular las estadísticas generales, condicionados a si es local o visitantes.
            list_statistics_teams.append(calc_statistics_total_is_home(df_data_teams, i_name, i_ishome))

        # Enviar datos para calcular las estadísticas generales.
        list_statistics_teams.append(calc_statistics_totals(df_data_teams, i_name))

    # for i in list_statistics_teams:
    #     print(i)

    # Enviar cada grupo de calculos estadísticos almacenados en "list_statistics_teams"
    # (-14) para evitar exception al iterar sobre la última posición de "list_statistics_teams"
    for i_sent in range(-14, len(list_statistics_teams)-14, 14):
        try:
            print(f'Sending data to "analysis_basketball.statistics for id_team: {list_statistics_teams[i_sent + 15]}')

            # list_statistics_teams[i_sent+23][3], list_statistics_teams[i_sent+15][0],
            conn_insert_statistics(list_statistics_teams[i_sent + 14], list_statistics_teams[i_sent + 15],
                                   list_statistics_teams[i_sent + 16], list_statistics_teams[i_sent + 27][0],
                                   list_statistics_teams[i_sent+27][1], list_statistics_teams[i_sent+27][2],
                                   list_statistics_teams[i_sent+27][3], list_statistics_teams[i_sent+26][0],
                                   list_statistics_teams[i_sent+26][1], list_statistics_teams[i_sent+26][2],
                                   list_statistics_teams[i_sent+26][3], list_statistics_teams[i_sent+21][0],
                                   list_statistics_teams[i_sent+21][1], list_statistics_teams[i_sent+21][2],
                                   list_statistics_teams[i_sent+21][3], list_statistics_teams[i_sent+22][0],
                                   list_statistics_teams[i_sent+22][1], list_statistics_teams[i_sent+22][2],
                                   list_statistics_teams[i_sent+22][3], list_statistics_teams[i_sent+23][0],
                                   list_statistics_teams[i_sent+23][1], list_statistics_teams[i_sent+23][2],
                                   list_statistics_teams[i_sent+23][3], list_statistics_teams[i_sent+24][0],
                                   list_statistics_teams[i_sent+24][1], list_statistics_teams[i_sent+24][2],
                                   list_statistics_teams[i_sent+24][3], list_statistics_teams[i_sent+25][0],
                                   list_statistics_teams[i_sent+25][1], list_statistics_teams[i_sent+25][2],
                                   list_statistics_teams[i_sent+25][3], list_statistics_teams[i_sent+17][0],
                                   list_statistics_teams[i_sent+17][1], list_statistics_teams[i_sent+17][2],
                                   list_statistics_teams[i_sent+17][3], list_statistics_teams[i_sent+18][0],
                                   list_statistics_teams[i_sent+18][1], list_statistics_teams[i_sent+18][2],
                                   list_statistics_teams[i_sent+18][3], list_statistics_teams[i_sent+19][0],
                                   list_statistics_teams[i_sent+19][1], list_statistics_teams[i_sent+19][2],
                                   list_statistics_teams[i_sent+19][3], list_statistics_teams[i_sent+20][0],
                                   list_statistics_teams[i_sent+20][1], list_statistics_teams[i_sent+20][2],
                                   list_statistics_teams[i_sent+20][3])
            # list_statistics_teams[0] = id_statistics, # list_statistics_teams[1] = teams_has_leagues_teams_id_team,
            # list_statistics_teams[2] = teams_has_leagues_leagues_id_league, list_statistics_teams[12] = Gral,
            # list_statistics_teams[12] = Gral Home, list_statistics_teams[7] = Gral Away,
            # list_statistics_teams[8:12][:] = q_i Home, list_statistics_teams[3:7][:] = q_i Away
            # Ejemplo:
            # [0]  id_statistics = 1256
            # [1]  teams_id_team = 9841
            # [2]  leagues_id_league = 2484
            # [3]  Q_1 AWAY =  (16.84211, 16.0, 27, 4)
            # [4]  Q_2 AWAY =  (15.36842, 16.0, 24, 8)
            # [5]  Q_3 AWAY =  (17.36842, 17.0, 26, 8)
            # [6]  Q_4 AWAY =  (19.10526, 20.0, 26, 8)
            # [7]  AWAY_GRAL = (79.70566, 80.0, 122, 47)
            # [8]  Q_1 home =  (19.05263, 20.0, 31, 7)
            # [9]  Q_2 home =  (17.10526, 16.0, 29, 7)
            # [10]  Q_3 home =  (20.73684, 21.0, 28, 12)
            # [11]  Q_4 home =  (20.47368, 21.0, 27, 13)
            # [12]  HOME_GRAL = (77.36842, 76.0, 104, 62)
            # [13]  GENERAL = (73.02632, 72.0, 104, 47)

        except Exception as e:
            print(f'EXCEPTION IN send data to "t_gral_tatatistics"\n{e}')

        finally:
            list_statistics_teams.clear()
# END --------- CALCULATE STATISTICS                                                                               # # #
# # ================================================================================================================== #


# ==================================================================================================================== #
# CALCULATE STATISTICS                                                                                                 #
# ==================================================================================================================== #
def calculate_statistics_one_team_in_unique_league(result_data_one_team, id_league, name_team):
    # Lista para almacenar los datos a enviar a la DB
    list_statistics_team = []

    # Crear el DataFrame a partir de la lista de tuplas recibida en la función.
    df_data_one_team = pd.DataFrame(data=result_data_one_team, columns=['name', 'is_home', 'total_points', 'q_1', 'q_2', 'q_3', 'q_4', 'is_win'])

    # Buscar id del registro asociado al equipo "name_team".
    query = f'''SELECT id_statistics
                FROM statistics
                JOIN teams_has_leagues ON statistics.id_leagues_id_league = teams_has_leagues.leagues_id_league
                JOIN teams ON teams_has_leagues.teams_id_team = teams.id_team
                WHERE teams_has_leagues.leagues_id_league = {id_league}
                  AND name_team = '{name_team}';'''
    id_statistics_exist = fs_select_row(query)[0][0]
    del query

    # Buscar ID del equipo "name_team"
    query = f'''SELECT id_team FROM teams
                WHERE name_team = "{name_team}"'''
    current_id_team = fs_select_row(query)[0][0]
    del query

    # Iterar en 2 ocasiones:
    # 0 para is_home = 0
    # 0 para is_home = 1
    for i_ishome in range(2):
        # Iterar 4 veces "list_quarters = ['q_1', 'q_2', 'q_3', 'q_4']"
        for i_q in list_quarters:
            # Enviar datos para calcular las estadísticas por cuartos, condicionados a si es local o visitante.
            list_statistics_team.append(calc_statistics_quarters(df_data_one_team, name_team, i_q, i_ishome))

        # Enviar datos para calcular las estadísticas generales, condicionados a si es local o visitantes.
        list_statistics_team.append(calc_statistics_total_is_home(df_data_one_team, name_team, i_ishome))

    # Enviar datos para calcular las estadísticas generales.
    list_statistics_team.append(calc_statistics_totals(df_data_one_team, name_team))

    print(list_statistics_team)
    # Enviar calculos estadísticos almacenados en "list_statistics_team"
    # (-14) para evitar exception al iterar sobre la última posición de "list_statistics_teams"
    for i_sent in range(-14, len(list_statistics_team)-14, 14):
        print(f'Sending data to "analysis_basketball.statistics for id_team: {list_statistics_teams[i_sent + 15]}')

        # list_statistics_teams[i_sent+23][3], list_statistics_teams[i_sent+15][0],
        conn_insert_statistics(list_statistics_teams[i_sent + 14], list_statistics_teams[i_sent + 15],
                               list_statistics_teams[i_sent + 16], list_statistics_teams[i_sent + 27][0],
                               list_statistics_teams[i_sent+27][1], list_statistics_teams[i_sent+27][2],
                               list_statistics_teams[i_sent+27][3], list_statistics_teams[i_sent+26][0],
                               list_statistics_teams[i_sent+26][1], list_statistics_teams[i_sent+26][2],
                               list_statistics_teams[i_sent+26][3], list_statistics_teams[i_sent+21][0],
                               list_statistics_teams[i_sent+21][1], list_statistics_teams[i_sent+21][2],
                               list_statistics_teams[i_sent+21][3], list_statistics_teams[i_sent+22][0],
                               list_statistics_teams[i_sent+22][1], list_statistics_teams[i_sent+22][2],
                               list_statistics_teams[i_sent+22][3], list_statistics_teams[i_sent+23][0],
                               list_statistics_teams[i_sent+23][1], list_statistics_teams[i_sent+23][2],
                               list_statistics_teams[i_sent+23][3], list_statistics_teams[i_sent+24][0],
                               list_statistics_teams[i_sent+24][1], list_statistics_teams[i_sent+24][2],
                               list_statistics_teams[i_sent+24][3], list_statistics_teams[i_sent+25][0],
                               list_statistics_teams[i_sent+25][1], list_statistics_teams[i_sent+25][2],
                               list_statistics_teams[i_sent+25][3], list_statistics_teams[i_sent+17][0],
                               list_statistics_teams[i_sent+17][1], list_statistics_teams[i_sent+17][2],
                               list_statistics_teams[i_sent+17][3], list_statistics_teams[i_sent+18][0],
                               list_statistics_teams[i_sent+18][1], list_statistics_teams[i_sent+18][2],
                               list_statistics_teams[i_sent+18][3], list_statistics_teams[i_sent+19][0],
                               list_statistics_teams[i_sent+19][1], list_statistics_teams[i_sent+19][2],
                               list_statistics_teams[i_sent+19][3], list_statistics_teams[i_sent+20][0],
                               list_statistics_teams[i_sent+20][1], list_statistics_teams[i_sent+20][2],
                               list_statistics_teams[i_sent+20][3])
        # list_statistics_teams[0] = id_statistics, # list_statistics_teams[1] = teams_has_leagues_teams_id_team,
        # list_statistics_teams[2] = teams_has_leagues_leagues_id_league, list_statistics_teams[12] = Gral,
        # list_statistics_teams[12] = Gral Home, list_statistics_teams[7] = Gral Away,
        # list_statistics_teams[8:12][:] = q_i Home, list_statistics_teams[3:7][:] = q_i Away
        # Ejemplo:
        # [0]  id_statistics = 1256
        # [1]  id_teams_id_team = 9841
        # [2]  id_leagues_id_league = 2484
        # [3]  Q_1 AWAY =  (16.84211, 16.0, 27, 4)
        # [4]  Q_2 AWAY =  (15.36842, 16.0, 24, 8)
        # [5]  Q_3 AWAY =  (17.36842, 17.0, 26, 8)
        # [6]  Q_4 AWAY =  (19.10526, 20.0, 26, 8)
        # [7]  AWAY_GRAL = (79.70566, 80.0, 122, 47)
        # [8]  Q_1 home =  (19.05263, 20.0, 31, 7)
        # [9]  Q_2 home =  (17.10526, 16.0, 29, 7)
        # [10]  Q_3 home =  (20.73684, 21.0, 28, 12)
        # [11]  Q_4 home =  (20.47368, 21.0, 27, 13)
        # [12]  HOME_GRAL = (77.36842, 76.0, 104, 62)
        # [13]  GENERAL = (73.02632, 72.0, 104, 47)

    list_statistics_teams.clear()
# END --------- CALCULATE STATISTICS                                                                               # # #
# # ================================================================================================================== #


# ==================================================================================================================== #
# GET DATA TABLE TEAMS                                                                                                 #
# ==================================================================================================================== #
def prepare_data_for_statistics_all_teams(id_league):

    # Query con el formato SQL para obtener los registros ordenados ASC por nombre
    query = f'''SELECT teams.name_team, matches.is_home, matches.total_points, matches.q_1, matches.q_2, matches.q_3, matches.q_4, matches.is_win
                FROM matches
                JOIN teams_has_matches ON matches.id_match = teams_has_matches.matches_id_match
                JOIN teams ON teams_has_matches.teams_id_team = teams.id_team 
                JOIN teams_has_leagues ON teams.id_team = teams_has_leagues.teams_id_team
                WHERE teams_has_leagues.leagues_id_league = {id_league}
                ORDER BY teams.name_team;'''

    # Lista que contiene tuplas.
    # Cada tupla tiene los datos, solicitados por medio del query anterior, de cada partido.
    # Ejemplo: [('Argentino', 0, 72, 12, 19, 18, 23, 0), ('Argentino', 0, 60, 12, 11, 14, 23, 0),..., ()]
    result_data = fs_select_row(query)

    del query

    # Enviar la lista con los datos obtenidos.
    calculate_statistics_all_teams_in_unique_league(result_data, id_league)
# END --------- ET DATA TABLE TEAMS                                                                                # # #
# # ================================================================================================================== #


# ==================================================================================================================== #
# GET DATA TABLE TEAMS                                                                                                 #
# ==================================================================================================================== #
def prepare_data_for_statistics_one_team(id_league, name_team):

    # Query con el formato SQL para obtener los registros ordenados ASC por nombre
    query = f'''SELECT teams.name_team, matches.is_home, matches.total_points, matches.q_1, matches.q_2, matches.q_3, matches.q_4, matches.is_win
                FROM matches
                JOIN teams_has_matches ON matches.id_match = teams_has_matches.matches_id_match
                JOIN teams ON teams_has_matches.teams_id_team = teams.id_team 
                JOIN teams_has_leagues ON teams.id_team = teams_has_leagues.teams_id_team
                WHERE teams_has_leagues.leagues_id_league = {id_league}
                  AND teams.name_team = '{name_team}'
                ORDER BY teams.name_team;'''

    # Lista que contiene tuplas.
    # Cada tupla tiene los datos, solicitados por medio del query anterior, de cada partido del equipo seleccionado.
    # Ejemplo: [('Argentino', 0, 72, 12, 19, 18, 23, 0), ('Argentino', 0, 60, 12, 11, 14, 23, 0),..., ()]
    result_data_one_team = fs_select_row(query)

    del query

    # Enviar la lista con los datos obtenidos.
    calculate_statistics_one_team_in_unique_league(result_data_one_team, id_league, name_team)
# END --------- ET DATA TABLE TEAMS                                                                                # # #
# # ================================================================================================================== #


def show_statistics(id_leagues_get, tuple_names_teams):
    try:
        # Ejemplo: tupla_names_teams = ('Union De Santa Fe', 'Ferro', 'Quimsa')
        query = f'''SELECT *
                    FROM statistics
                    JOIN teams_has_leagues ON statistics.id_teams_id_team = teams_has_leagues.teams_id_team  
                    JOIN teams ON teams_has_leagues.teams_id_team = teams.id_team
                    WHERE teams.name_team IN {tuple_names_teams}
                      AND statistics.id_leagues_id_league = {id_leagues_get} '''

        result_data_statistics = fs_select_row(query)
        # print(df_get_statistics.iloc[[0, 1], [3, 4, 5, 6, 7]])

        list_columns = ['id_statistics', 'id_teams_id_team', 'id_leagues_id_league', 'avg_gral', 'mdn_gral', 'max_gral',
                        'min_gral', 'avg_h', 'mdn_h', 'max_h', 'min_h', 'avg_a', 'mdn_a', 'max_a', 'min_a', 'avg_q1_h',
                        'mdn_q1_h', 'max_q1_h', 'min_q1_h', 'avg_q2_h', 'mdn_q2_h', 'max_q2_h', 'min_q2_h', 'avg_q3_h',
                        'mdn_q3_h', 'max_q3_h', 'min_q3_h', 'avg_q4_h', 'mdn_q4_h', 'max_q4_h', 'min_q4_h', 'avg_q1_a',
                        'mdn_q1_a', 'max_q1_a', 'min_q1_a', 'avg_q2_a', 'mdn_q2_a', 'max_q2_a', 'min_q2_a', 'avg_q3_a',
                        'mdn_q3_a', 'max_q3_a', 'min_q3_a', 'avg_q4_a', 'mdn_q4_a', 'max_q4_a', 'min_q4_a',
                        'id_teams_id_team', 'id_leagues_id_league', 'id_NN', 'name_team']

        df_get_statistics = pd.DataFrame(data=result_data_statistics, columns=list_columns)

        while True:
            msn_to_show = '\nSeleccione las columnas a mostrar:'

            msn = show_options(list_with_options=list_columns, msn_to_show=msn_to_show, range_options=1)

            select_options_df = int(input('\nSeleccione:\n\t1: Seleccionar nuevas columnas personalizadas para los equipos {home} y {away}.'
                                          '\n\t2: Obtener las estadísticas base del análisis.\n\t3: \n\t0: Salir\n\n\t-> '))

            if select_options_df == 1:
                list_columns_selected = []
                while True:
                    select_column = int(input(msn + '\n\n\t-> '))

                    if 0 < select_column <= len(list_columns):

                        column_choose = list_columns[select_column-1]

                        if column_choose not in list_columns_selected:
                            # Agregar el ID de la liga o nombre del equipo.
                            list_columns_selected.append(column_choose)
                            # Dividir el string cada salto de línea y crear una lista.
                            lineas = msn.splitlines()

                            # Agregar información de opción seleccionada.
                            lineas[select_column + 1] = f'\tTHIS OPTION WAS SELECTED AS HOME ------------ {lineas[select_column + 1].replace(": ", "")[2:]}'

                            # Unir las líneas modificadas en un nuevo string.
                            msn = '\n'.join(lineas)

                    # 0: SALIR.
                    elif select_column == 0:
                        break

                # Selección fuera del rango
                else:
                    print('\tIngrese un número que esté dentro de la lista.\n')

                try:
                    # print('\n')
                    print(df_get_statistics.loc[:, list_columns_selected])

                except Exception as e:
                    print(f'No se generó la lista de columnas para mostrar en el DataFrame.\n{e}')

            elif select_options_df == 2:
                # Ejemplo: tuple_names_teams = ['Union De Santa Fe', 'San Lorenzo']
                # "tuple_names_teams" es uno de los argumentos que recibe la función "show_statistics"
                data_home = df_get_statistics[df_get_statistics['name_team'] == tuple_names_teams[0]]
                data_away = df_get_statistics[df_get_statistics['name_team'] == tuple_names_teams[1]]
                print(data_home[['name_team', 'avg_h', 'mdn_h', 'max_h', 'min_h']])
                print('\n')
                print(data_away[['name_team', 'avg_a', 'mdn_a', 'max_a', 'min_a']])

            # 0: SALIR
            elif select_options_df == 0:
                break

    except Exception as e:
        print(f'EXCEPTION IN calculate_statistics.py.show_statistics\n{e}')


