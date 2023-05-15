import time
import unicodedata
from selenium import webdriver
from selenium.webdriver.common.by import By
from check_db_and_controllers.check_data_in_db import check_id_match as ck_match
from conn.connections import conn_db_table_teams_has_matches as conn_db_teams_has_matches
from conn.connections import conn_db_table_matches as conn_db_matches
from check_db_and_controllers.check_data_in_db import check_name_team as ck_name
from conn.functions_shared import select_row as fs_select_row


# ================================================================================================================ #
# Función para enviar los datos a "t_teams" y "t_matches"                                                          #
# ================================================================================================================ #
def send_data_to_teams_and_matches(teams_id_team, id_match, date_match, is_home, total_points, q_1, q_2, q_3, q_4,
                                   over_time, is_win, home_or_away):
    # Enviar data a "t_matches"
    print(f'Sending data to "analysis_basketball.matches" for {home_or_away}.')
    conn_db_matches(id_match, date_match, is_home, total_points, q_1, q_2, q_3, q_4, over_time, is_win)

    # Enviar data a "t_teams_has_matches"
    print(f'Sending data to "analysis_basketball.teams_has_matches" for {home_or_away}.')
    conn_db_teams_has_matches(teams_id_team, id_match)
# END --------- Función para enviar los datos a "t_teams" y "t_matches" ============== #


