import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from check_db_and_controllers.check_data_in_db import check_name_league as ck_name_league
from check_db_and_controllers.check_data_in_db import list_names_leagues as ck_list_name_league
from history_match.history_functions_shared import search_button, get_id_league_currently, send_data_to_db
from statistics_dir.calculate_statistics import prepare_data_for_statistics_all_teams


def catch_data(list_links_leagues):
    # ================================================================================================================ #
    # CHROME DRIVER CONNECTION                                                                                         #
    # ================================================================================================================ #
    options = webdriver.ChromeOptions()
    options.binary_location = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'
    driver_path = "../drivers/chromedriver.exe"
    driver = webdriver.Chrome(options=options, executable_path=driver_path)
    driver.maximize_window()
    # END --------- CHROME DRIVER CONNECTION                                                                           #
    # ================================================================================================================ #

    count_league = 0
    count_match = 1

    # Iterar sobre la lista de tuplas obtenida con los link de las ligas.
    for links_by_country in list_links_leagues[count_league:]:

        # ============================================================================================================ #
        # NOMBRE DE LA LIGA                                                                                            #
        # ============================================================================================================ #
        # Parámetro para recargar la página para cada liga (link en la tuple "links_by_country").
        new_tab_open = links_by_country
        # Ej: new_tab_open = "https://www.flashscore.co/baloncesto/italia/serie-a2/resultados/" :: str

        # List a partir de la url de la liga.
        new_tab_open_split = new_tab_open.split('/')
        # Ej: new_tab_open = ['https', '','www.flashscore.co', 'baloncesto', 'italia', 'serie-a2', 'resultados']

        # Extracción del nombre de la url (de la lista "new_tab_open_split").
        new_name_league = f"{new_tab_open_split[4]} - {new_tab_open_split[5]}"
        # Ej: new_name_league = "italia - serie-a2"
        print(new_name_league)
        # END --------- NOMBRE DE LA LIGA                                                                          # # #
        # ============================================================================================================ #

        # Abrir o recargar la página con la url de la liga actual "new_tab_open"
        driver.get(new_tab_open)

        # ============================================================================================================ #
        # BUSCAR Y DAR CLIC SOBRE EL CSS_SELECTOR DEL BOTÓN                                                            #
        # ============================================================================================================ #
        # Clic sobre el CSS_SELECTOR encontrado dentro de la página.
        # driver.execute_script("arguments[0].click();", button)
        while True:
            try:
                button = search_button(driver, '#live-table > div.event.event--results > div > div > a')
                driver.execute_script("arguments[0].click();", button)
                time.sleep(3)
                print('Click on button "Mostrar más partidos"')

            except Exception as e:
                print(e)
                break
        # Liberar espacio de almacenamiento para evitar fugas de memoria
        # END --------- BUSCAR Y DAR CLIC SOBRE EL CSS_SELECTOR DEL BOTÓN                                          # # #
        # ============================================================================================================ #

        # ============================================================================================================ #
        # ENVIAR NOMBRE DE LA LIGA A LA TABLEA "league" Y OBTENER ID DE LA LIGA.                                       #
        # ============================================================================================================ #
        # Enviar nombre de liga , sí no existe, a la tabla "analysis_basketball.leagues".
        ck_name_league(new_name_league, new_tab_open)

        # Obtener id (analysis_basketball.leagues.id_league) de la liga actual
        current_id_league = get_id_league_currently(ck_list_name_league[-1])
        # END --------- ENVIAR NOMBRE DE LA LIGA A LA TABLEA "league" Y OBTENER ID DE LA LIGA.                     # # #
        # ============================================================================================================ #

        # ============================================================================================================ #
        # GET A LOAD DATA TO LEAGUE                                                                                    #
        # ============================================================================================================ #
        # Obtener la data de todos los partidos cargados en el DIV
        try:
            div_data = driver.find_element(By.CSS_SELECTOR, '#live-table > div.event.event--results > div > div').text.splitlines()

        except Exception as e:
            print(f'X*X*X*X* EXCEPTION X*X*X*X*\n\tIN: GET A LOAD DATA TO LEAGUE\n{e}')

        # Patrones de re (expresiones regulares) para las fechas
        patron_fecha = re.compile(r"\d{2}\.\d{2}\. \d{2}:\d{2}")
        patron_hora = re.compile(r'. \d{2}:\d{2}')

        # Limite superior de la lista de cada partido
        upper_limit = None

        try:
            # Buscar patron de fechas en cada posición de la lista main
            # Se itera desde la última posición hasta la primera.
            for i_list_all_data in range(-1, ((-1) * len(div_data)), -1):
                # ==================================================================================================== #
                # SEPARAR Y LIMPIAR LOS DATOS DE CADA PARTIDO                                                          #
                # ==================================================================================================== #
                # Determinar si la posición cumple con el patrón de fecha establecido.
                match = patron_fecha.search(div_data[i_list_all_data])

                if match:
                    # Limpiar de la fecha, los datos que informan la hora del partido.
                    # No es relevante esta información.
                    div_data[i_list_all_data] = patron_hora.sub('', div_data[i_list_all_data]).replace('.', '/')

                    # Ajustar formato de fecha según MySql (AÑO/MES/DÍA),
                    # y adicionar el año, ya que en la página de "mismarcadores" solo registra mes y día
                    if int(div_data[i_list_all_data][3:]) > 8:
                        date_match = f'22/{div_data[i_list_all_data][3:]}/{div_data[i_list_all_data][:2]}'
                        div_data[i_list_all_data] = date_match
                    else:
                        date_match = f'23/{div_data[i_list_all_data][3:]}/{div_data[i_list_all_data][:2]}'
                        div_data[i_list_all_data] = date_match

                    # Lista con todos los datos de un solo partido.
                    list_data_match = div_data[i_list_all_data:upper_limit]
                    # Ejemplo: list_data_match = ['10-05', 'Real Madrid', 'Partizan', '98', '94', '22', '23', '17', '32', '30', '21', '29', '18']

                    is_over_time = False
                    if list_data_match[1] == 'Tras prórr.':
                        # El partido tiene over time
                        is_over_time = True

                        # Eliminar la posición que contiene 'Tras prórr.'
                        del (list_data_match[1])

                        if len(list_data_match) > 16:
                            # Eliminar datos adicionales innecesario en la lista del partido.
                            del (list_data_match[16:])

                        # Eliminar los puntajes obtenidos del overtime.
                        del (list_data_match[-2:])

                    else:
                        # El partido mo tiene over time.
                        if len(list_data_match) > 13:
                            # Eliminar datos adicionales innecesario en la lista del partido.
                            del (list_data_match[13:])

                    # Modificar el límite superior, con cada iteración, de cada lista única de un partido.
                    upper_limit = i_list_all_data
                    # ================================================================================================ #
                    # END ---------SEPARAR Y LIMPIAR LOS DATOS DE CADA PARTIDO                                     # # #

                    # ================================================================================================ #
                    # ASIGNAR DATOS DE LAS COLUMNAS DE LAS TABLAS                                                      #
                    # ================================================================================================ #
                    try:
                        name_home = list_data_match[1]
                        name_away = list_data_match[2]
                        points_final_home = int(list_data_match[3])
                        points_final_away = int(list_data_match[4])
                        q_1H = int(list_data_match[5])
                        q_1A = int(list_data_match[6])
                        q_2H = int(list_data_match[7])
                        q_2A = int(list_data_match[8])
                        q_3H = int(list_data_match[9])
                        q_3A = int(list_data_match[10])
                        q_4H = int(list_data_match[11])
                        q_4A = int(list_data_match[12])

                        is_win_home = False
                        if points_final_home > points_final_away:
                            is_win_home = True

                    except Exception as e:
                        print(f'X*X*X*X* EXCEPTION X*X*X*X*\n\tIN: ASIGNAR DATOS DE LAS COLUMNAS DE LAS TABLAS\n{e}')
                    # ================================================================================================ #
                    # END ---------ASIGNAR DATOS DE LAS COLUMNAS DE LAS TABLAS                                     # # #

                    # ================================================================================================ #
                    # SENDING DATA TO BD                                                                               #
                    # ================================================================================================ #
                    try:
                        # Duración de un quarto, en minutos.
                        time_quarter = 10
                        if new_name_league == 'usa - nba':
                            time_quarter = 12
                        print('time_quarter: ' + str(time_quarter))

                        # Nombre de los 2 equipos del partido
                        list_names_teams = [name_home, name_away]

                        send_data_to_db(list_names_teams, current_id_league, date_match, points_final_home, q_1H, q_2H,
                                        q_3H, q_4H, is_over_time, is_win_home, points_final_away, q_1A, q_2A, q_3A, q_4A,
                                        time_quarter)

                        count_match += 1

                        del list_names_teams, date_match, points_final_home, q_1H, q_2H, q_3H, q_4H, \
                            is_over_time, is_win_home, points_final_away, q_1A, q_2A, q_3A, q_4A, time_quarter

                    except Exception as e:
                        print(f'X*X*X*X* EXCEPTION X*X*X*X*\n\tIn SENDING DATA TO BD\n {e}')
                    # ================================================================================================ #
                    # END ---------SENDING DATA TO BD                                                              # # #

                print('\n')

        except Exception as e:
            print(f'X*X*X*X* EXCEPTION X*X*X*X*\n\tGET A LOAD DATA TO EACH LEAGUE \n {e}')

        finally:
            # Enviar data a "t_gral_statistics"
            prepare_data_for_statistics_all_teams(current_id_league)

            print('''Final historial de partidos de la liga actual.
            Iniciar nueva DATA COLLECTION con la siguiente liga.''')

            print(f'\nNúmero de partidos hasta ahora: {count_match}\nCambio de liga.')

            if count_match > 1700:
                break

    # END --------- GET A LOAD DATA TO EACH LEAGUE                                                                 # # #
    # ================================================================================================================ #

    # Cerrar navegador
    driver.quit()
