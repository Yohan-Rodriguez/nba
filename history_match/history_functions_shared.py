import time
from selenium.webdriver.common.by import By
from conn.connections import conn_db_table_matches as conn_db_matches, conn_db_table_match_statistics
from conn.connections import conn_db_table_teams_has_matches as conn_db_teams_has_matches
from conn.conn_functions_shared import select_row as fs_select_row
from check_db_and_controllers.check_data_in_db import check_id_match as ck_match
from check_db_and_controllers.check_data_in_db import check_name_team as ck_name


# ==================================================================================================================== #
# Función para enviar los datos a "t_teams" y "t_matches"                                                              #
# ==================================================================================================================== #
def send_data_to_teams_and_matches(teams_id_team, id_match, date_match, is_home, total_points, q_1, q_2, q_3, q_4,
                                   over_time, is_win, time_x_quarter, points_difference, home_or_away_2):
    # Enviar data a "t_matches"
    print(f'Sending data to "analysis_basketball.matches" for {home_or_away_2}.')
    conn_db_matches(id_match, date_match, is_home, total_points, q_1, q_2, q_3, q_4, over_time, is_win, points_difference)

    # Enviar data a "t_teams_has_matches"
    print(f'Sending data to "analysis_basketball.teams_has_matches" for {home_or_away_2}.')
    conn_db_teams_has_matches(teams_id_team, id_match)

    # Calcular las medias correspondientes a los puntos marcados divididos por el tiempo tomado.
    avg_match = (q_1 + q_2 + q_3 + q_4) / (time_x_quarter * 4)
    avg_q1 = q_1 / time_x_quarter
    avg_q2 = q_2 / time_x_quarter
    avg_q3 = q_3 / time_x_quarter
    avg_q4 = q_4 / time_x_quarter
    # Enviar data a "t_match_statistics"
    print(f'Sending data to "analysis_basketball.match_statistics" for {home_or_away_2}.')
    conn_db_table_match_statistics(id_match, avg_match, avg_q1, avg_q2, avg_q3, avg_q4)
# END --------- Función para enviar los datos a "t_teams" y "t_matches" ============================================== #


# ==================================================================================================================== #
# BUSCAR CSS_SELECTOR BUTTON                                                                                           #
# ==================================================================================================================== #
def search_button(driver, selector_css_button):
    # Salida de emergencia al siguiente bucle para evitar que sea infinito
    flag_emergency_button = 5

    while True:
        try:
            button_previous = driver.find_element(By.CSS_SELECTOR, selector_css_button)
            break

        except Exception:
            print(f'Reintentando obtener CSS_SELECTOR de "Mostrar Más partidos".\nIntentos Restante: -{flag_emergency_button} s')
            time.sleep(2)

            if flag_emergency_button <= 0:
                button_previous = ''
                break

            flag_emergency_button -= 1

    return button_previous
# END --------- BUSCAR CSS_SELECTOR BUTTON                                                                             #
# ==================================================================================================================== #


# ==================================================================================================================== #
# Obtener id (analysis_basketball.leagues.id_league) de la liga actual                                                 #
# ==================================================================================================================== #
def get_id_league_currently(name_league):
    query = f'''SELECT id_league FROM leagues
                WHERE name_league = "{name_league}"'''
    current_id_league = fs_select_row(query)[0][0]

    del query

    return current_id_league
# END --------- Obtener id (analysis_basketball.leagues.id_league) de la liga actual                               # # #
# ==================================================================================================================== #


# ==================================================================================================================== #
# SENDING DATA TO BD                                                                                                   #
# ==================================================================================================================== #
def send_data_to_db(list_names_teams, current_id_league, date_match, points_final_home, q_1H, q_2H, q_3H, q_4H,
                    is_over_time, is_win_home, points_final_away, q_1A, q_2A, q_3A, q_4A, time_quarter):

    points_difference = (q_1H + q_2H + q_3H) - (q_1A + q_2A + q_3A)

    # 2 repeticiones:
    # i_send_data_t_team == 0 para home y
    # i_send_data_t_team == 1 para away.
    for i_send_data_t_team in range(2):
        # Generar id_match
        id_match = ck_match()

        # Verificar que el nombre de los equipos están o no, relacionados en "t_team"
        # Sí el equipo no existe en t_teams, se guarda dentro del scope de la función
        # "ck.check_name_team"
        teams_id_team = ck_name(list_names_teams[i_send_data_t_team], current_id_league, home_or_away=i_send_data_t_team)

        if i_send_data_t_team == 0:
            # Enviar data de home a "t_matches"
            send_data_to_teams_and_matches(teams_id_team, id_match, date_match, True, points_final_home, q_1H, q_2H,
                                           q_3H, q_4H, is_over_time, is_win_home, time_quarter, points_difference,
                                           i_send_data_t_team)

        elif i_send_data_t_team == 1:
            # Enviar data de away a "t_team" y a "t_matches"
            send_data_to_teams_and_matches(teams_id_team, id_match, date_match, False, points_final_away, q_1A, q_2A,
                                           q_3A, q_4A, is_over_time, not is_win_home, time_quarter, points_difference*(-1),
                                           i_send_data_t_team)

    print('Completed Finish match -----------------------------')
# END --------- SENDING DATA TO BD                                                                                 # # #
# ==================================================================================================================== #