def cath_data():
    # ================================================================================================================ #
    # CHROME DRIVER CONNECTION                                                                                         #
    # ================================================================================================================ #
    options = webdriver.ChromeOptions()
    options.binary_location = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'
    driver_path = "../drivers/chromedriver.exe"
    driver = webdriver.Chrome(options=options, executable_path=driver_path)
    driver.maximize_window()
    driver.get('https://www.flashscore.co/baloncesto/')
    # END --------- CHROME DRIVER CONNECTION                                                                           #
    # ================================================================================================================ #

    # ================================================================================================================ #
    # BUSCAR CSS_SELECTOR BUTTON                                                                                       #
    # ================================================================================================================ #
    def search_button(selector_css_button):
        # Salida de emergencia al siguiente bucle para evitar que sea infinito
        flag_emergency_button = 5

        while True:
            try:
                button_previous = driver.find_element(By.CSS_SELECTOR, selector_css_button)
                break

            except Exception:
                print(f'Reintentando obtener XPATH de "Mostrar Más partidos".\nIntentos Restante: -{flag_emergency_button} s')
                time.sleep(2)

                if flag_emergency_button <= 0:
                    button_previous = ''
                    break

                flag_emergency_button -= 1

        return button_previous
    # END --------- BUSCAR CSS_SELECTOR BUTTON                                                                         #
    # ================================================================================================================ #

    # ================================================================================================================ #
    # SEARCH DAY IN CALENDAR.                                                                                          #
    # ================================================================================================================ #
    button = search_button('#live-table > div.filters > div.filters__group > div:nth-child(4) > div')
    driver.execute_script("arguments[0].click();", button)
    time.sleep(3)
    print('Click on button "FINALIZADOS"')

    button_calendar = search_button('#live-table > div.filters > div.calendarCont > div > button.calendar__navigation.calendar__navigation--yesterday')
    driver.execute_script("arguments[0].click();", button_calendar)
    time.sleep(3)
    print('Click on button "CALENDAR"')

    date_match_div = driver.find_element(By.CSS_SELECTOR, '#calendarMenu').text
    # Ejemplo "date_match_div" = '14/05 DO'

    # Ajustar formato de fecha según MySql (AÑO/MES/DÍA),
    date_match = f'23/{date_match_div[3:5]}/{date_match_div[:2]}'
    print(date_match)
    # END --------- SEARCH DAY IN CALENDAR.                                                                            #
    # ================================================================================================================ #

    # Obtener la data de todos los partidos cargados en el DIV
    try:
        div_data = driver.find_element(By.CSS_SELECTOR, '#live-table').text.splitlines()

    except Exception as e:
        print(f'X*X*X*X* EXCEPTION X*X*X*X*\n\tIN: GET A LOAD DATA TO LEAGUE\n{e}')

    # Eliminar las 5 primera posiciones ['TODOS', 'EN DIRECTO', 'CUOTAS', 'FINALIZADOS', 'PRÓXIMOS', '12/05 VI']
    del div_data[:6]

    # Dictionary para almacenar los equipos, agrupados por ligas, que actualizaran la DB.
    dict_leagues_teams = {}

    # Lista temporal con los nombres de las ligas para adjuntar el nombre correspondiente al diccionario "dict_leagues_teams"
    list_names_leagues = []

    # Almacenar los datos de los equipos de una liga dada y al final de cada liga, se limpia la lista (.clear())
    list_dict_teams_temp = []

    # Bandera para enviar los datos al diccionario cada vez que se inicia el censo de data en una nueva liga.
    flag_change_league = 0

    # Contador de número de iteraciones.
    temp_div = 0

    # ================================================================================================================ #
    # EXTRAER INFORMACIÓN DE LOS PARTIDOS.                                                                             #
    # ================================================================================================================ #
    # Iterar sobre "div_data" para extraer información de los partidos
    while True:
        # Si temp_div llega al final de la lista "div_data", se termina las iteraciones ============================== #
        if temp_div >= len(div_data):
            break
        # ============================================================================================================ #

        # ============================================================================================================ #
        # VERIFICAR PATRON DE INFORMACIÓN: LIGA - PARTIDO.                                                             #
        # ============================================================================================================ #
        # Iterar sobre cada conjunto de datos que pertenecen a un solo parido.
        # Los conjuntos de datos de un solo partido se establecen dentro del siguiente while.
        while True:
            # El patrón regular de inicio de un conjunto de datos de un partido está dado por 6 o 3 posiciones:
            # Ejemplo de 6 posiciones: ['AUSTRALIA', 'NBL1 North Women', 'Clasificación', 'Finalizado', 'Cairns F', 'Mackay Meteorettes F']
            # Ejemplo de 3 posiciones: ['Finalizado', 'Taurinos', 'Trotamundos']
            # Sí se cumple el patrón de 6 posiciones, indica grupo de partidos de una nueva liga.
            # Sí se cumple el patrón de 3 posiciones, indica que la iteración actual hace referencia de un partido de
            # la liga que cumplió el patron inmediatamente anterior, de 6 posiciones.
            if all((isinstance(item, str) and not item.isdigit()) for item in div_data[temp_div:temp_div + 6]):
                # Sí hay un cambio de liga, se carga el diccionario "dict_leagues_teams"
                # con la información de la liga, y partidos de ella, anterior.
                flag_change_league += 1
                if flag_change_league > 1:
                    dict_leagues_teams[f'{list_names_leagues[-1]}'] = list_dict_teams_temp.copy()
                    list_dict_teams_temp.clear()
                    flag_change_league -= 1

                # "name_country" es la posición "temp_div" actual de "div_data"
                # Se realiza una limpieza sobre el nombre del país obtenido de la página web
                name_country = div_data[temp_div].replace(' ', '-').lower()
                name_country = unicodedata.normalize('NFKD', name_country).encode('ASCII', 'ignore').decode('utf-8')
                # Ejemplo: Se pasa de "ARGENTINA" a "argentina"

                # "name_league_temp" es la segunda posición de las 6 seguidas que son no números
                # Se realiza una limpieza sobre el nombre de la liga obtenido de la página web.
                name_league_temp = div_data[temp_div + 1].split('-')[0].lower()
                # Obtener nombre de liga únicamente, del string anterior.

                # Eliminar el espacio en blanco en la última posición
                # y eliminar puntos, si los hay, del nombre de liga.
                name_league_temp = name_league_temp.rstrip(name_league_temp[-1]).replace(' ', '-').replace('.', '')
                # Ejemplo: pasar de "LNB - Playoffs" a "lnb"
                # "NB I. A - Puestos 5º-8º" a "nb-i-a"

                # Eliminar tildes.
                name_league_temp = unicodedata.normalize('NFKD', name_league_temp).encode('ASCII', 'ignore').decode('utf-8')

                # nombre de la liga en formato de la DB "'nombre país' - 'nombre liga'"
                name_league = f'{name_country} - {name_league_temp}'

                # Agregar el nombre de la liga, para poder referenciar el nombre correcto de la liga
                # al diccionario "dict_leagues_teams"
                list_names_leagues.append(name_league)

                # tem_div toma la posición que indica si el partido finalizao sin o con overtime:
                temp_div += 3
                # Luego del nuevo valor de "temp_div", la nueva posición queda así:
                # div_data[temp_div] = 'Finalizado' :: (no overtime) o
                # div_data[temp_div] = 'Tras la prórroga' :: (si overtime)'
                break

            elif (all((isinstance(item, str) and not item.isdigit()) for item in div_data[temp_div:temp_div + 3])) and div_data[temp_div + 3].isdigit():
                # No se adiciona ningun valor a "temp_div" porque la actual posición "div_data[temp_div]"
                # tiene como referencia el valor de 'Finalizado' o 'Tras la prórroga'
                # que son los valores que se quieren obtener.
                break

            # Si no se cumple ninguno de los 2 patrones establecidos,
            # se da el caso de tener datos incompletos en el partido actual
            else:
                # Ejemplo: ['Finalizado', 'Vietnam F', 'Filipinas F', '58', '116'] No hay más datops en este partido.
                # Contar el número de datos no númericos en el actual partido con error en la data.
                for i in range(len(div_data[temp_div:temp_div + 13]) - 1):
                    sum_temp_div = 1
                    if (isinstance(div_data[temp_div + i], str) and not div_data[temp_div + i].isdigit()) and (
                            isinstance(div_data[temp_div + i + 1], str) and not div_data[temp_div + i + 1].isdigit()):
                        sum_temp_div += 1

                # Guardar la información del partido con error.
                list_match_error = [div_data[temp_div:temp_div + sum_temp_div]]

                # Sumar las posiciones, no numéricas, del partido con error a "temp_div"
                temp_div += sum_temp_div

                # Buscar la posición donde inicia el siguiente partido.
                for i in range(len(div_data[temp_div:temp_div + 13]) - 1):
                    sum_temp_div = 1
                    if div_data[temp_div + i].isdigit() and div_data[temp_div + i + 1].isdigit():
                        sum_temp_div += 1

                    if div_data[temp_div + i + 1].isdigit():
                        break

                # Establecer a "temp_div" sobre la posición donde inicia el nuevo aprtido.
                temp_div += sum_temp_div

                break
        # END --------- VERIFICAR PATRON DE INFORMACIÓN: LIGA - PARTIDO.                                                   #
        # ================================================================================================================ #

        # ================================================================================================================ #
        # EXTRAER INFORMACIÓN DEL PARTIDO.                                                                                 #
        # ================================================================================================================ #
        # Verificar si el partido tuvo o no overtime.
        over_time = False
        if div_data[temp_div] == "Finalizado":
            # Sí no tuvo overtime, verificar que las posiciones numericas sean 10:
            # 2 de puntajes finales y 8 de puntajes por cuartos.
            if all(isinstance(item, str) and item.isdigit() for item in div_data[temp_div + 3:temp_div + 13]):

                # Lista con la información relevante del partido actual.
                list_data_match_currently = [div_data[temp_div + 1], div_data[temp_div + 2], div_data[temp_div + 3 : temp_div + 13], over_time]
                # list_data_team = [Home, Away, [all_h, all_a, q1_h, q1_a, q2_h, q2_a, q3_h, q3_a, q4_h, q4_a], over_time]

                # Adicionar datos del partido a la lista general de la liga.
                list_dict_teams_temp.append(list_data_match_currently)

                # Liberar espacio de memoria usado por la lista creada en cada iteración.
                del list_data_match_currently

                # Establecer a "temp_div" sobre la posición donde inicia el nuevo aprtido.
                temp_div += 13

            # Sí no se cumple la condición,
            # indica que hay un error en la cantidad de datos de los puntos obtenidos del partdio actual.
            else:
                # Contar el número de datos (referentes a puntos) que hay de este partido
                for i in range(len(div_data[temp_div + 3:temp_div + 13]) - 1):
                    sum_temp_div = 1

                    if div_data[i].isdigit() and div_data[i + 1].isdigit():
                        sum_temp_div += 1

                # Establecer a "temp_div" sobre la posición donde inicia el nuevo aprtido.
                temp_div += (sum_temp_div + 3)

        elif div_data[temp_div] == "Tras la prórroga":
            over_time = True
            # Sí tuvo overtime, verificar que las posiciones numericas sean 10:
            # 2 de puntajes finales y 8 de puntajes por cuartos.
            if all(isinstance(item, str) and item.isdigit() for item in div_data[temp_div + 3:temp_div + 15]):

                # Lista con la información relevante del partido actual.
                list_data_match_currently = [div_data[temp_div + 1], div_data[temp_div + 2], div_data[temp_div + 3: temp_div + 13], over_time]
                # list_data_team = [Home, Away, [all_h, all_a, q1_h, q1_a, q2_h, q2_a, q3_h, q3_a, q4_h, q4_a], over_time]

                # Adicionar datos del partido a la lista general de la liga.
                list_dict_teams_temp.append(list_data_match_currently)

                # Liberar espacio de memoria usado por la lista creada en cada iteración.
                del list_data_match_currently

                # Establecer a "temp_div" sobre la posición donde inicia el nuevo partido.
                temp_div += 15

            # Sí no se cumple la condición,
            # indica que hay un error en la cantidad de datos de los puntos obtenidos del partido actual.
            else:
                # Contar el number de datos (referentes a puntos) que hay de este partido
                for i in range(len(div_data[temp_div + 3:temp_div + 15]) - 1):
                    sum_temp_div = 1

                    if div_data[i].isdigit() and div_data[i + 1].isdigit():
                        sum_temp_div += 1

                # Establecer a "temp_div" sobre la posición donde inicia el nuevo aprtido.
                temp_div += (sum_temp_div + 3)
        # END --------- EXTRAER INFORMACIÓN DEL PARTIDO.                                                               #
        # ============================================================================================================ #

    # END --------- EXTRAER INFORMACIÓN DE LOS PARTIDOS.                                                               #
    # ================================================================================================================ #

    # Adicionar la última liga y sus respectivos partidos al diccionario "dict_leagues_teams".
    dict_leagues_teams[f'{list_names_leagues[-1]}'] = list_dict_teams_temp

    # Liberar espacio de memoria usado por las listas "list_dict_teams_temp". y "list_names_leagues"
    del list_names_leagues
    del list_dict_teams_temp

    # Cerrar navegador
    driver.quit()

    for i_dict in dict_leagues_teams:
        print(i_dict, dict_leagues_teams[i_dict])
        print('\n')

        try:
            # ======================================================================================================== #
            # OBTENER ID DE LA LIGA.                                                                                   #
            # ======================================================================================================== #
            # Obtener id (analysis_basketball.leagues.id_league) de la liga actual
            query = f'''SELECT id_league FROM leagues
                        WHERE name_league = "{i_dict}"'''

            current_id_league = fs_select_row(query)[0][0]
            # END --------- OBTENER ID DE LA LIGA.                                                                 # # #
            # ======================================================================================================== #

            # Iterar sobre la lista que contiene la cantidad de partidos de cada liga.
            for i in range(len(dict_leagues_teams[i_dict])):
                list_names_teams = [dict_leagues_teams[i_dict][i][0], dict_leagues_teams[i_dict][i][1]]

                points_final_home = dict_leagues_teams[i_dict][i][2][0]
                points_final_away = dict_leagues_teams[i_dict][i][2][1]

                is_win_home = False
                if points_final_home > points_final_away:
                    is_win_home = True

                # 2 repeticiones:
                # i_send_data_t_team == 0 para home y
                # i_send_data_t_team == 1 para away.
                for i_send_data_t_team in range(2):
                    # Generar id_match
                    id_match = ck_match()

                    # Verificar que el nombre de los equipos están o no, relacionados en "t_team"
                    # Sí el equipo no existe en t_teams, se guarda dentro del scope de la función
                    # "ck.check_name_team"
                    teams_id_team = ck_name(list_names_teams[i_send_data_t_team], current_id_league,
                                            home_or_away=i_send_data_t_team)

                    if i_send_data_t_team == 0:
                        # Enviar data de home a "t_matches"
                        send_data_to_teams_and_matches(teams_id_team, id_match, date_match, True, points_final_home,
                                                       dict_leagues_teams[i_dict][i][2][2], dict_leagues_teams[i_dict][i][2][4],
                                                       dict_leagues_teams[i_dict][i][2][6], dict_leagues_teams[i_dict][i][2][8],
                                                       dict_leagues_teams[i_dict][i][3], is_win_home, home_or_away=i_send_data_t_team)

                    elif i_send_data_t_team == 1:
                        # Enviar data de away a "t_team" y a "t_matches"
                        send_data_to_teams_and_matches(teams_id_team, id_match, date_match, False, points_final_away,
                                                       dict_leagues_teams[i_dict][i][2][3], dict_leagues_teams[i_dict][i][2][5],
                                                       dict_leagues_teams[i_dict][i][2][7], dict_leagues_teams[i_dict][i][2][9],
                                                       dict_leagues_teams[i_dict][i][3], not is_win_home, home_or_away=i_send_data_t_team)

            print('Completed Finish match -----------------------------')

        except Exception:
            print(f'No se puede actualizar los partidos de la liga {i_dict}.'
                  f'\nPosiblemente esta liga no existe aún en la base de datos.')
