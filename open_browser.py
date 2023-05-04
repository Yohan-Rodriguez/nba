import textwrap
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import check_db.check_data_in_db as ck
from conn import connections
import links
import xpaths_verification


# ==================================================================================================================== #
# OPEN BROWSER                                                                                                         #
# ==================================================================================================================== #
def conn_web():
    website = 'https://www.sofascore.com/basketball'
    options = webdriver.ChromeOptions()
    options.binary_location = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'
    driver_path = 'drivers\chromedriver.exe'
    driver_path = "..\drivers\chromedriver.exe"
    driver = webdriver.Chrome(options=options, executable_path=driver_path)

    driver.maximize_window()
    driver.get(website)

    # ================================================================================================================ #
    # ACCESS LINKS LEAGUES                                                                                             #
    # ================================================================================================================ #
    # Top Leagues (xpath_league es el xplath de la etiqueta "<div>" que contiene varias etiquetas "<a>" dentro de ella):
    xpath_league = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[1]/div[1]/div[1]/div[3]/div[2]')

    # Extraer los atributos href de todas las etiquetas "<a>".
    list_links_leagues = links.search_links(xpath_league)

    # Eliminar la "fiba-world-cup" porque no ha iniciado aún
    list_links_leagues.remove('https://www.sofascore.com/tournament/basketball/international/fiba-world-cup/441')
    # list_links_leagues.remove('https://www.sofascore.com/tournament/basketball/usa/nba/132')
    # list_links_leagues.remove('https://www.sofascore.com/tournament/basketball/international/euroleague/138')
    # list_links_leagues.remove('https://www.sofascore.com/tournament/basketball/greece/a1/304')
    # list_links_leagues.remove('https://www.sofascore.com/tournament/basketball/italy/serie-a/262')
    # list_links_leagues.remove('https://www.sofascore.com/tournament/basketball/spain/liga-acb/264')
    # list_links_leagues.remove('https://www.sofascore.com/tournament/basketball/international/admiralbet-aba-league/235')
    list_links_leagues.remove('https://www.sofascore.com/tournament/basketball/brazil/nbb/1562')

    # eurocup tiene unos xpath que aún no he definido
    list_links_leagues.remove('https://www.sofascore.com/tournament/basketball/international/eurocup/141')

    # END --------- ACCESS LINKS LEAGUES                                                                           # # #
    # ================================================================================================================ #

    # ================================================================================================================ #
    # FUNCTION search_button()                                                                                         #
    # ================================================================================================================ #
    # Si la función "search_button()" no logra encontrar el "button.previously"
    # me regresa un String vació
    def search_button(xpath):
        # Salida de emergencia al siguiente bucle para evitar que sea infinito
        flag_emergency_button = 5

        while True:
            try:
                button_previous = driver.find_element(By.XPATH, xpath)
                break

            except Exception:
                print(f'Reintentando obtener XPATH de "button.previously".\nTiempo Restante: -{flag_emergency_button} s')
                time.sleep(1)

                if flag_emergency_button <= 0:
                    button_previous = ''
                    break

                flag_emergency_button -= 1

        return button_previous
    # END --------- FUNCTION search_button()                                                                           #
    # ================================================================================================================ #

    # ================================================================================================================ #
    # ACCESS NEW LEAGUES                                                                                               #
    # ================================================================================================================ #
    # Parámetro para cambiar de liga
    change_league = 0

    # Bucle para recorrer todas las ligas
    while True:
        # ============================================================================================================ #
        # NOMBRE DE LA LIGA Y ENVIAR DATA A LA TABLE "basketball.leagues"                                              #
        # ============================================================================================================ #
        # Parámetro para recargar la página para cada liga (link en la lista "list_links_leagues").
        new_tab_open = list_links_leagues[change_league]
        # Ej: new_tab_open = "https://www.sofascore.com/tournament/basketball/international/euroleague/138" :: str

        # List a partir de la url de la liga.
        new_tab_open_split = new_tab_open.split('/')
        # Ej: new_tab_open = ['https', '','www.sofascore.com', 'tournament', 'basketball', 'international', 'euroleague', '138']

        # Extracción del nombre de la url (de la lista "new_tab_open_split").
        new_name_league = f"{new_tab_open_split[5]} - {new_tab_open_split[6]}"
        # Ej: new_name_league = "international - euroleague"
        print(new_name_league)

        # Enviar nombre de liga a la tabla "analysis_basketball.leagues".
        try:
            ck.check_name_league(new_name_league)
            query = f'''SELECT id_league FROM leagues 
                        WHERE name_league = "{ck.list_names_leagues[-1]}"'''
            current_id_league = connections.select_row(query)[0][0]

            # END --------- NOMBRE DE LA LIGA Y ENVIAR DATA A LA TABLE "basketball.leagues"                            # # #
            # ============================================================================================================ #

            # Recargar la página
            driver.get(f'{new_tab_open}')

            # ============================================================================================================ #
            # BUSCAR SECCIÓN "MATCHES"                                                                                     #
            # ============================================================================================================ #
            # Llamada de la función "search_button()" según la estructura a de la página de cada liga
            # y determinar XPATH del partido número [10] de la sección "MATCH"

            # Bandera para borrar los Xpath obtenidos dentro del for de los 10 partidos
            # Sí es 0, borrará los impares
            flag_xpath = 0

            # Devuelve una lista con los xpaths "match "return list_xpath_match"
            # "return list_xpath_match"
            xpath_to_used_match = xpaths_verification.verification_xpath_match()

            # El XPATH en el if y el elif son propios de cada página y determinan los xpaths que se utilizaran
            if driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[1]/div[2]/div[2]/div[3]').is_displayed():
                xpath_search_match = driver.find_element(By.XPATH, xpath_to_used_match[0])

                # Retorna una lista de una sola posición
                # Para borrar las posiciones impares, enviar "delete=1"
                # "return list_xpath_button_previously"
                xpath_button_previously = xpaths_verification.delete_xpath_button(delete=1)

                flag_xpath = 1

            elif driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[1]/div[2]/div[2]/div[5]').is_displayed():
                xpath_search_match = driver.find_element(By.XPATH, xpath_to_used_match[1])

                # Para borrar las posiciones pares, enviar "delete=0"
                xpath_button_previously = xpaths_verification.delete_xpath_button(delete=0)

                flag_xpath = 0

            # Desplazamiento a la sección "MATCHES"
            xpath_search_match.click()
            # END --------- BUSCAR SECCIÓN "MATCHES"                                                                   # # #
            # ============================================================================================================ #

            # controladores del "button_previously"
            # Clics iniciales en "button.previous" cada vez que se recarga la página inicial
            count_initial_clicks = 0
            # Número de clics sobre "button.previous" durante la ejecución del programa
            count_match_clicks = 70

            # ============================================================================================================ #
            # RELOAD PAGES                                                                                                 #
            # ============================================================================================================ #
            # Bandera para ser usada en caso de que el historial se termine y salir del 'while "RELOAD PAGES"'
            flag_end_history = False

            # Bucle encargado de recargar la página cada "count_match_clicks" clics en button.previous en "POST INITIAL"
            while True:
                # ======================================================================================================== #
                # CLICK ON PREVIOUS (INITIAL)                                                                              #
                # ======================================================================================================== #
                if count_initial_clicks > 0:
                    # Salida de emergencia del while
                    flag_exit_emergency = 1

                    # Parámetro que inicializa el número de veces que se dará clic sobre "button.previous"
                    count_initial_clicks_temp = 0

                    while count_initial_clicks_temp < count_initial_clicks:
                        # Parámetro del botón previously
                        button_previous = search_button(xpath_button_previously[0])

                        try:
                            if button_previous.is_displayed():
                                # Clic sobre el "button.previous"
                                driver.execute_script("arguments[0].click();", button_previous)

                                print(f'Button: {count_initial_clicks_temp}')
                                count_initial_clicks_temp += 1

                        except Exception:
                            # "button_previous = search_button(xpath_button_previously[0])" retorno como un String vacío
                            # "button.previously" desapareció de la página (Se termino el historiaL)
                            print(f'EXCEPTION CLICK in PREVIOUS (INITIAL).\nRevisar partidos de está liga.')
                            flag_end_history = True
                            break

                    if flag_end_history:
                        # Terminar la liga actual, porque tiene errores para ser leida,
                        # y continuar con la proxima liga
                        break
                # END --------- CLICK ON PREVIOUS (INITIAL)                                                            # # #
                # ======================================================================================================== #

                # ======================================================================================================== #
                # DIV 10 MATCH                                                                                             #
                # ======================================================================================================== #
                # Bandera para controlar las 'n' oportunidades que se dará clic sobre "button.previous" en POST INITIAL.
                # dependiendo de "count_match_clicks"
                count_match_clicks_test = 0

                # Bucle para darle 'n' clics sobre el "button.previous" dependiendo de "count_match_clicks".
                while count_match_clicks_test < count_match_clicks:
                    # ==================================================================================================== #
                    # RECORRE EL <div> QUE CONTIENE LOS 10 MATCHES                                                         #
                    # ==================================================================================================== #
                    # Bucle para extraer información cada vez que se hace clic en 'Previous' con el 'button_previous.clic()'.
                    # Se cargan 10 partidos con cada clic sobre "button.previous":

                    for match in range(10, 0, -1):
                        try:
                            # ============================================================================================ #
                            # VERIFICAR QUE EL PARTIDO YA HAYA FINALIZADO                                                  #
                            # ============================================================================================ #
                            # No uso try-except porque es poco probable que ocurra en esta sección
                            # Si ocurre una exception, esta se atrapa en "EXCEPTIONS CONTROL"

                            # Lista con los paths que funcionan en la liga actual
                            # "return list_xpath_to_used"
                            xpath_to_use_gral = xpaths_verification.delete_xpath_with_match(delete=flag_xpath, match=match)

                            # Fecha del partido
                            div_date_match_main = driver.find_element(By.XPATH, xpath_to_use_gral[0]).text
                            div_date_match_2 = driver.find_element(By.XPATH, xpath_to_use_gral[0]).text.split('/')

                            # Parámetro para verificar si el partido ha finalizado ("FT" or "AET")
                            div_FT_match_test = driver.find_element(By.XPATH, xpath_to_use_gral[1]).text

                            # Inicialización de la bandera para seguir o no con el proceso, sí el partido ya finalizó
                            flag_ft = False

                            # si el partido ya finalizó:
                            if div_date_match_main.__contains__('/') and (div_FT_match_test.__contains__('FT') or div_FT_match_test.__contains__('AET')):
                                # Formato de fecha para enviar a la base de datos
                                date_match = ''.join([div_date_match_2[2], '-', div_date_match_2[1], '-' + div_date_match_2[0]])

                                flag_ft = True
                            # END --------- VERIFICAR QUE EL PARTIDO YA HAYA FINALIZADO                                # # #
                            # ============================================================================================ #

                            while flag_ft:
                                # ======================================================================================== #
                                # DATA COLLECTION                                                                          #
                                # ======================================================================================== #
                                try:

                                    # Nombre de los equipos:
                                    div_name_home = driver.find_element(By.XPATH, xpath_to_use_gral[2]).text
                                    div_name_away = driver.find_element(By.XPATH, xpath_to_use_gral[3]).text

                                    # Lista str con los puntos por cuarto de home y away
                                    div_list_PointsHome = driver.find_element(By.XPATH, xpath_to_use_gral[4]).text.splitlines()
                                    div_list_PointsAway = driver.find_element(By.XPATH, xpath_to_use_gral[5]).text.splitlines()

                                    # Puntos finales de home y away.
                                    div_points_final_home = int(driver.find_element(By.XPATH, xpath_to_use_gral[6]).text)
                                    div_points_final_away = int(driver.find_element(By.XPATH, xpath_to_use_gral[7]).text)

                                except Exception:
                                    print('Exception in DATA COLLECTION.')
                                # ======================================================================================== #
                                # END --------- DATA COLLECTION                                                            #
                                # ======================================================================================== #

                                # ======================================================================================== #
                                # CASTEO STR-TO-INT PUNTOS POR CUARTO DE CADA EQUIPO                                       #
                                # ======================================================================================== #
                                try:
                                    # Listas para guardar los puntos X cuarto para cada equipo.
                                    div_list_PointsHome_Int = []
                                    div_list_PointsAway_Int = []

                                    for casteo_int in range(len(div_list_PointsHome)):
                                        # Puntos de cada cuarto en formato INTEGER para Home
                                        div_list_PointsHome_Int.append(int(div_list_PointsHome[casteo_int]))

                                        # Puntos de cada cuarto en formato INTEGER para Away
                                        div_list_PointsAway_Int.append(int(div_list_PointsAway[casteo_int]))

                                except Exception:
                                    print('Exception in CASTEO STR-TO-INT PUNTOS POR CUARTO DE CADA EQUIPO.')
                                # END --------- CASTEO STR-TO-INT PUNTOS POR CUARTO DE CADA EQUIPO                     # # #
                                # ======================================================================================== #

                                # ======================================================================================== #
                                # VERIFICAR OVERTIME (OT)                                                                  #
                                # ======================================================================================== #
                                try:
                                    # Si el partido tiene OverTime:
                                    if div_FT_match_test.__contains__('AET'):
                                        # Add que el partido si tuvo overtime.
                                        over_time = True

                                    # Si el partido no tiene OverTime:
                                    else:
                                        # Add que el partido no tuvo overtime
                                        over_time = False

                                except Exception:
                                    # Imprimir Type Exception
                                    print('Exception in OVERTIME VERIFICATION')
                                # END --------- VERIFICAR OVERTIME (OT)                                                # # #
                                # ======================================================================================== #

                                # ======================================================================================== #
                                # PREPARAR Y ENVIAR LA DATA A LA BD                                                        #
                                # ======================================================================================== #
                                try:
                                    q_1H = div_list_PointsHome_Int[0]
                                    q_1A = div_list_PointsAway_Int[0]
                                    q_2H = div_list_PointsHome_Int[1]
                                    q_2A = div_list_PointsAway_Int[1]
                                    q_3H = div_list_PointsHome_Int[2]
                                    q_3A = div_list_PointsAway_Int[2]
                                    q_4H = div_list_PointsHome_Int[3]
                                    q_4A = div_list_PointsAway_Int[3]

                                    # Determinar si el equipo ganó o perdió.
                                    is_win_home = False
                                    is_win_away = False
                                    if (div_points_final_home - div_points_final_away) > 0:
                                        is_win_home = True
                                    else:
                                        is_win_away = True

                                    # ==================================================================================== #
                                    # SENDING DATA TO BD                                                                   #
                                    # ==================================================================================== #

                                    # Función para enviar los datos a "t_teams" y "t_matches" ============================ #
                                    def send_data_to_team_and_match(team_id_team, id_match, date_match, is_home,
                                                                    total_points, q_1, q_2, q_3, q_4, over_time, is_win,
                                                                    home_or_away):

                                        # Enviar data a "t_matches"
                                        print(f'Sending data to "analysis_basketball.matches" for {home_or_away}.')
                                        connections.conn_db_table_matches(id_match, date_match, is_home, total_points, q_1,
                                                                          q_2, q_3, q_4, over_time, is_win)

                                        # Enviar data a "t_team_has_matches"
                                        print(f'Sending data to "analysis_basketball.team_has_matches" for {home_or_away}.')
                                        connections.conn_db_table_team_has_matches(team_id_team, id_match)
                                    # END --------- Función para enviar los datos a "t_teams" y "t_matches" ============== #

                                    try:
                                        list_names_teams = [div_name_home, div_name_away]

                                        # 2 repeticiones:
                                        # i_send_data_t_team == 0 para home y
                                        # i_send_data_t_team == 1 para away.
                                        for i_send_data_t_team in range(2):
                                            id_match = ck.check_id_match()

                                            # Verificar que el nombre de los equipos están o no, relacionados en "t_team"
                                            # Sí el equipo no existe en t_teams, se guarda dentro del scope de la función
                                            # "ck.check_name_team"
                                            team_id_team = ck.check_name_team(list_names_teams[i_send_data_t_team],
                                                                              current_id_league,
                                                                              home_or_away=i_send_data_t_team)

                                            if i_send_data_t_team == 0:
                                                # Enviar data de home a "t_matches"
                                                send_data_to_team_and_match(team_id_team, id_match, date_match, True,
                                                                            div_points_final_home, q_1H, q_2H, q_3H, q_4H,
                                                                            over_time, is_win_home,
                                                                            home_or_away=i_send_data_t_team)

                                            elif i_send_data_t_team == 1:
                                                # Enviar data de away a "t_team" y a "t_matches"
                                                send_data_to_team_and_match(team_id_team, id_match, date_match, False,
                                                                            div_points_final_away, q_1A, q_2A, q_3A, q_4A,
                                                                            over_time, is_win_away,
                                                                            home_or_away=i_send_data_t_team)

                                        print('Completed Finish match -----------------------------')

                                    except Exception as e:
                                        print(f'Exception in SENDING DATA TO BD\n {e}')

                                    break
                                    # ==================================================================================== #
                                    # END --------- SENDING DATA TO BD                                                     #
                                    # ==================================================================================== #

                                except Exception as e:
                                    # print Exception
                                    print(f'Exception in PREPARAR Y ENVIAR LA DATA A LA DB.\n{e}')
                                # END --------- PREPARAR Y ENVIAR LA DATA A LA BD                                      # # #
                                # ======================================================================================== #

                        # ================================================================================================ #
                        # EXCEPTIONS CONTROL                                                                               #
                        # ================================================================================================ #
                        except Exception:
                            try:
                                try:
                                    name_league = ck.list_names_leagues[-1]
                                    query_league = f'SELECT id_league FROM leagues WHERE name = "{name_league}"'
                                    id_error = connections.select_row(query_league)

                                except Exception:
                                    id_error = 0000

                                # Envía Data del partido con error, a la tabla "basketball.errors" el ID de la liga y los nombres reales.
                                connections.connection_db_t_errors(id_error, date_match, div_name_home, div_name_away)

                            except Exception:
                                print('EXCEPTION INSIDE MATCH - NO DATA error.')

                                try:
                                    # Envía Data del partido con error, a la tabla "basketball.errors" con los nombres reales de los equipos.
                                    connections.connection_db_t_errors(id_error, '1993-06-21', div_name_home,
                                                                       div_name_away)

                                except Exception:
                                    try:
                                        # Envía Data por defecto del partido con error, a la tabla "basketball.errors"
                                        connections.connection_db_t_errors(id_error, '1993-06-21', 'No', 'No')

                                    except Exception as e:
                                        print(f'NO DATA FOR BD_error X+X+X+X+X+X+X+X+X+X+X+X\n{e}')
                                        continue

                                    continue

                                continue

                            continue
                        # END --------- EXCEPTIONS CONTROL                                                             # # #
                        # ================================================================================================ #

                    # END --------- RECORRER EL <div> QUE CONTIENE LOS 10 MATCHES                                      # # #
                    # ==================================================================================================== #

                    # ==================================================================================================== #
                    # CARGAR NUEVA SECCIÓN CON 10 PARIDOS NUEVOS DURANTE 7 OPORTUNIDADES                                   #
                    # ==================================================================================================== #
                    # Cuando se usan las 'n' oportunidades, se cierra y vuelve a abrir el navegador.
                    # Esto se da porque la página de "www.sofascore.com" se actualiza automáticamente

                    try:
                        # Parámetro del botón previously
                        button_previous = search_button(xpath_button_previously[0])

                        # Dar clic en "button.previous" por medio de un script de js
                        driver.execute_script("arguments[0].click();", button_previous)

                        count_match_clicks_test += 1

                    except Exception:
                        try:
                            # Parámetro del botón previously
                            button_previous = search_button(xpath_button_previously[0])

                            # Dar clic en "button.previous" por medio de un script de js
                            driver.execute_script("arguments[0].click();", button_previous)

                            count_match_clicks_test += 1

                        except Exception:
                            print(f'EXCEPTION CLICK in POST-INITIAL PREVIOUS.\nRevisar partidos de está liga.')
                            flag_end_history = True
                            break
                    # END --------- CARGAR NUEVA SECCIÓN CON 10 PARIDOS NUEVOS DURANTE 7 OPORTUNIDADES                 # # #
                    # ==================================================================================================== #

                if flag_end_history:
                    break

                count_initial_clicks += (count_match_clicks+1)
                print('Actualizar Página')
                driver.refresh()

            print(textwrap.dedent('''Final historial de partidos de la liga actual.
                                 Iniciar nueva DATA COLLECTION con la siguiente liga.'''))

            # ============================================================================================================ #
            # END --------- RELOAD PAGES                                                                                   #
            # ============================================================================================================ #
        except Exception as e:
            print(e)

        if (len(list_links_leagues)-1) > change_league:
            change_league += 1
            print('Cambio de liga.')

        else:
            print('Fin de las ligas.')
            break
    # ================================================================================================================ #
    # END --------- ACCESS LEAGUES                                                                                     #
    # ================================================================================================================ #

    # Cerrar navegador
    driver.quit()
# END --------- OPEN BROWSER                                                                                       # # #
# ==================================================================================================================== #


# ==================================================================================================================== #
# CAPTAR 70 PARTIDOS Y RECARGAR PÁGINA                                                                                 #
# ==================================================================================================================== #
def catch_match():
    try:
        # Llamada de la función
        conn_web()

        print('PROGRAM SUCCESSFULLY COMPLETED without errors.')

    except Exception as e:
        print(f'END Error FATAL.\nFIN DEL PROGRAMA CON ERRORES\n{e}')
# ==================================================================================================================== #
# END --------- CAPTAR 70 PARTIDOS Y RECARGAR PÁGINA                                                                   #
# ==================================================================================================================== #
