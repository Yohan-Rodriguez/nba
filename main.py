# This is a sample Python script.
# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from history_links.search_links_leagues import search_link
from history_match.load_history import catch_data as load_data
from history_match.update_history import catch_data as update_data
from conn.conn_functions_shared import select_row as fs_select_row
from statistics_dir.calculate_statistics import prepare_data_for_statistics_one_team, show_statistics
from statistics_dir.calculate_statistics import prepare_data_for_statistics_all_teams
from statistics_dir.statistic_analysis import analysis_x_teams
from statistics_dir.statistics_functions_shared import show_options, see_options


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
                          'https://www.flashscore.co/baloncesto/republica-checa/nbl/resultados/',
                          'https://www.flashscore.co/baloncesto/rumania/divizia-a/resultados/',
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
def calculate_and_get_statistics():
    def calculate_statistics():
        pass
        # Funciona !!!
        # list_id_leagues = [3504]
        # # open_browser.catch_match()
        # prepare_data_for_statistics_all_teams(list_id_leagues)

    def get_statistics():
        # Obtener IDs de las ligas.
        ids_leagues_get = see_options(repeat_num=1)
        # Ejemplo: ids_leagues_get = (6093, [])

        # Obtener los nombres de los equipos de las ligas seleccionadas en la función anterior
        names_teams_get = see_options(repeat_num=2, id_get=ids_leagues_get[0])
        # Ejemplo: names_teams_get = ('Union De Santa Fe', ['Atenas', 'Union De Santa Fe'])
        print(names_teams_get)

        # Obtener las estadísticas de los equipos seleccionados en la función anterior.
        show_statistics(id_leagues_get=ids_leagues_get[0], tuple_names_teams=tuple(names_teams_get[1]))

    while True:
        try:
            select_calc_or_get = int(input('\nSeleccione:\n\t1: Obtener estadísticas.\n\t2: Calcular estadísticas.\n\t0: SALIR.\n\n\t-> '))

            if select_calc_or_get == 1:
                get_statistics()

            elif select_calc_or_get == 2:
                calculate_statistics()

            elif select_calc_or_get == 0:
                break

            else:
                print('\tIngrese un número que esté dentro de la lista.\n')

        except Exception:
            print('\tEl character ingresado no es un número.\n')

    # # Solicitud de información a la tabla "analysis_basketball".teams con el id de liga dado
    # list_id_leagues = [3504]
# END --------- STATISTICS                                                                                         # # #
# ==================================================================================================================== #


def see_forecast():
    pass

    # query = '''SELECT name_league, id_league
    #            FROM leagues
    #            ORDER BY name_league ASC'''
    # # list_leagues :: lista de tuplas,
    # # cada tupla con dos posiciones (name_league, id_league)
    # list_leagues = fs_select_row(query)
    # del query
    #
    # # Usar la función show_options(
    # msn_to_show = '\nSeleccione la liga del (los) equipo()s a análizar:'
    # msn_to_show_leagues = show_options(list_with_options=list_leagues, msn_to_show=msn_to_show)


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



# ==================================================================================================================== #
# FUNCTIONS CALLS                                                                                                      #
# ==================================================================================================================== #
# # Cargar nueva data al historial de equipos y sus estadísticas en cada liga,
# # para guardar en la base de datos.
# new_league_history()


# # Actualizar historial de equipos y sus estadísticas en cada liga,
# # para guardar en la base de datos.
# update_history()


# # Calcular estadísticas
# calculate_and_get_statistics()

# # Obtener estadísticas de los equipos
# calculate_and_get_statistics.get_statistics()


# # Ver pronósticos de un o dos equipo.
# see_forecast()
# END --------- FUNCTIONS CALLS                                                                                    # # #
# ==================================================================================================================== #


# prepare_data_for_statistics_all_teams(list_id_leagues=[2559])
# prepare_data_for_statistics_one_team(id_league=2559, name_team='Milwaukee Bucks')

# prepare_data_for_statistics_all_teams(5722)
id_league = 8122
name_home = 'Nymburk'
name_away = 'Pardubice'
analysis_x_teams(id_league, name_home, name_away)