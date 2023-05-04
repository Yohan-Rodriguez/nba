# This is a sample Python script.
# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import open_browser
import calculate_statistics
import tests


# ==================================================================================================================== #
# HISTORY                                                                                                              #
# ==================================================================================================================== #
def conn_main():
    # open_browser.catch_match()
    open_browser.catch_match()
# END --------- HISTORY                                                                                            # # #
# ==================================================================================================================== #


# ==================================================================================================================== #
# STATISTICS                                                                                                           #
# ==================================================================================================================== #
def see_statistics():
    # Solicitud de información a la tabla "analysis_basketball".teams con el id de liga dado
    list_id_leagues = [441, 485, 546, 705, 756, 819]

    # open_browser.catch_match()
    calculate_statistics.get_data(list_id_leagues)
# END --------- STATISTICS                                                                                         # # #
# ==================================================================================================================== #


# ==================================================================================================================== #
# FUNCTIONS CALLS                                                                                                      #
# ==================================================================================================================== #
# Generar historial de equipos para guardar en la base de datos
conn_main()

# # Generar estadísticas de los equipos
# see_statistics()
# END --------- FUNCTIONS CALLS                                                                                    # # #
# ==================================================================================================================== #

# tests.testing()
