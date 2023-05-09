import re
import time
import textwrap
from selenium import webdriver
from selenium.webdriver.common.by import By
from check_db_and_controllers.check_data_in_db import list_names_leagues as ck_list_name_league
from check_db_and_controllers.check_data_in_db import check_name_league as ck_name_league
from history_match.functions_shared import select_row as fs_select_row
from conn.connections import connection_db_t_errors as conn_t_errors
from history_match.prepare_and_sent_data import prepare_data as psd
from history_match.css_xpath_list import search_css as cxl


def conn_web():
    # ================================================================================================================ #
    # FUNCTION search_button()                                                                                         #
    # ================================================================================================================ #
    # Si la función "search_button()" no logra encontrar el "button.previously"
    # me regresa un String vació
    def search_button(selector_css_button):
        # Salida de emergencia al siguiente bucle para evitar que sea infinito
        flag_emergency_button = 3

        while True:
            try:
                button_previous = driver.find_element(By.CSS_SELECTOR, selector_css_button)
                break

            except Exception:
                print(
                    f'Reintentando obtener XPATH de "button.previously".\nTiempo Restante: -{flag_emergency_button} s')
                time.sleep(1)

                if flag_emergency_button <= 0:
                    button_previous = ''
                    break

                flag_emergency_button -= 1

        return button_previous

    # END --------- FUNCTION search_button()                                                                           #
    # ================================================================================================================ #

    def search_css_buttons(list_css_selected, component):
        for search_css in list_css_selected:
            try:
                if driver.find_element(By.CSS_SELECTOR, search_css).is_displayed():
                    break

            except Exception as e:
                # Si se iteró sobre el último elemento y generó exception también,
                # Se genera una exception intencional
                if search_css == list_css_selected[-1]:
                    raise Exception('X*X*X*X* INTENTIONAL EXCEPTION X*X*X*X*\n\tCSS_SELECTOR NO ESTA EN LA LISTA.')

                print(f'Buscando css correcto de {component}...\n{e}')
                pass

        return search_css

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

    # ================================================================================================================ #
    # GET ALL'S LINKS LEAGUES                                                                                          #
    # ================================================================================================================ #
    # sentencia sql para traer los links de la tabla "links_leagues"
    query = '''SELECT link_league 
               FROM links_leagues'''

    # [(link_league_1,), (link_league_2,), (link_league_3,), (link_league_4,), ..., link_league_n,]
    list_tuple_links_leagues = fs_select_row(query, database='analysis_basketball_test')
    del query
    # END --------- GET ALL'S LINKS LEAGUES                                                                        # # #
    # ================================================================================================================ #

    # ================================================================================================================ #
    # ACCESS TO EACH LEAGUE                                                                                            #
    # ================================================================================================================ #
    # Iterar sobre la lista de tuplas obtenida con los link de las ligas.
    for links_by_country in list_tuple_links_leagues[40:]:
        # links_by_country = (link_league,) :: tuple
        # links_by_country es una tupla de una sola posición

        # ============================================================================================================ #
        # NOMBRE DE LA LIGA                                                                                            #
        # ============================================================================================================ #
        # Parámetro para recargar la página para cada liga (link en la tuple "links_by_country").
        new_tab_open = links_by_country[0]
        # Ej: new_tab_open = "https://www.sofascore.com/tournament/basketball/international/euroleague/138" :: str

        # List a partir de la url de la liga.
        new_tab_open_split = new_tab_open.split('/')
        # Ej: new_tab_open = ['https', '','www.sofascore.com', 'tournament', 'basketball', 'international', 'euroleague', '138']

        # Extracción del nombre de la url (de la lista "new_tab_open_split").
        new_name_league = f"{new_tab_open_split[5]} - {new_tab_open_split[6]}"
        # Ej: new_name_league = "international - euroleague"
        print(new_name_league)
        # END --------- NOMBRE DE LA LIGA                                                                          # # #
        # ============================================================================================================ #

        try:
            # Abrir o recargar la página con la url de la liga actual "new_tab_open"
            driver.get(new_tab_open)

            # ======================================================================================================== #
            # BUSCAR CSS_SELECTOR DE LOS BOTONES                                                                       #
            # ======================================================================================================== #
            # "list_selectors_buttons_found" = [button_previous, button_next] :: str-list
            list_selectors_buttons_found = []

            for selec_which_button in range(2):
                # selector_button = search_selectors_selected(selec_which_button)
                # 0 para PREVIOUS y 1 para NEXT:
                # Obtener lista de CSS seleccionado
                # "list_css_selectors_selected" :: str-list
                list_css_selectors_selected = cxl(selec_which_button)

                # "search_css" : str -> Contiene el CSS_SELECTOR a buscar
                search_css = search_css_buttons(list_css_selectors_selected, component='button')

                # Adicionar el str del button a la lista "list_selectors_buttons_found"
                list_selectors_buttons_found.append(search_css)

                # Buscar el CSS_SELECTOR
                button = search_button(search_css)

                # Clic sobre el CSS_SELECTOR encontrado dentro de la página.
                driver.execute_script("arguments[0].click();", button)
                print(f'Click button {selec_which_button}')

            # Liberar espacio de almacenamiento para evitar fugas de memoria
            list_css_selectors_selected.clear()
            # END --------- BUSCAR CSS_SELECTOR DE LOS BOTONES                                                     # # #
            # ======================================================================================================== #

            # ======================================================================================================== #
            # ENVIAR NOMBRE DE LA LIGA A LA TABLEA "league"                                                            #
            # ======================================================================================================== #
            # Enviar nombre de liga , sí no existe, a la tabla "analysis_basketball.leagues".
            ck_name_league(new_name_league)

            # Obtener id (analysis_basketball.leagues.id_league) de la liga actual
            query = f'''SELECT id_league FROM leagues
                            WHERE name_league = "{ck_list_name_league[-1]}"'''
            current_id_league = fs_select_row(query)[0][0]
            del query
            # END --------- ENVIAR NOMBRE DE LA LIGA A LA TABLEA "league"                                          # # #
            # ======================================================================================================== #

            # ======================================================================================================== #
            # RELOAD PAGE EVERY "count_match_clicks" CLICKS                                                            #
            # ======================================================================================================== #
            # Si la liga no cuenta con partidos en el año 2023, se activa la siguiente bandera
            flag_date_old = False
            # 2da Bandera: Verificar que los 10 partidos más recientes de la liga actual sean del año 2023.
            flag_first_match = True
            # Bandera para ser usada en caso de que el historial se termine y salir del 'while "RELOAD PAGE"
            flag_end_history = False

            # Establecer parámetros de repetición
            count_initial_clicks = 0
            # Número de clics sobre "button.previous" durante la ejecución del programa
            count_match_clicks = 70

            # Bucle encargado de recargar la página cada "n" "count_match_clicks" clics en button.previous en "POST INITIAL"
            while True:
                # ==================================================================================================== #
                # CLICK ON PREVIOUS (INITIAL)                                                                          #
                # ==================================================================================================== #
                if count_initial_clicks > 0:
                    # Parámetro que inicializa el número de veces que se dará clic sobre "button.previous"
                    count_initial_clicks_temp = 0

                    while count_initial_clicks_temp < count_initial_clicks:
                        # Parámetro del botón previously
                        # list_selectors_buttons_found = [button_previous, button_next] :: str
                        # list_selectors_buttons_found[0] = string del CSS_SELECTOR de PREVIOUS
                        button_previous = search_button(list_selectors_buttons_found[0])

                        try:
                            if button_previous.is_displayed():
                                # Clic sobre el "button.previous"
                                driver.execute_script("arguments[0].click();", button_previous)

                                print(f'Button: {count_initial_clicks_temp}')

                                count_initial_clicks_temp += 1

                        except Exception:
                            # "button_previous = search_button(xpath_button_previous[0])" retorno como un String vacío
                            # "button.previously" desapareció de la página (Se termino el historiaL)
                            print(f'X*X*X*X* EXCEPTION X*X*X*X*\n\tCLICK in PREVIOUS (INITIAL).\n\tRevisar partidos de está liga.')
                            flag_end_history = True
                            break

                    if flag_end_history:
                        # Terminar la liga actual, porque tiene errores para ser leida,
                        # y continuar con la proxima liga
                        break
                # END --------- CLICK ON PREVIOUS (INITIAL)                                                        # # #
                # ==================================================================================================== #

                # ==================================================================================================== #
                # GET A LOAD DATA TO EACH "DIV 10 MATCH"                                                               #
                # ==================================================================================================== #
                # Bandera para controlar las 'n' oportunidades que se dará clic sobre "button.previous" en POST INITIAL.
                # dependiendo de "count_match_clicks"
                count_match_clicks_test = 0

                # Bucle para darle 'n' clics sobre el "button.previous" dependiendo de "count_match_clicks".
                while count_match_clicks_test < count_match_clicks:
                    try:
                        # Selector CSS de la sección "DIV 1 to 10 MACTHES"
                        # "list_css_selectors_matches" :: str-list
                        list_css_selectors_matches = cxl(2)

                        # "search_css_matches" : str -> Contiene el CSS_SELECTOR de MATCHES
                        search_css_matches = search_css_buttons(list_css_selectors_matches, component='Match')

                        # Lista a partir del string con saltos de línea obtenido con ".text".
                        # Cada salto de línea representa un nuevo elemento en la lista (splitlines())
                        section_10_matches = driver.find_element(By.CSS_SELECTOR, search_css_matches).text.splitlines()
                        print('Obteniendo datos del CSS_SELECTOR MATCHES...')

                        # Comprensión de la lista
                        # [nuevo_valor_si_condición_verdadera if condición else nuevo_valor_si_condición_falsa for valor in lista_original]
                        load_section_10_matches = [palabra.replace(' ', '-') if ' ' in palabra else palabra for palabra in section_10_matches]

                        # Pasar una lista de string´s a una única cadena de carácteres
                        # data_section_10_matches :: str
                        data_section_10_matches = ' '.join(load_section_10_matches)

                        # Crear patron de expresiones regulares para las fechas
                        # r:"raw string" Le dice a python que no omita el comportamiento de los caracteres
                        #   especiales dentro del string- Ej: '\n'
                        # \d: Se espera una expresion regular de un dígito.
                        # {2}: Se esperan dos ocurrecias del digito (\d)
                        # /: caracter normal de división de fecha (00/00/00)
                        patron = re.compile(r"\d{2}/\d{2}/\d{2}")

                        # Buscar todas las ocurrencias de la fecha en el string generado con ".join()"
                        # list_dates :: list of str
                        list_dates = patron.findall(data_section_10_matches)

                        # Dividir el texto en cada ocurrencia de la fecha
                        list_data_section_10_matches_split = re.split(patron, data_section_10_matches)

                        # Unir "list_data_section_10_matches_split"  y
                        # "list_data_section_10_matches_split" en una sola lista.
                        list_match = [list_data_section_10_matches_split[0]]
                        for i_add_list in range(len(list_dates)):
                            list_match.append(list_dates[i_add_list])
                            list_match.append(list_data_section_10_matches_split[i_add_list + 1])
                        # Ej "list_match = ['PREVIOUS A1 Box-score ', '09/04/23', ' FT AEK Olympiacos 19 16 18 25 22 16 29 18 78 85 ',
                        #                  '20/04/23',...,  '30/04/23', ' FT PAOK Promitheas 23 24 17 17 21 21 15 21 81 78']"

                        for i_splait in range(-2, ((-1) * len(list_match)), -2):
                            # i_splait toma valore pares negativos (-2, -4, -6, ... ,)
                            # Buscar si la posición es un string que hace referencia una
                            # fecha (00/00/00) con una expresión regular 'r"\d{2}/\d{2}/\d{2}"'
                            if re.search(patron, list_match[i_splait]):
                                list_match_temp = list_match[i_splait + 1].split()
                                # list_match_temp = Ej: ...
                                # ... ['FT', 'PAOK', 'Promitheas', ' 23', '24', '17', '17','OT_h', '21', '21', '15', '21', 'OT_a', '81', '78']

                                # ==================================================================================== #
                                # CHECK IF THE MATCH IS OVER AND SEND DATA TO DB's                                     #
                                # ==================================================================================== #
                                if list_match_temp[0].__contains__('FT') or list_match_temp[0].__contains__('AET'):
                                    # "date_temp" :: str.
                                    # Fecha en formato Día/Mes/Año
                                    date_temp = list_match[i_splait]
                                    # Ej : '08/04/23'

                                    # Cambiar el formato a: Año/Mes/Día para enviar este formato a MySql.
                                    date_match = f'{date_temp[6]}{date_temp[7]}/{date_temp[3:5]}/{date_temp[0]}{date_temp[1]}'
                                    # Ej : '23/04/08'
                                    # Verificar que los 10 partidos más recientes de la liga actual seán del año 2023 --
                                    # para evitar obtener información de ligas no activas ------------------------------
                                    if i_splait == -2:
                                        if (int(date_match[:2]) < 23) and flag_first_match:
                                            print(f'La liga "{new_name_league}" no cuenta con partidos en el año 2023.')
                                            flag_date_old = True
                                            flag_end_history = True
                                            break

                                        else:
                                            # Ya se está sensando el primer partido,
                                            # por lo cual: "flag_first_match" deja de usarse
                                            flag_first_match = False
                                    # ----------------------------------------------------------------------------------

                                    # Verificar si el partido tuvo overtime
                                    over_time = False
                                    # 8 posiciones de puntos por cuartos,
                                    # 2 posiciones del puntaje del Over Time
                                    # 2 positones de puntajes finales (resultado_temp[-12])

                                    if list_match_temp[12].isdigit():
                                        # No hubo overtime
                                        if len(list_match_temp) > 13:
                                            del list_match_temp[13:]

                                        # ... ['FT', 'PAOK', 'Promitheas', 23', '24', '17', '17', '21', '21', '15', '21', '81', '78']
                                        psd(current_id_league, list_match_temp, date_match, -1, -2, -3, -4,
                                                         -5, -6, -7, -8, -9, -10, -11, -12, over_time)

                                    elif list_match_temp[14].isdigit():
                                        # Si hubo overtime
                                        over_time = True
                                        if len(list_match_temp) > 15:
                                            del list_match_temp[15:]

                                        psd(current_id_league, list_match_temp, date_match, -1, -2, -4, -5,
                                                         -6, -7, -9, -10, -11, -12, -13, -14, over_time)

                                # END --------- CHECK IF THE MATCH IS OVER AND SEND DATA TO DB's                   # # #
                                # ==================================================================================== #

                        # Si el partido no cuneta con partidos en el año 2023,
                        # se cambia de liga por medio del siguiente condicional.
                        if flag_date_old:
                            break

                    except Exception as e:
                        print(f'X*X*X*X* EXCEPTION X*X*X*X*\n\tIn "count_match_clicks_test < count_match_clicks:"\n{e}')
                        pass

                    # ================================================================================================ #
                    # CARGAR NUEVA SECCIÓN CON 10 PARIDOS NUEVOS DURANTE 7 OPORTUNIDADES                               #
                    # ================================================================================================ #
                    # Cuando "count_match_clicks_test < count_match_clicks:" ya no se cumple,
                    # se cierra y vuelve a abrir el navegador.
                    # Esto se da porque la página de "www.sofascore.com" se actualiza automáticamente
                    try:
                        # Parámetro del botón previously
                        button_previous = search_button(list_selectors_buttons_found[0])

                        # Dar clic en "button.previous" por medio de un script de js
                        driver.execute_script("arguments[0].click();", button_previous)

                        count_match_clicks_test += 1

                    except Exception:
                        print(f'X*X*X*X* EXCEPTION X*X*X*X*\n\tCLICK in POST-INITIAL PREVIOUS.'
                              f'\n\tRevisar partidos de la liga {new_name_league}.')

                        flag_end_history = True

                        break
                    # END --------- CARGAR NUEVA SECCIÓN CON 10 PARIDOS NUEVOS DURANTE 7 OPORTUNIDADES             # # #
                    # ================================================================================================ #
                try:
                    # Liberar espacio de almacenamiento para evitar fugas de memoria
                    list_css_selectors_matches.clear()
                    load_section_10_matches.clear()
                    list_dates.clear()
                    list_data_section_10_matches_split.clear()
                    list_match.clear()
                    list_match_temp.clear()

                except Exception:
                    pass

                # END --------- GET A LOAD DATA TO EACH "DIV 10 MATCH"                                             # # #
                # ==================================================================================================== #

                if flag_end_history:
                    break

                count_initial_clicks += (count_match_clicks + 1)
                print('Actualizar Página')
                driver.refresh()

            print(textwrap.dedent('''Final historial de partidos de la liga actual.
                                                         Iniciar nueva DATA COLLECTION con la siguiente liga.'''))

            # END --------- RELOAD PAGE EVERY "count_match_clicks" CLICKS                                          # # #
            # ======================================================================================================== #

        except Exception as e:
            print(f'X*X*X*X* EXCEPTION X*X*X*X*\n\tEn el for que itera sobre las lista de tuplas que contiene los links de ligas\n'
                  f'CSS_SELECTOR NO ENCONTRADO. X-X-X-X-X-X-X."\n{e}')
            try:
                name_league_error = new_name_league
                conn_t_errors(name_league_error)

            except Exception as e:
                try:
                    name_league = str(len(ck_list_name_league))
                    conn_t_errors(name_league)

                except Exception:
                    print(f'X*X*X*X* EXCEPTION X*X*X*X*\n\tNO DATA FOR BD_error X+X+X+X+X+X+X+X+X+X+X+X\n{e}')
                    pass

                pass

            pass

        print('\n\nCambio de liga.')
    # ================================================================================================================ #
    # END --------- ACCESS TO EACH LEAGUE                                                                              #
    # ================================================================================================================ #

    print('Fin de las ligas.')
    # Cerrar navegador
    driver.quit()

# ==================================================================================================================== #
# CAPTAR 70 PARTIDOS Y RECARGAR PÁGINA                                                                                 #
# ==================================================================================================================== #
def catch_match():
    try:
        # Llamada de la función
        conn_web()

        print('PROGRAM SUCCESSFULLY COMPLETED without errors.')

    except Exception as e:
        print(f'X*X*X*X* EXCEPTION X*X*X*X*\n\tEND Error FATAL.\n\tFIN DEL PROGRAMA CON ERRORES\n{e}')
# ==================================================================================================================== #
# END --------- CAPTAR 70 PARTIDOS Y RECARGAR PÁGINA                                                                   #
# ==================================================================================================================== #
