from conn.conn_to_database import conn_to_database as conn_db
from conn.conn_to_database import database_default


# ==================================================================================================================== #
# READ                                                                                                                 #
# ==================================================================================================================== #
def select_row(query, database=database_default):
    conn = conn_db(database=database)
    conn[1].execute(query)

    # "my_result" es una lista de tulpas.
    # Cada tupla contiene las columnas (los datos) de cada registro
    my_result = conn[1].fetchall()

    return my_result
# END --------- READ                                                                                               # # #
# ==================================================================================================================== #


# ==================================================================================================================== #
# INSERT                                                                                                               #
# ==================================================================================================================== #
def insert_row (query, database=database_default):
    conn = conn_db(database=database)
    conn[1].execute(query)

    conn[0].commit()
# END --------- INSERT                                                                                             # # #
# ==================================================================================================================== #
