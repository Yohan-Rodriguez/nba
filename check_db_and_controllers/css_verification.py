from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_selectors_css_top_leagues(identifier_league):
    # identifier_league = 5 para las ligas diferentes a la eurocop
    # identifier_league = 6 la liga eurocop
    list_selectors_css = [
                          # Section 10 matches (NBA - euroliga - Grecia A1 - ) ---------------------------------
                          f'#__next > main > div.sc-hLBbgP.dRtNhU.sc-836c558d-0.dTLyjH > div.fresnel-container.fresnel-greaterThanOrEqual-mdMin > div > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf.sc-836c558d-1.eDNgWX > div.sc-hLBbgP.fSpQRs.sc-836c558d-2.kBACDz > div:nth-child({identifier_league}) > div > div.sc-csuSiG.ikkoci > div > div > div.sc-hLBbgP.sYIUR',
                          # Section 10 matches (Brazil NBB)
                          '#__next > main > div.sc-hLBbgP.dRtNhU.sc-836c558d-0.dTLyjH > div.fresnel-container.fresnel-greaterThanOrEqual-mdMin > div > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf.sc-836c558d-1.eDNgWX > div.sc-hLBbgP.fSpQRs.sc-836c558d-2.kBACDz > div:nth-child(5) > div > div > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf > div.sc-hLBbgP.sYIUR',
                          # Button previously (NBA - euroliga - Grecia A1 - ) ---------------------------------
                          f'#__next > main > div.sc-hLBbgP.dRtNhU.sc-836c558d-0.dTLyjH > div.fresnel-container.fresnel-greaterThanOrEqual-mdMin > div > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf.sc-836c558d-1.eDNgWX > div.sc-hLBbgP.fSpQRs.sc-836c558d-2.kBACDz > div:nth-child({identifier_league}) > div > div.sc-csuSiG.ikkoci > div > div > div.sc-hLBbgP.sYIUR > div > div.sc-hLBbgP.sc-eDvSVe.fcWLie.ilXvf > div:nth-child(1) > button',
                          # Button previously (Brazil NBB - )
                          '#__next > main > div.sc-hLBbgP.dRtNhU.sc-836c558d-0.dTLyjH > div.fresnel-container.fresnel-greaterThanOrEqual-mdMin > div > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf.sc-836c558d-1.eDNgWX > div.sc-hLBbgP.fSpQRs.sc-836c558d-2.kBACDz > div:nth-child(5) > div > div > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf > div.sc-hLBbgP.sYIUR > div > div.sc-hLBbgP.sc-eDvSVe.fcWLie.ilXvf > div:nth-child(1) > button',
                          # Button NEXT (NBA - euroliga - Grecia A1 - ) ---------------------------------
                          f'#__next > main > div.sc-hLBbgP.dRtNhU.sc-836c558d-0.dTLyjH > div.fresnel-container.fresnel-greaterThanOrEqual-mdMin > div > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf.sc-836c558d-1.eDNgWX > div.sc-hLBbgP.fSpQRs.sc-836c558d-2.kBACDz > div:nth-child({identifier_league}) > div > div.sc-csuSiG.ikkoci > div > div > div.sc-hLBbgP.sYIUR > div > div.sc-hLBbgP.sc-eDvSVe.fcWLie.ilXvf > div:nth-child(2) > button',
                          # Button NEXT (Brazil NBB -)
                          '#__next > main > div.sc-hLBbgP.dRtNhU.sc-836c558d-0.dTLyjH > div.fresnel-container.fresnel-greaterThanOrEqual-mdMin > div > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf.sc-836c558d-1.eDNgWX > div.sc-hLBbgP.fSpQRs.sc-836c558d-2.kBACDz > div:nth-child(5) > div > div > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf > div.sc-hLBbgP.sYIUR > div > div.sc-hLBbgP.sc-eDvSVe.fcWLie.ilXvf > div:nth-child(2) > button',
                          ]

    return list_selectors_css


def selector_all_leagues(i_selector):
    selector_button = f'#__next > main > div.sc-hLBbgP.dRtNhU.sc-836c558d-0.dTLyjH > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf.sc-836c558d-1.eDNgWX > div.sc-hLBbgP.bMQfbT.sc-836c558d-2.leSghq > div.sc-hLBbgP.dRtNhU > div > div.sc-hLBbgP.gRCqqZ > a:nth-child({i_selector}) > div > svg'
    selector_name_country = f'#__next > main > div.sc-hLBbgP.dRtNhU.sc-836c558d-0.dTLyjH > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf.sc-836c558d-1.eDNgWX > div.sc-hLBbgP.bMQfbT.sc-836c558d-2.leSghq > div.sc-hLBbgP.dRtNhU > div > div.sc-hLBbgP.gRCqqZ > a:nth-child({i_selector}) > div > div > span'

    return selector_button, selector_name_country


def wait_for_selector(str_selector, driver):
    # Aquí se define el tiempo máximo de espera en segundos
    wait_time = 10

    # Definir el elemento que quieres esperar
    locator = (By.CSS_SELECTOR, str_selector)

    return locator

