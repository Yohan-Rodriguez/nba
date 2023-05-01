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

    return my_result[0][0]
# END --------- READ                                                                                               # # #
# ==================================================================================================================== #


# ==================================================================================================================== #
# INSERT                                                                                                               #
# ==================================================================================================================== #
def insert_row (database, query):
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

    insert_row(database=database_default, query=query)
    print('Executed TABLE "teams".')
# END --------- TABLE "analysis_basketball.teams"                                                                  # # #
# ==================================================================================================================== #


# ==================================================================================================================== #
# TABLE "analysis_basketball.leagues"                                                                                  #
# ==================================================================================================================== #
def conn_db_table_leagues(id_league, name_league):
    query = f'''INSERT INTO leagues (id_league, name) VALUES ({id_league}, '{name_league}')'''
    insert_row(database=database_default, query=query)
    print('Executed TABLE "leagues".')
# END --------- TABLE "analysis_basketball.leagues"                                                                 # # #
# ==================================================================================================================== #


# ==================================================================================================================== #
# TABLE "analysis_basketball.errors"                                                                                   #
# ==================================================================================================================== #
def connection_db_t_errors(id_error, date_match, div_name_home, div_name_away):
    query = f'''INSERT INTO t_errors (id_error, date, home, away) VALUES ({id_error}, '{date_match}', '{div_name_home}',
            '{div_name_away}')'''
    insert_row(database=database_default, query=query)
    print('Executed TABLE "t_errors" X+X+X+X+X+X+XX+X -----------')
# ==================================================================================================================== #
# END --------- TABLE "analysis_basketball.errors"                                                                 # # #
# ==================================================================================================================== #
