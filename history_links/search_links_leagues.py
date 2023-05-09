from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from check_db_and_controllers.css_verification import selector_all_leagues as sel_all_leagues
from conn.connections import insert_row as conn_insert_row
import history_links.links as links


def search_link():
    website = 'https://www.sofascore.com/basketball'
    options = webdriver.ChromeOptions()
    options.binary_location = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'
    driver_path = '../drivers/chromedriver.exe'
    driver_path = "..\drivers\chromedriver.exe"
    driver = webdriver.Chrome(options=options, executable_path=driver_path)
    driver.maximize_window(website)

    # ================================================================================================================ #
    # ACCESS LINKS LEAGUES                                                                                             #
    # ================================================================================================================ #
    # Diccionario para almacenar nombre del país y sus respetivas url's de ligas
    dict_country_links = {}

    # Aquí se define el tiempo máximo de espera en segundos para el wit
    wait_time = 5

    # Contador para localizar el xpath de los links de cada país
    temp_xpath_links = 1
    for i_menu in range(1, 127, 2):
        try:
            # Obtener los selectores css y el xpath a usar por cada país
            selector_css_button_and_name_country = sel_all_leagues(i_menu, temp_xpath_links)

            # # Trae el selector, de cada iteración, correspondiente a
            # # el nombre del país y el div donde están los links de las ligas.
            # name_country = driver.find_element(By.CSS_SELECTOR, selector_css_button_and_name_country[0]).text

            # Botón de despliegue del menú de ligas
            is_display_menu_league = driver.find_element(By.CSS_SELECTOR, selector_css_button_and_name_country[0])

            # Abrir div de urls de ligas del country actual
            # driver.execute_script("arguments[0].click();", is_display_menu_league)
            is_display_menu_league.click()

            # Definir el elemento que quieres esperar
            xpath_ligueas_current = selector_css_button_and_name_country[1]
            locator_links_leagues = (By.XPATH, xpath_ligueas_current)
            # Esperar hasta que el elemento sea visible
            WebDriverWait(driver, wait_time).until(EC.visibility_of_element_located(locator_links_leagues))
            xpath_links_found = driver.find_element(By.XPATH, xpath_ligueas_current)

            # Extraer los atributos href de todas las etiquetas "<a>".
            list_links_leagues_country = links(xpath_links_found)
            temp_xpath_links += 1

            for send_link in list_links_leagues_country[:-1]:
                query = (f"INSERT INTO links_leagues (link_league) VALUE ('{send_link}')")
                print('Sending data to "analysis_basketball.links_leagues".')
                conn_insert_row(query)
                print('Executed TABLE "LINKS_LEAGUES".')

        except Exception as e:
            print(f'{e}')
            pass

    print('Data load completed successfully in "analysis_basketball.links_leagues".')

    driver.quit()
