
def search_css(selector):
    # selector = 0 para PREVIOUS
    # selector = 1 para NEXT
    # selector = 2 para MATCHES
    list_css = []
    if selector == 0:
        list_css.append('#__next > main > div.sc-hLBbgP.dRtNhU.sc-836c558d-0.dTLyjH > div.fresnel-container.fresnel-greaterThanOrEqual-mdMin > div > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf.sc-836c558d-1.eDNgWX > div.sc-hLBbgP.fSpQRs.sc-836c558d-2.kBACDz > div:nth-child(5) > div > div.sc-csuSiG.ikkoci > div > div > div.sc-hLBbgP.sYIUR > div > div.sc-hLBbgP.sc-eDvSVe.fcWLie.ilXvf > div:nth-child(1) > button')
        list_css.append('#__next > main > div.sc-hLBbgP.dRtNhU.sc-836c558d-0.dTLyjH > div.fresnel-container.fresnel-greaterThanOrEqual-mdMin > div > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf.sc-836c558d-1.eDNgWX > div.sc-hLBbgP.fSpQRs.sc-836c558d-2.kBACDz > div:nth-child(6) > div > div.sc-csuSiG.ikkoci > div > div > div.sc-hLBbgP.sYIUR > div > div.sc-hLBbgP.sc-eDvSVe.fcWLie.ilXvf > div:nth-child(1) > button')
        list_css.append('#__next > main > div.sc-hLBbgP.dRtNhU.sc-836c558d-0.dTLyjH > div.fresnel-container.fresnel-greaterThanOrEqual-mdMin > div > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf.sc-836c558d-1.eDNgWX > div.sc-hLBbgP.fSpQRs.sc-836c558d-2.kBACDz > div:nth-child(5) > div > div > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf > div.sc-hLBbgP.sYIUR > div > div.sc-hLBbgP.sc-eDvSVe.fcWLie.ilXvf > div:nth-child(1) > button')

    elif selector == 1:
        list_css.append('#__next > main > div.sc-hLBbgP.dRtNhU.sc-836c558d-0.dTLyjH > div.fresnel-container.fresnel-greaterThanOrEqual-mdMin > div > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf.sc-836c558d-1.eDNgWX > div.sc-hLBbgP.fSpQRs.sc-836c558d-2.kBACDz > div:nth-child(5) > div > div.sc-csuSiG.ikkoci > div > div > div.sc-hLBbgP.sYIUR > div > div.sc-hLBbgP.sc-eDvSVe.fcWLie.ilXvf > div:nth-child(2) > button')
        list_css.append('#__next > main > div.sc-hLBbgP.dRtNhU.sc-836c558d-0.dTLyjH > div.fresnel-container.fresnel-greaterThanOrEqual-mdMin > div > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf.sc-836c558d-1.eDNgWX > div.sc-hLBbgP.fSpQRs.sc-836c558d-2.kBACDz > div:nth-child(6) > div > div.sc-csuSiG.ikkoci > div > div > div.sc-hLBbgP.sYIUR > div > div.sc-hLBbgP.sc-eDvSVe.fcWLie.ilXvf > div:nth-child(2) > button')
        list_css.append('#__next > main > div.sc-hLBbgP.dRtNhU.sc-836c558d-0.dTLyjH > div.fresnel-container.fresnel-greaterThanOrEqual-mdMin > div > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf.sc-836c558d-1.eDNgWX > div.sc-hLBbgP.fSpQRs.sc-836c558d-2.kBACDz > div:nth-child(5) > div > div > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf > div.sc-hLBbgP.sYIUR > div > div.sc-hLBbgP.sc-eDvSVe.fcWLie.ilXvf > div:nth-child(2) > button')

    elif selector == 2:
        list_css.append('#__next > main > div.sc-hLBbgP.dRtNhU.sc-836c558d-0.dTLyjH > div.fresnel-container.fresnel-greaterThanOrEqual-mdMin > div > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf.sc-836c558d-1.eDNgWX > div.sc-hLBbgP.fSpQRs.sc-836c558d-2.kBACDz > div:nth-child(5) > div > div.sc-csuSiG.ikkoci > div > div > div.sc-hLBbgP.sYIUR')
        list_css.append('#__next > main > div.sc-hLBbgP.dRtNhU.sc-836c558d-0.dTLyjH > div.fresnel-container.fresnel-greaterThanOrEqual-mdMin > div > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf.sc-836c558d-1.eDNgWX > div.sc-hLBbgP.fSpQRs.sc-836c558d-2.kBACDz > div:nth-child(6) > div > div.sc-csuSiG.ikkoci > div > div > div.sc-hLBbgP.sYIUR')
        list_css.append('#__next > main > div.sc-hLBbgP.dRtNhU.sc-836c558d-0.dTLyjH > div.fresnel-container.fresnel-greaterThanOrEqual-mdMin > div > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf.sc-836c558d-1.eDNgWX > div.sc-hLBbgP.fSpQRs.sc-836c558d-2.kBACDz > div:nth-child(5) > div > div > div.sc-hLBbgP.sc-eDvSVe.gjJmZQ.fEHohf > div.sc-hLBbgP.sYIUR')

    return list_css
