# This is a sample Python script.
# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import load_history
import load_historytest
import calculate_statistics
import search_links_leagues
import tests


# ==================================================================================================================== #
# LINKS LEAGUES                                                                                                        #
# ==================================================================================================================== #
def load_links_leagues():
    search_links_leagues.search_link()
# END --------- LINKS LEAGUES                                                                                      # # #
# ==================================================================================================================== #


# ==================================================================================================================== #
# HISTORY                                                                                                              #
# ==================================================================================================================== #
def conn_main():
    # open_browser.catch_match()
    load_history.catch_match()
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
# # Guardar todos los links de las ligas
# load_links_leagues()

# Generar historial de equipos para guardar en la base de datos
conn_main()

# # Generar estadísticas de los equipos
# see_statistics()
# END --------- FUNCTIONS CALLS                                                                                    # # #
# ==================================================================================================================== #

# tests.testing()
