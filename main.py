# This is a sample Python script.
# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from statistics_dir.calculate_statistics import get_data
from history_links.search_links_leagues import search_link
from history_match.load_history import cath_data as load_data


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
    # catch_match()
    list_links_leagues = [
                          # 'https://www.flashscore.co/baloncesto/espana/liga-endesa/resultados/',
                          # 'https://www.flashscore.co/baloncesto/argentina/lnb/resultados/',
                          # 'https://www.flashscore.co/baloncesto/austria/superliga/resultados/',
                          # 'https://www.flashscore.co/baloncesto/dinamarca/basketligaen/resultados/',
                          # 'https://www.flashscore.co/baloncesto/eslovenia/liga-nova-kbm/resultados/',
                          # 'https://www.flashscore.co/baloncesto/finlandia/korisliiga/resultados/',
                          # 'https://www.flashscore.co/baloncesto/letonia/lbl/resultados/',
                          # 'https://www.flashscore.co/baloncesto/nueva-zelanda/nbl/resultados/',
                          # 'https://www.flashscore.co/baloncesto/polonia/energa-basket-liga/resultados/',
                          # 'https://www.flashscore.co/baloncesto/puerto-rico/bsn/resultados/',
                          # 'https://www.flashscore.co/baloncesto/republica-checa/nbl/resultados/',
                          # 'https://www.flashscore.co/baloncesto/rumania/divizia-a/resultados/'
    ]
    load_data(list_links_leagues)

# END --------- HISTORY                                                                                            # # #
# ==================================================================================================================== #


# ==================================================================================================================== #
# STATISTICS                                                                                                           #
# ==================================================================================================================== #
def see_statistics():
    # Solicitud de información a la tabla "analysis_basketball".teams con el id de liga dado
    list_id_leagues = [9862]

    # open_browser.catch_match()
    get_data(list_id_leagues)
# END --------- STATISTICS                                                                                         # # #
# ==================================================================================================================== #


# ==================================================================================================================== #
# FUNCTIONS CALLS                                                                                                      #
# ==================================================================================================================== #
# # Guardar todos los links de las ligas
# load_links_leagues()

# # Generar historial de equipos para guardar en la base de datos
# conn_main()

# Generar estadísticas de los equipos
see_statistics()
# END --------- FUNCTIONS CALLS                                                                                    # # #
# ==================================================================================================================== #

# tests.testing()

