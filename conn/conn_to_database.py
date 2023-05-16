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