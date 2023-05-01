from selenium.webdriver.common.by import By


# ==================================================================================================================== #
# Extraer los atributos href de todas las etiquetas "<a>"                                                              #                                                  #
# ==================================================================================================================== #
def search_links(xpath_test):
    # Lista donde se guardarán los links de cada liga:
    list_links = []
    
    # XPATH con los links:
    links = xpath_test.find_elements(By.XPATH, ".//a")
    
    for i_link in links:
        # Adición de cada link a la lista "list_links_leagues"
        list_links.append(i_link.get_attribute("href"))
        
    return list_links
# END --------- Extraer los atributos href de todas las etiquetas "<a>"                                            # # #
# ==================================================================================================================== #
