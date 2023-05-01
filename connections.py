import mysql.connector


# ==================================================================================================================== #
# Atributos                                                                                                            #
# ==================================================================================================================== #
host_default = 'localhost'
user_default = 'root'
pass_default = 'admin'
database_default = 'analysis_basketball'
# END: Atributos                                                                                                   # # #
# ==================================================================================================================== #


# ==================================================================================================================== #
# CONNECTION                                                                                                           #
# ==================================================================================================================== #
def conn_to_database(database, host=host_default, user=user_default, password=pass_default):
    my_db = mysql.connector.connect(host=host,
                                    user=user,
                                    password=password,
                                    database=database)

    my_cursor = my_db.cursor()

    return my_db, my_cursor  # conn[0] y conn[1]
# END --------- CONNECTION                                                                                         # # #
# ==================================================================================================================== #


# ==================================================================================================================== #
# READ                                                                                                                 #
# ==================================================================================================================== #
def select_row(query, database=database_default):
    conn = conn_to_database(database=database)
    conn[1].execute(query)
    my_result = conn[1].fetchall()

    return my_result
# END --------- READ                                                                                               # # #
# ==================================================================================================================== #


# ==================================================================================================================== #
# INSERT                                                                                                               #
# ==================================================================================================================== #
def insert_row (query, database=database_default):
    conn = conn_to_database(database=database)
    conn[1].execute(query)
    conn[0].commit()
# END --------- INSERT                                                                                             # # #
# ==================================================================================================================== #


# ==================================================================================================================== #
# TABLE "analysis_basketball.teams"                                                                                    #
# ==================================================================================================================== #
def conn_db_table_teams(id_team, date, name_team, is_home, total_points, q_1, q_2, q_3, q_4, over_time, is_win, leagues_id_league):
    query = f'''INSERT INTO teams (id_team, date, name, is_home, total_points, q_1, q_2, q_3, q_4, over_time, 
                          is_win, leagues_id_league) VALUES ({id_team}, '{date}', '{name_team}', {is_home}, {total_points}, {q_1}, 
                          {q_2}, {q_3}, {q_4}, {over_time}, {is_win}, {leagues_id_league})'''

    insert_row(query=query)
    print('Executed TABLE "teams".')
# END --------- TABLE "analysis_basketball.teams"                                                                  # # #
# ==================================================================================================================== #


# ==================================================================================================================== #
# TABLE "analysis_basketball.leagues"                                                                                  #
# ==================================================================================================================== #
def conn_db_table_leagues(id_league, name_league):
    query = f'''INSERT INTO leagues (id_league, name) VALUES ({id_league}, '{name_league}')'''
    insert_row(query=query)
    print('Executed TABLE "leagues".')
# END --------- TABLE "analysis_basketball.leagues"                                                                 # # #
# ==================================================================================================================== #


# ==================================================================================================================== #
# TABLE "analysis_basketball.errors"                                                                                   #
# ==================================================================================================================== #
def connection_db_t_errors(id_error, date_match, div_name_home, div_name_away):
    query = f'''INSERT INTO t_errors (id_error, date, home, away) VALUES ({id_error}, '{date_match}', '{div_name_home}',
            '{div_name_away}')'''
    insert_row(query=query)
    print('Executed TABLE "t_errors" X+X+X+X+X+X+XX+X -----------')
# ==================================================================================================================== #
# END --------- TABLE "analysis_basketball.errors"                                                                 # # #
# ==================================================================================================================== #

# ==================================================================================================================== #
# SEN DATA TABLE STATISTICS                                                                                            #
# ==================================================================================================================== #
def conn_insert_table_statistics(id_team, avg_gral, mdn_gral, max_gral, min_gral, avg_home, mdn_home, max_point_h, min_point_h, avg_q1_h,
              mdn_q1_h, max_point_q1_h, min_point_q1_h, avg_q2_h, mdn_q2_h, max_point_q2_h, min_point_q2_h, avg_q3_h,
              mdn_q3_h, max_point_q3_h, min_point_q3_h, avg_q4_h, mdn_q4_h, max_point_q4_h, min_point_q4_h, avg_away,
              mdn_away, max_away, min_away, avg_q1_a, mdn_q1_a, max_point_q1_a, min_point_q1_a, avg_q2_a, mdn_q2_a,
              max_point_q2_a, min_point_q2_a, avg_q3_a, mdn_q3_a, max_point_q3_a, min_point_q3_a, avg_q4_a, mdn_q4_a,
              max_point_q4_a, min_point_q4_a):

    query = f'''INSERT INTO statistics (id_team, avg_gral, mdn_gral, max_gral, min_gral, avg_home, mdn_home, max_point_h, 
                min_point_h, avg_q1_h, mdn_q1_h, max_point_q1_h, min_point_q1_h, avg_q2_h, mdn_q2_h, max_point_q2_h, 
                min_point_q2_h, avg_q3_h, mdn_q3_h, max_point_q3_h, min_point_q3_h, avg_q4_h, mdn_q4_h, max_point_q4_h, 
                min_point_q4_h, avg_away, mdn_away, max_away, min_away, avg_q1_a, mdn_q1_a, max_point_q1_a, min_point_q1_a,
                avg_q2_a, mdn_q2_a, max_point_q2_a, min_point_q2_a, avg_q3_a, mdn_q3_a, max_point_q3_a, min_point_q3_a, 
                avg_q4_a, mdn_q4_a, max_point_q4_a, min_point_q4_a) VALLUES ({id_team}, {avg_gral}, {mdn_gral}, {max_gral}, 
                {min_gral}, {avg_home}, {mdn_home}, {max_point_h}, {min_point_h}, {avg_q1_h}, {mdn_q1_h}, {max_point_q1_h},
                {min_point_q1_h}, {avg_q2_h}, {mdn_q2_h}, {max_point_q2_h}, {min_point_q2_h}, {avg_q3_h}, {mdn_q3_h}, 
                {max_point_q3_h}, {min_point_q3_h}, {avg_q4_h}, {mdn_q4_h}, {max_point_q4_h}, {min_point_q4_h}, {avg_away}, 
                {mdn_away}, {max_away}, {min_away}, {avg_q1_a}, {mdn_q1_a}, {max_point_q1_a}, {min_point_q1_a}, {avg_q2_a}, 
                {mdn_q2_a}, {max_point_q2_a}, {min_point_q2_a}, {avg_q3_a}, {mdn_q3_a}, {max_point_q3_a}, {min_point_q3_a}, 
                {avg_q4_a}, {mdn_q4_a}, {max_point_q4_a}, {min_point_q4_a})'''

    insert_row(query)
    print('Executed INSERT INTO TABLE "statistics" successfully!.')
# END --------- SEN DATA TABLE STATISTICS                                                                          # # #
# # ================================================================================================================== #
