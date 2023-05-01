
# ==================================================================================================================== #
# VERIFICAR XPATH DEL PARTIDO                                                                                          #
# ==================================================================================================================== #
def verification_xpath_match():
    list_xpath_match = [
        '//*[@id="__next"]/main/div[1]/div[2]/div[1]/div[5]/div/div[2]/div/div/div[1]/div/div[2]/a[10]/div/div/div[1]',
        '//*[@id="__next"]/main/div[1]/div[2]/div[1]/div[5]/div/div/div[2]/div[1]/div/div[2]/a[10]/div/div/div[1]']

    return list_xpath_match
# ==================================================================================================================== #
# END --------- VERIFICAR XPATH DEL PARTIDO                                                                            #
# ==================================================================================================================== #

# ==================================================================================================================== #
# BORRAR XPATH DEL "button.previously" QUE NO PERTENECEN A LA LIGA                                                     #
# ==================================================================================================================== #
def delete_xpath_button(delete):
    list_xpath_button_previously = [
        '//*[@id="__next"]/main/div[1]/div[2]/div[1]/div[5]/div/div[2]/div/div/div[1]/div/div[1]/div[1]/button',
        '//*[@id="__next"]/main/div[1]/div[2]/div[1]/div[5]/div/div/div[2]/div[1]/div/div[1]/div[1]/button']

    del(list_xpath_button_previously[delete])

    return list_xpath_button_previously
# ==================================================================================================================== #
# END --------- BORRAR XPATH DEL "button.previously" QUE NO PERTENECEN A LA LIGA                                       #
# ==================================================================================================================== #

# ==================================================================================================================== #
# BORRAR XPATHs QUE NO PERTENECEN A LA LIGA                                                                            #
# ==================================================================================================================== #
def delete_xpath_with_match(delete, match):
    list_xpath_to_used = [
        # date
        f'//*[@id="__next"]/main/div[1]/div[2]/div[1]/div[5]/div/div[2]/div/div/div[1]/div/div[2]/a[{match}]/div/div/div[2]/span',
        f'//*[@id="__next"]/main/div[1]/div[2]/div[1]/div[5]/div/div/div[2]/div[1]/div/div[2]/a[{match}]/div/div/div[2]/span',
        # FT_match
        f'//*[@id="__next"]/main/div[1]/div[2]/div[1]/div[5]/div/div[2]/div/div/div[1]/div/div[2]/a[{match}]/div/div/div[2]/div/span[1]/span',
        f'//*[@id="__next"]/main/div[1]/div[2]/div[1]/div[5]/div/div/div[2]/div[1]/div/div[2]/a[{match}]/div/div/div[2]/div/span[1]/span',
        # Name home
        f'//*[@id="__next"]/main/div[1]/div[2]/div[1]/div[5]/div/div[2]/div/div/div[1]/div/div[2]/a[{match}]/div/div/div[4]/div/div[1]/div[1]/div',
        f'//*[@id="__next"]/main/div[1]/div[2]/div[1]/div[5]/div/div/div[2]/div[1]/div/div[2]/a[{match}]/div/div/div[4]/div/div[1]/div[1]/div',
        # Name away
        f'//*[@id="__next"]/main/div[1]/div[2]/div[1]/div[5]/div/div[2]/div/div/div[1]/div/div[2]/a[{match}]/div/div/div[4]/div/div[1]/div[2]/div',
        f'//*[@id="__next"]/main/div[1]/div[2]/div[1]/div[5]/div/div/div[2]/div[1]/div/div[2]/a[{match}]/div/div/div[4]/div/div[1]/div[2]/div',
        # list_points_home
        f'//*[@id="__next"]/main/div[1]/div[2]/div[1]/div[5]/div/div[2]/div/div/div[1]/div/div[2]/a[{match}]/div/div/div[4]/div/div[3]/div[1]',
        f'//*[@id="__next"]/main/div[1]/div[2]/div[1]/div[5]/div/div/div[2]/div[1]/div/div[2]/a[{match}]/div/div/div[4]/div/div[3]/div[1]',
        # list_points_away
        f'//*[@id="__next"]/main/div[1]/div[2]/div[1]/div[5]/div/div[2]/div/div/div[1]/div/div[2]/a[{match}]/div/div/div[4]/div/div[3]/div[2]',
        f'//*[@id="__next"]/main/div[1]/div[2]/div[1]/div[5]/div/div/div[2]/div[1]/div/div[2]/a[{match}]/div/div/div[4]/div/div[3]/div[2]',
        # list_points_final_home
        f'//*[@id="__next"]/main/div[1]/div[2]/div[1]/div[5]/div/div[2]/div/div/div[1]/div/div[2]/a[{match}]/div/div/div[4]/div/div[4]/div[1]/span[1]',
        f'//*[@id="__next"]/main/div[1]/div[2]/div[1]/div[5]/div/div/div[2]/div[1]/div/div[2]/a[{match}]/div/div/div[4]/div/div[4]/div[1]/span[1]',
        # list_points_final_away
        f'//*[@id="__next"]/main/div[1]/div[2]/div[1]/div[5]/div/div[2]/div/div/div[1]/div/div[2]/a[{match}]/div/div/div[4]/div/div[4]/div[2]/span[1]',
        f'//*[@id="__next"]/main/div[1]/div[2]/div[1]/div[5]/div/div/div[2]/div[1]/div/div[2]/a[{match}]/div/div/div[4]/div/div[4]/div[2]/span[1]'
    ]

    for i_del in range(len(list_xpath_to_used) - 1, -1, -2):
        # Borrar índices pares (delete = 0)
        if delete % 2 == 0:
            del (list_xpath_to_used[i_del - 1])

        # Borrar índices impares (delete = 1)
        else:
            del(list_xpath_to_used[i_del])

    return list_xpath_to_used
# ==================================================================================================================== #
# END --------- BORRAR XPATHs QUE NO PERTENECEN A LA LIGA                                                              #
# ==================================================================================================================== #
