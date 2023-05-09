# This is a sample Python script.
# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# from history_match.tests import catch_match
from history_match.load_history import catch_match
from statistics_dir.calculate_statistics import get_data
from history_links.search_links_leagues import search_link


# ==================================================================================================================== #
# LINKS LEAGUES                                                                                                        #
# ==================================================================================================================== #
def load_links_leagues():
    search_link()
# END --------- LINKS LEAGUES                                                                                      # # #
# ==================================================================================================================== #


# ==================================================================================================================== #
# HISTORY                                                                                                              #
# ==================================================================================================================== #
def conn_main():
    # open_browser.catch_match()
    catch_match()
# END --------- HISTORY                                                                                            # # #
# ==================================================================================================================== #


# ==================================================================================================================== #
# STATISTICS                                                                                                           #
# ==================================================================================================================== #
def see_statistics():
    # Solicitud de información a la tabla "analysis_basketball".teams con el id de liga dado
    list_id_leagues = [441, 485, 546, 705, 756, 819]

    # open_browser.catch_match()
    get_data(list_id_leagues)
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
