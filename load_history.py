from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import links
import textwrap
import time
from selenium.webdriver.common.by import By
import check_db_and_controllers.check_data_in_db as ck
from conn import connections
import re
import prepare_and_sent_data as psd


# ==================================================================================================================== #
# OPEN BROWSER                                                                                                         #
# ==================================================================================================================== #
def conn_web():
    options = webdriver.ChromeOptions()
    options.binary_location = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'
    driver_path = 'drivers\chromedriver.exe'
    driver_path = "..\drivers\chromedriver.exe"
    driver = webdriver.Chrome(options=options, executable_path=driver_path)
    driver.maximize_window()

    def search_css_buttons(list_css):
        for search_css in list_css:
            try:
                if driver.find_element(By.CSS_SELECTOR, search_css).is_displayed():
                    break

            except Exception as e:
                # Si se iteró sobre el último elemento y generó exception también,
                # Se genera una exception intencional
                if search_css == list_css[-1]:
                    raise Exception('CSS_SELECTOR NO ENCONTRADO. X-X-X-X-X-X-X.')

                print(f'Buscando css button correcto{e}')
                pass

        return search_css

    def search_selectors_css_b_previously():

        list_selectors_css_button_previously = [
            '#__next > main > div.sc-hLBbgP.dRtNhU.sc-836c558d-0.dTLyjH > div.fresnel-container.fresnel-greaterThanOrEqual-mdMin > div > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf.sc-836c558d-1.eDNgWX > div.sc-hLBbgP.fSpQRs.sc-836c558d-2.kBACDz > div:nth-child(5) > div > div.sc-csuSiG.ikkoci > div > div > div.sc-hLBbgP.sYIUR > div > div.sc-hLBbgP.sc-eDvSVe.fcWLie.ilXvf > div:nth-child(1) > button',
            '#__next > main > div.sc-hLBbgP.dRtNhU.sc-836c558d-0.dTLyjH > div.fresnel-container.fresnel-greaterThanOrEqual-mdMin > div > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf.sc-836c558d-1.eDNgWX > div.sc-hLBbgP.fSpQRs.sc-836c558d-2.kBACDz > div:nth-child(6) > div > div.sc-csuSiG.ikkoci > div > div > div.sc-hLBbgP.sYIUR > div > div.sc-hLBbgP.sc-eDvSVe.fcWLie.ilXvf > div:nth-child(1) > button',
            '#__next > main > div.sc-hLBbgP.dRtNhU.sc-836c558d-0.dTLyjH > div.fresnel-container.fresnel-greaterThanOrEqual-mdMin > div > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf.sc-836c558d-1.eDNgWX > div.sc-hLBbgP.fSpQRs.sc-836c558d-2.kBACDz > div:nth-child(5) > div > div > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf > div.sc-hLBbgP.sYIUR > div > div.sc-hLBbgP.sc-eDvSVe.fcWLie.ilXvf > div:nth-child(1) > button',
            ]

        search_css = search_css_buttons(list_selectors_css_button_previously)

        return search_css

    def search_selectors_css_b_next():

        list_selectors_css_button_next = [
            '#__next > main > div.sc-hLBbgP.dRtNhU.sc-836c558d-0.dTLyjH > div.fresnel-container.fresnel-greaterThanOrEqual-mdMin > div > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf.sc-836c558d-1.eDNgWX > div.sc-hLBbgP.fSpQRs.sc-836c558d-2.kBACDz > div:nth-child(5) > div > div.sc-csuSiG.ikkoci > div > div > div.sc-hLBbgP.sYIUR > div > div.sc-hLBbgP.sc-eDvSVe.fcWLie.ilXvf > div:nth-child(2) > button',
            '#__next > main > div.sc-hLBbgP.dRtNhU.sc-836c558d-0.dTLyjH > div.fresnel-container.fresnel-greaterThanOrEqual-mdMin > div > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf.sc-836c558d-1.eDNgWX > div.sc-hLBbgP.fSpQRs.sc-836c558d-2.kBACDz > div:nth-child(6) > div > div.sc-csuSiG.ikkoci > div > div > div.sc-hLBbgP.sYIUR > div > div.sc-hLBbgP.sc-eDvSVe.fcWLie.ilXvf > div:nth-child(2) > button',
            '#__next > main > div.sc-hLBbgP.dRtNhU.sc-836c558d-0.dTLyjH > div.fresnel-container.fresnel-greaterThanOrEqual-mdMin > div > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf.sc-836c558d-1.eDNgWX > div.sc-hLBbgP.fSpQRs.sc-836c558d-2.kBACDz > div:nth-child(5) > div > div > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf > div.sc-hLBbgP.sYIUR > div > div.sc-hLBbgP.sc-eDvSVe.fcWLie.ilXvf > div:nth-child(2) > button',
            ]

        search_css = search_css_buttons(list_selectors_css_button_next)

        return search_css

    def search_selectors_css_matches():

        list_selectors_css_matches = [
            '#__next > main > div.sc-hLBbgP.dRtNhU.sc-836c558d-0.dTLyjH > div.fresnel-container.fresnel-greaterThanOrEqual-mdMin > div > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf.sc-836c558d-1.eDNgWX > div.sc-hLBbgP.fSpQRs.sc-836c558d-2.kBACDz > div:nth-child(5) > div > div.sc-csuSiG.ikkoci > div > div > div.sc-hLBbgP.sYIUR',
            '#__next > main > div.sc-hLBbgP.dRtNhU.sc-836c558d-0.dTLyjH > div.fresnel-container.fresnel-greaterThanOrEqual-mdMin > div > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf.sc-836c558d-1.eDNgWX > div.sc-hLBbgP.fSpQRs.sc-836c558d-2.kBACDz > div:nth-child(6) > div > div.sc-csuSiG.ikkoci > div > div > div.sc-hLBbgP.sYIUR',
            '#__next > main > div.sc-hLBbgP.dRtNhU.sc-836c558d-0.dTLyjH > div.fresnel-container.fresnel-greaterThanOrEqual-mdMin > div > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf.sc-836c558d-1.eDNgWX > div.sc-hLBbgP.fSpQRs.sc-836c558d-2.kBACDz > div:nth-child(5) > div > div > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf > div.sc-hLBbgP.sYIUR',
            ]

        search_css = search_css_buttons(list_selectors_css_matches)

        return search_css

    # ================================================================================================================ #
    # GET ALL'S LINKS LEAGUES                                                                                          #
    # ================================================================================================================ #
    # sentencia sql para traer los links de la tabla "links_leagues"
    query = '''SELECT link_league 
               FROM links_leagues'''

    # [(link_league_1,), (link_league_2,), (link_league_3,), (link_league_4,), ..., link_league_n,]
    list_tuple_links_leagues = connections.select_row(query, database='analysis_basketball_test')
    # END --------- GET ALL'S LINKS LEAGUES                                                                        # # #
    # ================================================================================================================ #

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
    # Posicion de la url dentro de la tupla "links_by_country"
    change_league = 0

    # ================================================================================================================ #
    # ACCESS NEW LEAGUES                                                                                               #
    # ================================================================================================================ #
    for links_by_country in list_tuple_links_leagues:

        # ============================================================================================================ #
        # NOMBRE DE LA LIGA                                                                                            #
        # ============================================================================================================ #
        # Parámetro para recargar la página para cada liga (link en la lista "list_links_leagues").
        new_tab_open = links_by_country[change_league]
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
            # driver.maximize_window()
            # Recargar la página
            driver.get(new_tab_open)
            # driver.get(f'{new_tab_open}')

            # ============================================================================================================ #
            # BUSCAR CSS_SELECTOR DE LOS BOTONES                                                                     #
            # ============================================================================================================ #
            def search_css_correct_button(which_button):
                while True:
                    try:
                        if which_button == 0:
                            print('which_button = 0')
                            # Selector CSS del botón PREVIOUS"
                            # selector_button :: str
                            selector_button = search_selectors_css_b_previously()

                        elif which_button == 1:
                            print('which_button = 1')
                            # Selector CSS del botón NEXT"
                            # selector_button_previous :: str
                            selector_button = search_selectors_css_b_next()

                        button = search_button(selector_button)
                        driver.execute_script("arguments[0].click();", button)

                        break

                    except Exception:
                        raise Exception('Cargando data a la tabla "t_errors".')

                return selector_button

            # list_selectors_buttons = [button_previous, button_next] :: str
            list_selectors_buttons = []
            for selec_which_button in range(2):
                # 0 para button_previous y 1 para button_next:
                list_selectors_buttons.append(search_css_correct_button(selec_which_button))

            # Enviar nombre de liga a la tabla "analysis_basketball.leagues".
            ck.check_name_league(new_name_league)
            query = f'''SELECT id_league FROM leagues
                            WHERE name_league = "{ck.list_names_leagues[-1]}"'''
            current_id_league = connections.select_row(query)[0][0]
            # END --------- BUSCAR CSS_SELECTOR DE LOS BOTONES                                                # # #
            # ============================================================================================================ #

            count_initial_clicks = 0
            # Número de clics sobre "button.previous" durante la ejecución del programa
            count_match_clicks = 70
            # ============================================================================================================ #
            # RELOAD PAGES                                                                                                 #
            # ============================================================================================================ #
            # Bandera para ser usada en caso de que el historial se termine y salir del 'while "RELOAD PAGES"'
            flag_end_history = False

            # Bucle encargado de recargar la página cada "n" "count_match_clicks" clics en button.previous en "POST INITIAL"
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
                        # list_selectors_buttons = [button_previous, button_next] :: str
                        button_previous = search_button(list_selectors_buttons[0])

                        try:
                            if button_previous.is_displayed():
                                # Clic sobre el "button.previous"
                                driver.execute_script("arguments[0].click();", button_previous)

                                print(f'Button: {count_initial_clicks_temp}')

                                count_initial_clicks_temp += 1

                        except Exception:
                            # "button_previous = search_button(xpath_button_previous[0])" retorno como un String vacío
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
                    try:
                        # Selector CSS de la sección "DIV 1 to 10 MACTHES"
                        # selector_section_10_matches :: str
                        selector_section_10_matches = search_selectors_css_matches()

                        # Lista a partir del string con saltos de línea obtenido con ".text".
                        # Cada salto de línea representa un nuevo elemento en la lista (splitlines())
                        section_10_matches = driver.find_element(By.CSS_SELECTOR, selector_section_10_matches).text.splitlines()

                        # Comprensión de lista
                        # [nuevo_valor_si_condición_verdadera if condición else nuevo_valor_si_condición_falsa for valor in lista_original]
                        load_section_10_matches = [palabra.replace(' ', '-') if ' ' in palabra else palabra for palabra in section_10_matches]

                        # Pasar una lista de string´s a una única cadena de carácteres
                        # data_section_10_matches :: str
                        data_section_10_matches = ' '.join(load_section_10_matches)

                        # Crear patron de expresiones regulares para las fechas
                        # r:"raw string" Le dice a python que no omita el comportamiento de los caracteres
                        #   especiales dentro del string- Ej: '\n'
                        # \d: Se espera una expresion regular de un digito.
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

                        for i_splait in range(-2, (-1) * len(list_match), -2):
                            # i_splait toma valore pares negativos (-2, -4, -6, ... ,)
                            # Buscar si la posición es un string que hace referencia una
                            # fecha (00/00/00) con una expresión regular 'r"\d{2}/\d{2}/\d{2}"'
                            if re.search(patron, list_match[i_splait]):
                                list_match_temp = list_match[i_splait + 1].split()
                                # list_match_temp = Ej: ...
                                # ... ['FT', 'PAOK', 'Promitheas', ' 23', '24', '17', '17','OT_h', '21', '21', '15', '21', 'OT_a', '81', '78']

                                if list_match_temp[0].__contains__('FT') or list_match_temp[0].__contains__('AET'):
                                    date_match = list_match[i_splait]

                                    over_time = False
                                    # Verificar si el partido tuvó overtime
                                    # 8 posiciones de puntos por cuartos,
                                    # 2 posiciones del puntaje del Oer Time
                                    # 2 pósicones de puntajes finales (resultado_temp[-12])
                                    if list_match_temp[-12].isdigit():
                                        # Si hubo overtime
                                        over_time = True
                                        psd.prepare_data(current_id_league, list_match_temp, date_match,
                                                         -1, -2, -4, -5, -6, -7, -9, -10, -11, -12, -13,
                                                         -14, over_time)

                                    elif list_match_temp[-10].isdigit():
                                        # No hubo overtime
                                        # ... ['FT', 'PAOK', 'Promitheas', 23', '24', '17', '17', '21', '21', '15', '21', '81', '78']
                                        psd.prepare_data(current_id_league, list_match_temp, date_match, -1,
                                                         -2, -3, -4, -5, -6, -7, -8, -9, -10, -11,
                                                         -12, over_time)
                    # ================================================================================================ #
                    # EXCEPTIONS CONTROL                                                                               #
                    # ================================================================================================ #
                    except Exception as e:
                        print(f'Exception in for match (10, 0, -1)\n{e}')
                        pass
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
                        button_previous = search_button(list_selectors_buttons[0])

                        # Dar clic en "button.previous" por medio de un script de js
                        driver.execute_script("arguments[0].click();", button_previous)

                        count_match_clicks_test += 1

                    except Exception:
                        try:
                            # Parámetro del botón previously
                            button_previous = search_button(list_selectors_buttons[0])

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

                count_initial_clicks += (count_match_clicks + 1)
                print('Actualizar Página')
                driver.refresh()

            print(textwrap.dedent('''Final historial de partidos de la liga actual.
                                             Iniciar nueva DATA COLLECTION con la siguiente liga.'''))
            # ============================================================================================================ #
            # END --------- RELOAD PAGES                                                                                   #
            # ============================================================================================================ #

        except Exception as e:
            print(e)
            try:
                name_league = ck.list_names_leagues[-1]
                connections.connection_db_t_errors(name_league)

            except Exception as e:
                try:
                    name_league = str(len(ck.list_names_leagues))
                    connections.connection_db_t_errors(name_league)

                except Exception:
                    print(f'NO DATA FOR BD_error X+X+X+X+X+X+X+X+X+X+X+X\n{e}')
                    pass

                pass

            pass

        print('Cambio de liga.')

    print('Fin de las ligas.')
    # Cerrar navegador
    driver.quit()
    # ================================================================================================================ #
    # END --------- NEW ACCESS LEAGUES                                                                                 #
    # ================================================================================================================ #

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
