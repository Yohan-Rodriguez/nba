
def selector_all_leagues(i_selector, temp_xpath_links):
    # selector_name_country = f'#__next > main > div.sc-hLBbgP.dRtNhU.sc-836c558d-0.dTLyjH > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf.sc-836c558d-1.eDNgWX > div.sc-hLBbgP.bMQfbT.sc-836c558d-2.leSghq > div.sc-hLBbgP.dRtNhU > div > div.sc-hLBbgP.gRCqqZ > a:nth-child({i_selector}) > div > div > span'

    selector_button = f'#__next > main > div.sc-hLBbgP.dRtNhU.sc-836c558d-0.dTLyjH > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf.sc-836c558d-1.eDNgWX > div.sc-hLBbgP.bMQfbT.sc-836c558d-2.leSghq > div.sc-hLBbgP.dRtNhU > div > div.sc-hLBbgP.gRCqqZ > a:nth-child({i_selector}) > div > svg'

    if i_selector != 1:
        xpath_div_links = f'//*[@id="__next"]/main/div[1]/div[1]/div[1]/div[4]/div/div[2]/div[{temp_xpath_links}]'

    else:
        xpath_div_links = '//*[@id="__next"]/main/div[1]/div[1]/div[1]/div[4]/div/div[2]/div'

    return selector_button, xpath_div_links
