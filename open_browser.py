import textwrap
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import check_db_and_controllers.check_data_in_db as ck
from conn import connections
import links
from check_db_and_controllers import css_verification
import re
import prepare_and_sent_data as psd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    # Aquí se define el tiempo máximo de espera en segundos
    wait_time = 5

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

    # Diccionario para almacenar nombre del país y sus respetivas url's de ligas
    dict_country_links = {}

    # Aquí se define el tiempo máximo de espera en segundos para el wit
    wait_time = 10
    for i_menu in range(1, 64, 1):
        try:
            # Trae el selector, de cada iteración, correspondiente a
            # el nombre del país y el div donde están los links de las ligas.
            selector_css_button_and_name_country = css_verification.selector_all_leagues(i_menu)

            name_country = driver.find_element(By.CSS_SELECTOR, selector_css_button_and_name_country[1]).text

            # Definir el elemento que quieres esperar
            is_display_menu_league = driver.find_element(By.CSS_SELECTOR, selector_css_button_and_name_country[0])
            # Abrir div de urls de ligas del country actual
            is_display_menu_league.click()

            # Esperar a que cargue el div donde se alojan los links de las ligas del actual país.
            xpath_links_leagues = '//*[@id="__next"]/main/div[1]/div[1]/div[1]/div[4]/div/div[2]/div'
            locator_links_leagues = (By.XPATH, xpath_links_leagues)
            WebDriverWait(driver, wait_time).until(EC.visibility_of_element_located(locator_links_leagues))

            # Extraer los atributos href de todas las etiquetas "<a>".
            list_links_leagues = links.search_links(driver.find_element(By.XPATH, xpath_links_leagues))

            # Almacenar los links de las ligas del actual país
            dict_country_links[name_country] = list_links_leagues

            # Cerrar div de urls de ligas del country actual
            # para no afectar la estructura de los selectores de los proximos paises.
            is_display_menu_league.click()

            print(dict_country_links)
        except Exception as e:
            print(f'{e}')
            pass

    for i_links_leagues in dict_country_links.keys():
        print(i_links_leagues, dict_country_links[i_links_leagues])

    # Eliminar la "fiba-world-cup" porque no ha iniciado aún
    # list_links_leagues.remove('https://www.sofascore.com/tournament/basketball/international/fiba-world-cup/441')
    # list_links_leagues.remove('https://www.sofascore.com/tournament/basketball/usa/nba/132')
    # list_links_leagues.remove('https://www.sofascore.com/tournament/basketball/international/euroleague/138')
    # list_links_leagues.remove('https://www.sofascore.com/tournament/basketball/greece/a1/304')
    # list_links_leagues.remove('https://www.sofascore.com/tournament/basketball/italy/serie-a/262')
    # list_links_leagues.remove('https://www.sofascore.com/tournament/basketball/spain/liga-acb/264')
    # list_links_leagues.remove('https://www.sofascore.com/tournament/basketball/international/admiralbet-aba-league/235')
    # list_links_leagues.remove('https://www.sofascore.com/tournament/basketball/brazil/nbb/1562')
    # eurocup tiene unos xpath que aún no he definido
    # list_links_leagues.remove('https://www.sofascore.com/tournament/basketball/international/eurocup/141')

    # END --------- ACCESS LINKS LEAGUES                                                                           # # #
    # ================================================================================================================ #

    # # ================================================================================================================ #
    # # FUNCTION search_button()                                                                                         #
    # # ================================================================================================================ #
    # # Si la función "search_button()" no logra encontrar el "button.previously"
    # # me regresa un String vació
    # def search_button(selector_css_button):
    #     # Salida de emergencia al siguiente bucle para evitar que sea infinito
    #     flag_emergency_button = 3
    #
    #     while True:
    #         try:
    #             button_previous = driver.find_element(By.CSS_SELECTOR, selector_css_button)
    #             break
    #
    #         except Exception:
    #             print(
    #                 f'Reintentando obtener XPATH de "button.previously".\nTiempo Restante: -{flag_emergency_button} s')
    #             time.sleep(1)
    #
    #             if flag_emergency_button <= 0:
    #                 button_previous = ''
    #                 break
    #
    #             flag_emergency_button -= 1
    #
    #     return button_previous
    #
    # # END --------- FUNCTION search_button()                                                                           #
    # # ================================================================================================================ #
    #
    # # ================================================================================================================ #
    # # ACCESS NEW LEAGUES                                                                                               #
    # # ================================================================================================================ #
    # # Parámetro para cambiar de liga
    # change_league = 0
    #
    # # Bucle para recorrer todas las ligas
    # while True:
    #     # ============================================================================================================ #
    #     # NOMBRE DE LA LIGA Y ENVIAR DATA A LA TABLE "basketball.leagues"                                              #
    #     # ============================================================================================================ #
    #     # Parámetro para recargar la página para cada liga (link en la lista "list_links_leagues").
    #     new_tab_open = list_links_leagues[change_league]
    #     # Ej: new_tab_open = "https://www.sofascore.com/tournament/basketball/international/euroleague/138" :: str
    #
    #     # List a partir de la url de la liga.
    #     new_tab_open_split = new_tab_open.split('/')
    #     # Ej: new_tab_open = ['https', '','www.sofascore.com', 'tournament', 'basketball', 'international', 'euroleague', '138']
    #
    #     # Extracción del nombre de la url (de la lista "new_tab_open_split").
    #     new_name_league = f"{new_tab_open_split[5]} - {new_tab_open_split[6]}"
    #     # Ej: new_name_league = "international - euroleague"
    #     print(new_name_league)
    #
    #     # Enviar nombre de liga a la tabla "analysis_basketball.leagues".
    #     try:
    #         ck.check_name_league(new_name_league)
    #         query = f'''SELECT id_league FROM leagues
    #                         WHERE name_league = "{ck.list_names_leagues[-1]}"'''
    #         current_id_league = connections.select_row(query)[0][0]
    #
    #         flag_brazil = 0
    #         if new_name_league.__contains__('brazil - nbb'):
    #             flag_brazil += 1
    #         # END --------- NOMBRE DE LA LIGA Y ENVIAR DATA A LA TABLE "basketball.leagues"                            # # #
    #         # ============================================================================================================ #
    #
    #         # Recargar la página
    #         driver.get(f'{new_tab_open}')
    #
    #         # controladores del "button_previous"
    #         # Clics iniciales en "button.previous" cada vez que se recarga la página inicial
    #
    #         # Selector CSS del button.previous
    #         # selector_button_previous :: str
    #         selector_button_previous = css_verification.get_selectors_css()[2 + flag_brazil]
    #         button_previous = search_button(selector_button_previous)
    #         driver.execute_script("arguments[0].click();", button_previous)
    #
    #         # Selector CSS del botón NEXT"
    #         # selector_css_next :: str
    #         selector_css_next = css_verification.get_selectors_css()[4 + flag_brazil]
    #         button_next = search_button(selector_css_next)
    #         driver.execute_script("arguments[0].click();", button_next)
    #
    #         count_initial_clicks = 0
    #         # Número de clics sobre "button.previous" durante la ejecución del programa
    #         count_match_clicks = 70
    #         # ============================================================================================================ #
    #         # RELOAD PAGES                                                                                                 #
    #         # ============================================================================================================ #
    #         # Bandera para ser usada en caso de que el historial se termine y salir del 'while "RELOAD PAGES"'
    #         flag_end_history = False
    #
    #         # Bucle encargado de recargar la página cada "count_match_clicks" clics en button.previous en "POST INITIAL"
    #         while True:
    #
    #             # ======================================================================================================== #
    #             # CLICK ON PREVIOUS (INITIAL)                                                                              #
    #             # ======================================================================================================== #
    #             if count_initial_clicks > 0:
    #                 # Salida de emergencia del while
    #                 flag_exit_emergency = 1
    #
    #                 # Parámetro que inicializa el número de veces que se dará clic sobre "button.previous"
    #                 count_initial_clicks_temp = 0
    #
    #                 while count_initial_clicks_temp < count_initial_clicks:
    #                     # Parámetro del botón previously
    #                     # tuple_path[2] = xpath_button_previous :: str
    #                     button_previous = search_button(selector_button_previous)
    #
    #                     try:
    #                         if button_previous.is_displayed():
    #                             # Clic sobre el "button.previous"
    #                             driver.execute_script("arguments[0].click();", button_previous)
    #
    #                             print(f'Button: {count_initial_clicks_temp}')
    #                             count_initial_clicks_temp += 1
    #
    #                     except Exception:
    #                         # "button_previous = search_button(xpath_button_previous[0])" retorno como un String vacío
    #                         # "button.previously" desapareció de la página (Se termino el historiaL)
    #                         print(f'EXCEPTION CLICK in PREVIOUS (INITIAL).\nRevisar partidos de está liga.')
    #                         flag_end_history = True
    #                         break
    #
    #                 if flag_end_history:
    #                     # Terminar la liga actual, porque tiene errores para ser leida,
    #                     # y continuar con la proxima liga
    #                     break
    #             # END --------- CLICK ON PREVIOUS (INITIAL)                                                            # # #
    #             # ======================================================================================================== #
    #
    #             # ======================================================================================================== #
    #             # DIV 10 MATCH                                                                                             #
    #             # ======================================================================================================== #
    #             # Bandera para controlar las 'n' oportunidades que se dará clic sobre "button.previous" en POST INITIAL.
    #             # dependiendo de "count_match_clicks"
    #             count_match_clicks_test = 0
    #
    #             # Bucle para darle 'n' clics sobre el "button.previous" dependiendo de "count_match_clicks".
    #             while count_match_clicks_test < count_match_clicks:
    #                 try:
    #                     # Selector CSS de la sección "DIV 1 to 10 MACTHES"
    #                     # selector_section_10_matches :: str
    #                     selector_section_10_matches = css_verification.get_selectors_css()[0 + flag_brazil]
    #
    #                     # Lista a partir del string con saltos de línea obtenido con ".text".
    #                     # Cada salto de línea representa un nuevo elemento en la lista (splitlines())
    #                     section_10_matches = driver.find_element(By.CSS_SELECTOR, selector_section_10_matches).text.splitlines()
    #
    #                     # Comprensión de lista
    #                     # [nuevo_valor_si_condición_verdadera if condición else nuevo_valor_si_condición_falsa for valor in lista_original]
    #                     load_section_10_matches = [palabra.replace(' ', '-') if ' ' in palabra else palabra for palabra in section_10_matches]
    #
    #                     # Pasar una lista de string´s a una única cadena de carácteres
    #                     # data_section_10_matches :: str
    #                     data_section_10_matches = ' '.join(load_section_10_matches)
    #
    #                     # Crear patron de expresiones regulares para las fechas
    #                     # r:"raw string" Le dice a python que no omita el comportamiento de los caracteres
    #                     #   especiales dentro del string- Ej: '\n'
    #                     # \d: Se espera una expresion regular de un digito.
    #                     # {2}: Se esperan dos ocurrecias del digito (\d)
    #                     # /: caracter normal de división de fecha (00/00/00)
    #                     patron = re.compile(r"\d{2}/\d{2}/\d{2}")
    #
    #                     # Buscar todas las ocurrencias de la fecha en el string generado con ".join()"
    #                     # list_dates :: list of str
    #                     list_dates = patron.findall(data_section_10_matches)
    #
    #                     # Dividir el texto en cada ocurrencia de la fecha
    #                     list_data_section_10_matches_split = re.split(patron, data_section_10_matches)
    #
    #                     # Unir "list_data_section_10_matches_split"  y
    #                     # "list_data_section_10_matches_split" en una sola lista.
    #                     list_match = [list_data_section_10_matches_split[0]]
    #                     for i_add_list in range(len(list_dates)):
    #                         list_match.append(list_dates[i_add_list])
    #                         list_match.append(list_data_section_10_matches_split[i_add_list + 1])
    #                     # Ej "list_match = ['PREVIOUS A1 Box-score ', '09/04/23', ' FT AEK Olympiacos 19 16 18 25 22 16 29 18 78 85 ',
    #                     #                  '20/04/23',...,  '30/04/23', ' FT PAOK Promitheas 23 24 17 17 21 21 15 21 81 78']"
    #
    #                     for i_splait in range(-2, (-1) * len(list_match), -2):
    #                         # i_splait toma valore pares negativos (-2, -4, -6, ... ,)
    #                         # Buscar si la posición es un string que hace referencia una
    #                         # fecha (00/00/00) con una expresión regular 'r"\d{2}/\d{2}/\d{2}"'
    #                         if re.search(patron, list_match[i_splait]):
    #                             list_match_temp = list_match[i_splait + 1].split()
    #                             # list_match_temp = Ej: ...
    #                             # ... ['FT', 'PAOK', 'Promitheas', ' 23', '24', '17', '17','OT_h', '21', '21', '15', '21', 'OT_a', '81', '78']
    #
    #                             if list_match_temp[0].__contains__('FT') or list_match_temp[0].__contains__('AET'):
    #                                 date_match = list_match[i_splait]
    #
    #                                 over_time = False
    #                                 # Verificar si el partido tuvó overtime
    #                                 # 8 posiciones de puntos por cuartos,
    #                                 # 2 posiciones del puntaje del Oer Time
    #                                 # 2 pósicones de puntajes finales (resultado_temp[-12])
    #                                 if list_match_temp[-12].isdigit():
    #                                     # Si hubo overtime
    #                                     over_time = True
    #                                     home_away_date = psd.prepare_data(current_id_league, list_match_temp, date_match,
    #                                                                       -1, -2, -4, -5, -6, -7, -9, -10, -11, -12, -13,
    #                                                                       -14, over_time)
    #
    #                                 elif list_match_temp[-10].isdigit():
    #                                     # No hubo overtime
    #                                     # ... ['FT', 'PAOK', 'Promitheas', 23', '24', '17', '17', '21', '21', '15', '21', '81', '78']
    #                                     home_away_date = psd.prepare_data(current_id_league, list_match_temp, date_match, -1,
    #                                                                       -2, -3, -4, -5, -6, -7, -8, -9, -10, -11,
    #                                                                       -12, over_time)
    #                 # ================================================================================================ #
    #                 # EXCEPTIONS CONTROL                                                                               #
    #                 # ================================================================================================ #
    #                 except Exception as e:
    #                     print(f'Exception in for match (10, 0, -1)\n{e}')
    #
    #
    #                     continue
    #                 # END --------- EXCEPTIONS CONTROL                                                             # # #
    #                 # ================================================================================================ #
    #
    #                 # END --------- RECORRER EL <div> QUE CONTIENE LOS 10 MATCHES                                      # # #
    #                 # ==================================================================================================== #
    #
    #                 # ==================================================================================================== #
    #                 # CARGAR NUEVA SECCIÓN CON 10 PARIDOS NUEVOS DURANTE 7 OPORTUNIDADES                                   #
    #                 # ==================================================================================================== #
    #                 # Cuando se usan las 'n' oportunidades, se cierra y vuelve a abrir el navegador.
    #                 # Esto se da porque la página de "www.sofascore.com" se actualiza automáticamente
    #
    #                 try:
    #                     # Parámetro del botón previously
    #                     button_previous = search_button(selector_button_previous)
    #
    #                     # Dar clic en "button.previous" por medio de un script de js
    #                     driver.execute_script("arguments[0].click();", button_previous)
    #
    #                     count_match_clicks_test += 1
    #
    #                 except Exception:
    #                     try:
    #                         # Parámetro del botón previously
    #                         button_previous = search_button(selector_button_previous)
    #
    #                         # Dar clic en "button.previous" por medio de un script de js
    #                         driver.execute_script("arguments[0].click();", button_previous)
    #
    #                         count_match_clicks_test += 1
    #
    #                     except Exception:
    #                         print(f'EXCEPTION CLICK in POST-INITIAL PREVIOUS.\nRevisar partidos de está liga.')
    #                         flag_end_history = True
    #                         break
    #                 # END --------- CARGAR NUEVA SECCIÓN CON 10 PARIDOS NUEVOS DURANTE 7 OPORTUNIDADES                 # # #
    #                 # ==================================================================================================== #
    #
    #             if flag_end_history:
    #                 break
    #
    #             count_initial_clicks += (count_match_clicks + 1)
    #             print('Actualizar Página')
    #             driver.refresh()
    #
    #         print(textwrap.dedent('''Final historial de partidos de la liga actual.
    #                                          Iniciar nueva DATA COLLECTION con la siguiente liga.'''))
    #
    #         # ============================================================================================================ #
    #         # END --------- RELOAD PAGES                                                                                   #
    #         # ============================================================================================================ #
    #
    #     except Exception as e:
    #         print(e)
    #         try:
    #             name_league = ck.list_names_leagues[-1]
    #             connections.connection_db_t_errors(name_league)
    #
    #         except Exception as e:
    #             try:
    #                 name_league = str(len(ck.list_names_leagues))
    #                 connections.connection_db_t_errors(name_league)
    #
    #             except Exception:
    #                 print(f'NO DATA FOR BD_error X+X+X+X+X+X+X+X+X+X+X+X\n{e}')
    #                 continue
    #
    #             continue
    #
    #         continue
    #
    #     print(str(len(list_links_leagues) - 1), str(change_league))
    #     # Cargar nueva liga
    #     if (len(list_links_leagues) - 1) > change_league:
    #         change_league += 1
    #         print('Cambio de liga.')
    #
    #     else:
    #         print('Fin de las ligas.')
    #         break
    #     # ================================================================================================================ #
    #     # END --------- ACCESS LEAGUES                                                                                     #
    #     # ================================================================================================================ #

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
