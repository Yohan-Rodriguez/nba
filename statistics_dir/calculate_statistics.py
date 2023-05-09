import pandas as pd
from conn.connections import conn_insert_table_statistics as conn_insert_statistics
from history_match.functions_shared import select_row as fs_select_row


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
    avg_gral_ishome = round(df_data_teams.loc[(df_data_teams['name'] == f'{i_name}') & df_data_teams['is_home'] == i_ishome, 'sum_total_quarters'].mean(), 5)
    # END --------- CALCULATE AVG                                                                                  # # #
    # # ============================================================================================================== #

    # ================================================================================================================ #
    # CALCULATE MEDIAN                                                                                                 #
    # ================================================================================================================ #
    # MEDIANA total del equipo específico ({i_name}),
    # y si es local o visitante (con máximo, 5 decimas).
    mdn_gral_ishome = round(df_data_teams.loc[(df_data_teams['name'] == f'{i_name}') & df_data_teams['is_home'] == i_ishome, 'sum_total_quarters'].median(), 5)
    # END --------- MEDIAN                                                                                         # # #
    # # ============================================================================================================== #

    # ================================================================================================================ #
    # CALCULATE MAX                                                                                                    #
    # ================================================================================================================ #
    # MÁXIMO total del equipo específico ({i_name}),
    # y si es local o visitante (con máximo, 5 decimas).
    max_gral_ishome = round(df_data_teams.loc[(df_data_teams['name'] == f'{i_name}') & df_data_teams['is_home'] == i_ishome, 'sum_total_quarters'].max(), 5)
    # END --------- MAX                                                                                            # # #
    # # ============================================================================================================== #

    # ================================================================================================================ #
    # CALCULATE MIN                                                                                                    #
    # ================================================================================================================ #
    # MÍNIMO total del equipo específico ({i_name}),
    # y si es local o visitante (con máximo, 5 decimas).
    min_gral_ishome = round(df_data_teams.loc[(df_data_teams['name'] == f'{i_name}') & df_data_teams['is_home'] == i_ishome, 'sum_total_quarters'].min(), 5)
    # END --------- MIN                                                                                            # # #
    # # ============================================================================================================== #
    
    return avg_gral_ishome, mdn_gral_ishome, max_gral_ishome, min_gral_ishome
    

def calc_statistics_totals(df_data_teams, i_name):
    # ================================================================================================================ #
    # CALCULATE AVG                                                                                                    #
    # ================================================================================================================ #
    # AVG total del equipo específico ({i_name}), con máximo, 5 decimas.
    avg_gral = round(df_data_teams.loc[(df_data_teams['name'] == f'{i_name}'), 'sum_total_quarters'].mean(), 5)        
    # END --------- CALCULATE AVG                                                                                  # # #
    # # ============================================================================================================== #

    # ================================================================================================================ #
    # CALCULATE MEDIAN                                                                                                 #
    # ================================================================================================================ #
    # MEDIANA total del equipo específico ({i_name}), con máximo, 5 decimas.
    mdn_gral = round(df_data_teams.loc[(df_data_teams['name'] == f'{i_name}'), 'sum_total_quarters'].median(), 5)
    # END --------- MEDIAN                                                                                         # # #
    # # ============================================================================================================== #

    # ================================================================================================================ #
    # CALCULATE MAX                                                                                                    #
    # ================================================================================================================ #
    # MÁXIMO total del equipo específico ({i_name}), con máximo, 5 decimas.
    max_gral = round(df_data_teams.loc[(df_data_teams['name'] == f'{i_name}'), 'sum_total_quarters'].max(), 5)
    # END --------- MAX                                                                                            # # #
    # # ============================================================================================================== #

    # ================================================================================================================ #
    # CALCULATE MIN                                                                                                    #
    # ================================================================================================================ #
    # MÍNIMO total del equipo específico ({i_name}), con máximo, 5 decimas.
    min_gral = round(df_data_teams.loc[(df_data_teams['name'] == f'{i_name}'), 'sum_total_quarters'].min(), 5)
    # END --------- MIN                                                                                            # # #
    # # ============================================================================================================== #
    
    return avg_gral, mdn_gral, max_gral, min_gral

# ==================================================================================================================== #
# CALCULATE STATISTICS                                                                                                 #
# ==================================================================================================================== #
list_quarters = ['q_1', 'q_2', 'q_3', 'q_4']


