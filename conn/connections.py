from conn.conn_to_database import database_default
from conn.conn_functions_shared import insert_row


# ==================================================================================================================== #
# TABLE "analysis_basketball.leagues"                                                                                  #
# ==================================================================================================================== #
def conn_db_table_leagues(id_league, name_league,new_tab_open):
    query = f'''INSERT INTO leagues (id_league, name_league, link_league) 
                VALUES ({id_league}, '{name_league}', '{new_tab_open}')'''
    insert_row(query=query)

    print('Executed TABLE "leagues".')
# END --------- TABLE "analysis_basketball.leagues"                                                                 # # #
# ==================================================================================================================== #


# ==================================================================================================================== #
# TABLE "analysis_basketball.teams"                                                                                    #
# ==================================================================================================================== #
def conn_db_table_teams(id_team, name_team):
    query = f'''INSERT INTO teams (id_team, name_team) VALUES ({id_team}, '{name_team}')'''
    insert_row(query=query)

    print('Executed TABLE "teams".')
# END --------- TABLE "analysis_basketball.teams"                                                                  # # #
# ==================================================================================================================== #


# ==================================================================================================================== #
# TABLE "analysis_basketball.teams"                                                                                    #
# ==================================================================================================================== #
def conn_db_table_teams_has_leagues(teams_id_team, leagues_id_league):
    query = f'''INSERT INTO teams_has_leagues (teams_id_team, leagues_id_league) VALUES ({teams_id_team}, 
    '{leagues_id_league}')'''
    insert_row(query=query)

    print('Executed TABLE "teams_has_leagues".')
# END --------- TABLE "analysis_basketball.teams"                                                                  # # #
# ==================================================================================================================== #


# ==================================================================================================================== #
# TABLE "analysis_basketball.teams"                                                                                    #
# ==================================================================================================================== #
def conn_db_table_matches(id_match, date_match, is_home, total_points, q_1, q_2, q_3, q_4, over_time, is_win, points_diff_q3,
                          points_diff_final):

    query = f'''INSERT INTO matches (id_match, date_match, is_home, total_points, q_1, q_2, q_3, q_4, over_time, is_win,
                points_diff_q3, points_diff_final) VALUES ({id_match}, '{date_match}', {is_home}, {total_points}, {q_1},
                {q_2}, {q_3}, {q_4}, {over_time}, {is_win}, {points_diff_q3}, {points_diff_final})'''
    insert_row(query=query)

    print('Executed TABLE "matches".')
# END --------- TABLE "analysis_basketball.teams"                                                                  # # #
# ==================================================================================================================== #


# ==================================================================================================================== #
# TABLE "analysis_basketball.teams"                                                                                    #
# ==================================================================================================================== #
def conn_db_table_teams_has_matches(teams_id_team, matches_id_match):
    query = f'''INSERT INTO teams_has_matches (teams_id_team, matches_id_match) VALUES ({teams_id_team}, 
                '{matches_id_match}')'''
    insert_row(query=query)

    print('Executed TABLE "teams_has_matches".')
# END --------- TABLE "analysis_basketball.teams"                                                                  # # #
# ==================================================================================================================== #


# ==================================================================================================================== #
# TABLE "analysis_basketball.teams"                                                                                    #
# ==================================================================================================================== #
def conn_db_table_match_statistics(matches_id_match, avg_match, avg_q1, avg_q2,
                                   avg_q3, avg_q4):
    query = f'''INSERT INTO match_statistics (matches_id_match, avg_match, avg_q1_match, avg_q2_match, 
                avg_q3_match, avg_q4_match) VALUES ({matches_id_match}, {avg_match}, {avg_q1}, {avg_q2}, 
                {avg_q3}, {avg_q4})'''
    insert_row(query=query)

    print('Executed TABLE "match_statistics".')
# END --------- TABLE "analysis_basketball.teams"                                                                  # # #
# ==================================================================================================================== #


# ==================================================================================================================== #
# SEN DATA TABLE STATISTICS                                                                                            #
# ==================================================================================================================== #
def conn_insert_table_gral_statistics(id_statistics, teams_id_team, leagues_id_league, avg_gral, mdn_gral, max_gral,
                                      min_gral, avg_h, mdn_h, max_h, min_h, avg_a, mdn_a, max_a, min_a, avg_q1_h,
                                      mdn_q1_h, max_q1_h, min_q1_h, avg_q2_h, mdn_q2_h, max_q2_h, min_q2_h, avg_q3_h,
                                      mdn_q3_h, max_q3_h, min_q3_h, avg_q4_h, mdn_q4_h, max_q4_h, min_q4_h, avg_q1_a,
                                      mdn_q1_a, max_q1_a, min_q1_a, avg_q2_a, mdn_q2_a, max_q2_a, min_q2_a, avg_q3_a,
                                      mdn_q3_a, max_q3_a, min_q3_a, avg_q4_a, mdn_q4_a, max_q4_a, min_q4_a):

    query = f'''INSERT INTO gral_statistics (id_statistics, teams_id_team, leagues_id_league, avg_gral, mdn_gral, max_gral, 
    min_gral, avg_h, mdn_h, max_h, min_h, avg_a, mdn_a, max_a, min_a, avg_q1_h, mdn_q1_h, max_q1_h, min_q1_h, avg_q2_h, 
    mdn_q2_h, max_q2_h, min_q2_h, avg_q3_h, mdn_q3_h, max_q3_h, min_q3_h, avg_q4_h, mdn_q4_h, max_q4_h, min_q4_h, avg_q1_a, 
    mdn_q1_a, max_q1_a, min_q1_a, avg_q2_a, mdn_q2_a, max_q2_a, min_q2_a, avg_q3_a, mdn_q3_a, max_q3_a, min_q3_a, avg_q4_a, 
    mdn_q4_a, max_q4_a, min_q4_a) VALUES ({id_statistics}, {teams_id_team}, {leagues_id_league}, {avg_gral}, 
    {mdn_gral}, {max_gral}, {min_gral}, {avg_h}, {mdn_h}, {max_h}, {min_h}, {avg_a}, {mdn_a}, {max_a}, {min_a}, {avg_q1_h}, 
    {mdn_q1_h}, {max_q1_h}, {min_q1_h}, {avg_q2_h}, {mdn_q2_h}, {max_q2_h}, {min_q2_h}, {avg_q3_h}, {mdn_q3_h}, {max_q3_h}, 
    {min_q3_h}, {avg_q4_h}, {mdn_q4_h}, {max_q4_h}, {min_q4_h}, {avg_q1_a}, {mdn_q1_a}, {max_q1_a}, {min_q1_a},  {avg_q2_a}, 
    {mdn_q2_a}, {max_q2_a}, {min_q2_a}, {avg_q3_a}, {mdn_q3_a}, {max_q3_a}, {min_q3_a}, {avg_q4_a}, 
    {mdn_q4_a}, {max_q4_a}, {min_q4_a})'''

    insert_row(query, database=database_default)

    print('Executed INSERT INTO TABLE "statistics" successfully!.')
# END --------- SEN DATA TABLE STATISTICS                                                                          # # #
# # ================================================================================================================== #


# ==================================================================================================================== #
# TABLE "analysis_basketball.errors"                                                                                   #
# ==================================================================================================================== #
def connection_db_t_errors(name_league):
    query = f'''INSERT INTO t_errors (league_error) VALUES ('{name_league}')'''
    insert_row(query=query)

    print('Executed TABLE "t_errors" X+X+X+X+X+X+XX+X -----------')
# ==================================================================================================================== #
# END --------- TABLE "analysis_basketball.errors"                                                                 # # #
# ==================================================================================================================== #
