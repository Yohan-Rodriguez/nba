import connections


# ==================================================================================================================== #
# SEND DATA TO TABLE "analysis_basketball"                                                                             #
# ==================================================================================================================== #
def send_data():
    connections.conn_insert_table_statistics(id_team, avg_gral, mdn_gral, max_gral, min_gral, avg_home, mdn_home,
                                             max_point_h, min_point_h, avg_q1_h, mdn_q1_h, max_point_q1_h, min_point_q1_h,
                                             avg_q2_h, mdn_q2_h, max_point_q2_h, min_point_q2_h, avg_q3_h, mdn_q3_h,
                                             max_point_q3_h, min_point_q3_h, avg_q4_h, mdn_q4_h, max_point_q4_h,
                                             min_point_q4_h, avg_away, mdn_away, max_away, min_away, avg_q1_a, mdn_q1_a,
                                             max_point_q1_a, min_point_q1_a, avg_q2_a, mdn_q2_a, max_point_q2_a,
                                             min_point_q2_a, avg_q3_a, mdn_q3_a, max_point_q3_a, min_point_q3_a, avg_q4_a,
                                             mdn_q4_a, max_point_q4_a, min_point_q4_a)
# END --------- SEND DATA TO TABLE "analysis_basketball"                                                           # # #
# # ================================================================================================================== #


# ==================================================================================================================== #
# CALCULATE STATISTICS                                                                                                 #
# ==================================================================================================================== #
def calc_statistics(result_data):
    
    index_result_data = 0
    while True:
        #Nombre del equipo
        name_team = result_data[index_result_data][2]

        try:
            # Capturar la data de un solo equipo.
            # Mientras las tuplas tengan el mismo nombre de equipo,
            # se ejecuta el siguiente bucle:
            while result_data[index_result_data][2] == name_team:

                print(result_data[index_result_data][2])

                # El código sigue con el proximo equipo de la lista.
                index_result_data += 1

        except Exception as e:
            # Se Termina de recorrer la lista "result_data".
            break



    id_team
    avg_gral
    mdn_gral
    max_gral
    min_gral
    avg_home
    mdn_home
    max_point_h
    min_point_h
    avg_q1_h
    mdn_q1_h
    max_point_q1_h
    min_point_q1_h
    avg_q2_h
    mdn_q2_h
    max_point_q2_h
    min_point_q2_h
    avg_q3_h
    mdn_q3_h
    max_point_q3_h
    min_point_q3_h
    avg_q4_h
    mdn_q4_h
    max_point_q4_h
    min_point_q4_h
    avg_away
    mdn_away
    max_away
    min_away
    avg_q1_a
    mdn_q1_a
    max_point_q1_a
    min_point_q1_a
    avg_q2_a
    mdn_q2_a
    max_point_q2_a
    min_point_q2_a
    avg_q3_a
    mdn_q3_a
    max_point_q3_a
    min_point_q3_a
    avg_q4_a
    mdn_q4_a
    max_point_q4_a
    min_point_q4_a

# END --------- CALCULATE STATISTICS                                                                               # # #
# # ================================================================================================================== #

# ==================================================================================================================== #
# GET DATA TABLE TEAMS                                                                                                 #
# ==================================================================================================================== #
def get_data():
    # Solicitud de información a la tabla analysis_basketball.teams con el id de liga dado
    leagues_id_league = 819

    # Query con el formato SQL para obtener los registros ordenados ASC por nombre
    query = f'''SELECT * FROM teams
                WHERE leagues_id_league = {leagues_id_league}
                ORDER BY name'''

    # Resultado de la consulta. Lista con cada registro en formato de tupla con los datos de cada columna:
    # [(id_team, date, name, is_home, total_points, q_1, q_2, q_3, q_4, over_time, is_win, leagues_id_league),...,]
    # [(1514, datetime.date(2023, 1, 6), 'Suns', 1, 96, 23, 23, 27, 23, 0, 0, 819),...,]
    result_data = connections.select_row(query)


    # for i in result_data:
    #     print(i)

    calc_statistics(result_data)
# END --------- ET DATA TABLE TEAMS                                                                                # # #
# # ================================================================================================================== #