def calc_statistics(result_data):

    list_statistics_teams = []

    df_data_teams = pd.DataFrame(data=result_data, columns=['name', 'is_home', 'total_points', 'q_1', 'q_2', 'q_3', 'q_4', 'is_win'])

    # Crea una lista con los nombres de los equipos
    names_teams = df_data_teams['name'].unique()

    # Crear nueva columna en "df_data_teams" que contiene la suma definida a continuación
    df_data_teams['sum_total_quarters'] = df_data_teams['q_1'] + df_data_teams['q_2'] + df_data_teams['q_3'] + df_data_teams['q_4']

    for i_name in names_teams:
        list_statistics_teams.append(i_name)
        for i_ishome in range(2):
            for i_q in list_quarters:
                list_statistics_teams.append(calc_statistics_quarters(df_data_teams, i_name, i_q, i_ishome))

            list_statistics_teams.append(calc_statistics_total_is_home(df_data_teams, i_name, i_ishome))

        list_statistics_teams.append(calc_statistics_totals(df_data_teams, i_name))

    for i_sent in range(-12, len(list_statistics_teams)-12, 12):

        conn_insert_statistics(list_statistics_teams[i_sent + 12], list_statistics_teams[i_sent + 23][0],
                                                 list_statistics_teams[i_sent+23][1], list_statistics_teams[i_sent+23][2],
                                                 list_statistics_teams[i_sent+23][3], list_statistics_teams[i_sent+22][0],
                                                 list_statistics_teams[i_sent+22][1], list_statistics_teams[i_sent+22][2],
                                                 list_statistics_teams[i_sent+22][3], list_statistics_teams[i_sent+17][0],
                                                 list_statistics_teams[i_sent+17][1], list_statistics_teams[i_sent+17][2],
                                                 list_statistics_teams[i_sent+17][3], list_statistics_teams[i_sent+18][0],
                                                 list_statistics_teams[i_sent+18][1], list_statistics_teams[i_sent+18][2],
                                                 list_statistics_teams[i_sent+18][3], list_statistics_teams[i_sent+19][0],
                                                 list_statistics_teams[i_sent+19][1], list_statistics_teams[i_sent+19][2],
                                                 list_statistics_teams[i_sent+19][3], list_statistics_teams[i_sent+20][0],
                                                 list_statistics_teams[i_sent+20][1], list_statistics_teams[i_sent+20][2],
                                                 list_statistics_teams[i_sent+20][3], list_statistics_teams[i_sent+21][0],
                                                 list_statistics_teams[i_sent+21][1], list_statistics_teams[i_sent+21][2],
                                                 list_statistics_teams[i_sent+21][3], list_statistics_teams[i_sent+13][0],
                                                 list_statistics_teams[i_sent+13][1], list_statistics_teams[i_sent+13][2],
                                                 list_statistics_teams[i_sent+13][3], list_statistics_teams[i_sent+14][0],
                                                 list_statistics_teams[i_sent+14][1], list_statistics_teams[i_sent+14][2],
                                                 list_statistics_teams[i_sent+14][3], list_statistics_teams[i_sent+15][0],
                                                 list_statistics_teams[i_sent+15][1], list_statistics_teams[i_sent+15][2],
                                                 list_statistics_teams[i_sent+15][3], list_statistics_teams[i_sent+16][0],
                                                 list_statistics_teams[i_sent+16][1], list_statistics_teams[i_sent+16][2],
                                                 list_statistics_teams[i_sent+16][3])

    list_statistics_teams.clear()
# END --------- CALCULATE STATISTICS                                                                               # # #
# # ================================================================================================================== #


# ==================================================================================================================== #
# GET DATA TABLE TEAMS                                                                                                 #
# ==================================================================================================================== #
def get_data(list_id_leagues):

    for i_id_leagues in list_id_leagues:
        # Query con el formato SQL para obtener los registros ordenados ASC por nombre
        query = f'''SELECT name, is_home, total_points, q_1, q_2, q_3, q_4, is_win
                    FROM teams
                    WHERE leagues_id_league = {i_id_leagues}
                    ORDER BY name ASC'''
        result_data = fs_select_row(query)
        del query

        calc_statistics(result_data)
# END --------- ET DATA TABLE TEAMS                                                                                # # #
# # ================================================================================================================== #

