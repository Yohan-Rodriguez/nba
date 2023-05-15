# This is a sample Python script.
# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from conn.connections import insert_row
from history_links.search_links_leagues import search_link
from history_match.load_history import cath_data as load_data
from history_match.update_history import cath_data as update_data
from conn.functions_shared import select_row as fs_select_row
from statistics_dir.calculate_statistics import get_data
from check_db_and_controllers.show_list_options import show_options


# ==================================================================================================================== #
# LOAD NEW DATA TO HISTORY.                                                                                            #
# ==================================================================================================================== #
def new_league_history():
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
                          # 'https://www.flashscore.co/baloncesto/usa/nba/resultados/'
    ]

    load_data(list_links_leagues)
# END --------- LOAD NEW DATA TO HISTORY.                                                                          # # #
# ==================================================================================================================== #


# ==================================================================================================================== #
# UPDATE HISTORY.                                                                                                      #
# ==================================================================================================================== #
def update_history():
    update_data()
# END --------- UPDATE HISTORY.                                                                                    # # #
# ==================================================================================================================== #


# ==================================================================================================================== #
# STATISTICS                                                                                                           #
# ==================================================================================================================== #
def get_statistics():
    query = '''SELECT name_league, id_league 
               FROM leagues
               ORDER BY name_league ASC'''
    # list_leagues :: lista de tuplas,
    # cada tupla con dos posiciones (name_league, id_league)
    list_leagues = fs_select_row(query)
    del query

    # Usar la función show_options(
    msn_to_show = '\nSeleccione la liga del (los) equipo()s0 a análizar:'
    msn_to_show_leagues = show_options(list_with_options=list_leagues, msn_to_show=msn_to_show)


    # try:
    #     # Mostrar el primer mensaje
    #     select_league = int(input(msn_to_show_leagues + '\n\n\t-> '))
    #
    #     if 0 < select_league <= len(list_leagues):
    #         # Obtener el ID de la liga seleccionada por medio de la
    #         # posición de la lista que contiene el ID de la liga dada.
    #         # link_league_choose = _ _ _ _ :: int (ID)
    #         link_league_choose = list_leagues[select_league - 1][1]
    #
    #         # Solicitar la información a la tabla "analysis_basketball.teams" con el ID de la(s)
    #         # liga(s) referencidas en la siguiente lista.
    #         list_id_leagues = [link_league_choose]
    #
    #         # Ya tengo el id de la liga, ahora tengo que obtener los nombres de los equipos de esa liga
    #         #
    #         #
    #         #
    #         #
    #         #
    #         #
    #         #
    #         # ...
    #
    #
    #
    #     # 0: SALIR
    #     elif select_league == 0:
    #         pass
    #
    #     # Selección fuera del rango
    #     else:
    #         print('\tIngrese un número que esté dentro de la lista.\n')
    #
    # # Usuario no digita un número.
    # except Exception:
    #     print('\tEl character ingresado no es un número.\n')

    # # Solicitud de información a la tabla "analysis_basketball".teams con el id de liga dado
    # list_id_leagues = [9862]
    #

    # # open_browser.catch_match()
    # get_data(list_id_leagues)


# END --------- STATISTICS                                                                                         # # #
# ==================================================================================================================== #


def see_forecast():
    pass


# ==================================================================================================================== #
# FUNCTIONS CALLS                                                                                                      #
# ==================================================================================================================== #
# # Cargar nueva data al historial de equipos y sus estadísticas en cada liga,
# # para guardar en la base de datos.
# new_league_history()

# Actualizar historial de equipos y sus estadísticas en cada liga,
# para guardar en la base de datos.
update_history()

# # Obtener estadísticas de los equipos
# get_statistics()

# # Ver pronósticos de un o dos equipo.
# see_forecast()
# END --------- FUNCTIONS CALLS                                                                                    # # #
# ==================================================================================================================== #

