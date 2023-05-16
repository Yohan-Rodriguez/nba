from conn.connections import conn_db_table_teams_has_matches as conn_db_teams_has_matches
from check_db_and_controllers.check_data_in_db import check_id_match as ck_match
from check_db_and_controllers.check_data_in_db import check_name_team as ck_name
from conn.connections import conn_db_table_matches as conn_db_matches


def prepare_data(current_id_league, list_match_temp, date_match, i_1, i_2, i_3, i_4, i_5, i_6, i_7, i_8, i_9, i_10, i_11, i_12,
                 over_time):
    try:
        # Función para enviar los datos a "t_teams" y "t_matches" ==================================================== #
        def send_data_to_teams_and_matchs(teams_id_team, id_match, date_match, is_home,
                                          total_points, q_1, q_2, q_3, q_4, over_time, is_win,
                                          home_or_away):

            # Enviar data a "t_matches"
            print(f'Sending data to "analysis_basketball.matches" for {home_or_away}.')
            conn_db_matches(id_match, date_match, is_home, total_points, q_1,
                                              q_2, q_3, q_4, over_time, is_win)

            # Enviar data a "t_teams_has_matches"
            print(f'Sending data to "analysis_basketball.teams_has_matches" for {home_or_away}.')
            conn_db_teams_has_matches(teams_id_team, id_match)

        # END --------- Función para enviar los datos a "t_teams" y "t_matches" ====================================== #
        name_home = list_match_temp[i_12]
        name_away = list_match_temp[i_11]
        points_final_away = int(list_match_temp[i_1])
        points_final_home = int(list_match_temp[i_2])
        q_4A = int(list_match_temp[i_3])
        q_3A = int(list_match_temp[i_4])
        q_2A = int(list_match_temp[i_5])
        q_1A = int(list_match_temp[i_6])
        q_4H = int(list_match_temp[i_7])
        q_3H = int(list_match_temp[i_8])
        q_2H = int(list_match_temp[i_9])
        q_1H = int(list_match_temp[i_10])
        is_over_time = over_time

        is_win_home = False
        if points_final_home > points_final_away:
            is_win_home = True
        # ============================================================================================================ #
        # SENDING DATA TO BD                                                                                           #
        # ============================================================================================================ #
        try:
            list_names_teams = [name_home, name_away]

            # 2 repeticiones:
            # i_send_data_t_team == 0 para home y
            # i_send_data_t_team == 1 para away.
            for i_send_data_t_team in range(2):
                # Generar id_match
                id_match = ck_match()

                # Verificar que el nombre de los equipos están o no, relacionados en "t_team"
                # Sí el equipo no existe en t_teams, se guarda dentro del scope de la función
                # "ck.check_name_team"
                teams_id_team = ck_name(list_names_teams[i_send_data_t_team], current_id_league,
                                        home_or_away=i_send_data_t_team)

                if i_send_data_t_team == 0:
                    # Enviar data de home a "t_matches"
                    send_data_to_teams_and_matchs(teams_id_team, id_match, date_match, True, points_final_home, q_1H,
                                                  q_2H, q_3H, q_4H, over_time, is_win_home, home_or_away=i_send_data_t_team)

                elif i_send_data_t_team == 1:
                    # Enviar data de away a "t_team" y a "t_matches"
                    send_data_to_teams_and_matchs(teams_id_team, id_match, date_match, False, points_final_away, q_1A,
                                                  q_2A, q_3A, q_4A, over_time, not is_win_home, home_or_away=i_send_data_t_team)

            print('Completed Finish match -----------------------------')

        except Exception as e:
            print(f'X*X*X*X* EXCEPTION X*X*X*X*\n\tIn SENDING DATA TO BD\n {e}')

    except Exception as e:
        print(f'X*X*X*X* EXCEPTION X*X*X*X*\n\tIn Module .psd\n\tPREPARAR Y ENVIAR LA DATA A LA DB.\n{e}')
