from conn.conn_functions_shared import select_row as fs_select_row


# ==================================================================================================================== #
#                                                                                                            #
# ==================================================================================================================== #
def show_options(list_with_options, msn_to_show='\nSeleccionar:'):
    # Iterar sobre la lista de tuplas de ligas, con su id cada una,
    # para generar el primer mensaje completo.
    for i in range(len(list_with_options)):
        # Concatenar el mensaje.
        msn_to_show += f'\n\t{i + 1}: {list_with_options[i][0].upper()}'

        # Adicionar la opción de salida en último lugar.
        if i == len(list_with_options)-1:
            msn_to_show += f'\n\t{0}: SALIR'

    return msn_to_show
# END ---------                                                                   # # #
# ==================================================================================================================== #


# ==================================================================================================================== #
# SEARCH AND GET ALL LEAGUES IN DB.                                                                                    #
# ==================================================================================================================== #
def search_data_in_table(query, msn_to_show):
    # list_temp_db :: lista de tuplas,
    # cada tupla con dos posiciones (name_league, id_league)

    # list_temp_db :: lista de tuplas
    list_temp_db = fs_select_row(query)
    # Ejemplo para el resultado al solicitar las ligas:
    # list_temp_db = [('argentina - lnb', 6093), ('austria - superliga', 4502), ('espana - liga-endesa', 3504)]
    del query

    # Llamar la función "show_options()"
    msn_to_show = msn_to_show
    msn_to_show_options = show_options(list_with_options=list_temp_db, msn_to_show=msn_to_show)

    return msn_to_show_options, list_temp_db
# END --------- SEARCH AND GET ALL LEAGUES IN DB.                                                                  # # #
# ==================================================================================================================== #


# ==================================================================================================================== #
#                                                                                    #
# ==================================================================================================================== #
def see_options(repeat_num, tuple_get=None):
    # Lista para guardar la información solicitada por el usuario.
    # Esta lista se borra al final de la función.
    list_data = []

    position = None

    # repeat_num == 1 es para obtener ID de la ligas
    if repeat_num == 1:
        # ============================================================================================================ #
        # SEARCH AND GET ALL LEAGUES IN DB.                                                                            #
        # ============================================================================================================ #
        query = '''SELECT name_league, id_league
                   FROM leagues
                   ORDER BY name_league ASC'''
        
        # Llamar la función "show_options()"
        msn_to_show = '\nSeleccione la liga del (los) equipo()s para ver sus estadísticas:'
        result_tuple = search_data_in_table(query, msn_to_show)
        position = 1
        # END --------- SEARCH AND GET ALL LEAGUES IN DB.                                                          # # #
        # ============================================================================================================ #

    # repeat_num == 2 es para obtener el nombre de los equipos de las ligas seleccionadas
    elif repeat_num == 2:
        # ============================================================================================================ #
        # SEARCH AND GET ALL LEAGUES IN DB.                                                                            #
        # ============================================================================================================ #
        if len(tuple_get) > 1:
            query = f'''SELECT name_team
                        FROM teams
                        JOIN teams_has_leagues ON teams.id_team = teams_has_leagues.teams_id_team
                        WHERE teams_has_leagues.leagues_id_league IN {tuple_get}
                        ORDER BY teams_has_leagues.leagues_id_league, name_team'''

        else:
            query = f'''SELECT name_team
                        FROM teams
                        JOIN teams_has_leagues ON teams.id_team = teams_has_leagues.teams_id_team
                        WHERE teams_has_leagues.leagues_id_league = {tuple_get[0]}
                        ORDER BY name_team'''

        msn_to_show = '\nSeleccione el o los equipos para ver sus estadísticas. Están ordenados alfabéticamente:'

        # result_tuple :: tupla
        result_tuple = search_data_in_table(query, msn_to_show)
        # result_tuple = (msn_to_show_options, list_temp_db)

        position = 0
        # END --------- SEARCH AND GET ALL LEAGUES IN DB.                                                          # # #
        # ============================================================================================================ #

    # ================================================================================================================ #
    # SHOW ALL OPTIONS TO CHOOSE.                                                                                      #
    # ================================================================================================================ #
    # El mensaje a mostrar es la posición 0,
    msn = result_tuple[0]

    while True:
        try:
            # Mostrar el primer mensaje
            select_league = int(input(msn + '\n\n\t-> '))

            if 0 < select_league <= len(result_tuple[1]):
                # Obtener el ID de la liga seleccionada o el nombre del equipo, dependiendo el caso, por medio de la
                # posición de la lista que contiene el ID de la liga dada o el nombre del equipo.
                # data_returned = _ _ _ _ :: int (ID)
                data_returned = result_tuple[1][select_league - 1][position]
                # para el caso de las ligas: result_tuple = (msn_to_show_options, list_temp_db) y
                # list_temp_db = [('argentina - lnb', 6093), ('austria - superliga', 4502), ('espana - liga-endesa', 3504)]

                # No repetir IDs o nombres al momento de agregarlos a la lista "list_data":
                if data_returned not in list_data:
                    # Agregar el ID de la liga o nombre del equipo.
                    list_data.append(data_returned)
                    # Dividir el string cada salto de línea y crear una lista.
                    lineas = msn.splitlines()

                    # Agregar información de opción seleccionada.
                    lineas[select_league + 1] = f'\tTHIS OPTION WAS SELECTED ------------------ {lineas[select_league + 1].replace(": ", "")[2:]}'

                    # Unir las líneas modificadas en un nuevo string.
                    msn = '\n'.join(lineas)

            # 0: SALIR
            elif select_league == 0:
                break

            # Selección fuera del rango
            else:
                print('\tIngrese un número que esté dentro de la lista.\n')

        # Usuario no digita un número.
        except Exception as e:
            print('\tEl character ingresado no es un número.\n')

    tuple_data = tuple(list_data)
    list_data.clear()
    
    return tuple_data
# END --------- SHOW ALL OPTIONS TO CHOOSE.                                                                    # # #
# ================================================================================================================ #
