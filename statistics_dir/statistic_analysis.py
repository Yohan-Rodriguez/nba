from conn.conn_functions_shared import select_row as fs_select_row
import pandas as pd
import statsmodels.api as sm


# ==================================================================================================================== #
#                                                                                                   #
# ==================================================================================================================== #
def cal_corr(df_get_statistics, name_team, is_home=2):
    # Diccionario para almacenar las correlaciones fuertes una sola llamada de la función "cal_corr"
    dict_corr_temp = {}

    # Sí se solicita correlaciones del "name_team" si "is_home = 0" o "is_home = 1"
    if is_home == 0 or is_home == 1:
        df_temp = df_get_statistics[
            (df_get_statistics['NAME_TEAM'] == f'{name_team}') & (df_get_statistics['IS_HOME'] == is_home)]
        # print(df_temp)

    # Sí se solicita correlaciones del "name_team" indistintamente de "is_home" (todos los resultados)
    elif is_home == 2:
        df_temp = df_get_statistics[df_get_statistics['NAME_TEAM'] == f'{name_team}']

    # Correlaciones entre variables independientes con las variables dependientes del equipo local
    list_columns_ind = ['AVG_Q1_to_Q3', 'AVG_Q1', 'AVG_Q2', 'AVG_Q3', 'DIFF']
    list_columns_dep = ['AVG_Q4', 'AVG_MATCH']

    # Iterar sobre variables independientes.
    for i_ind in list_columns_ind:
        # Iterar sobre variables dependientes
        for j_dep in list_columns_dep:
            corr_temp = df_temp[i_ind].corr(df_temp[j_dep])

            # Sí la correlación calculada es fuerte:
            if (corr_temp >= 0.75) or (corr_temp <= -0.75):
                # Agregar correlación
                dict_corr_temp[f'Corr ({i_ind} - {j_dep})'] = corr_temp

                # print(df_temp[[i_ind, j_dep]])
                df_analysis = df_temp[[i_ind, j_dep]]

                # Separar las variables independientes (x) y dependiente (y)
                var_x = df_analysis[i_ind]
                var_y = df_analysis[j_dep]

                # Agregar una constante a los datos de entrada para calcular el término de intercepción
                var_x = sm.add_constant(var_x)

                # Ajustar el modelo de regresión lineal
                model = sm.OLS(var_y, var_x)
                results = model.fit()

                # Obtener los valores ajustados (predichos)
                # y = (coeficiente de intercepción + coeficiente de la variable independiente * variable independiente)
                y_pred = results.predict(var_x)
                dict_corr_temp[f'Predicted values - ({i_ind} - {j_dep})'] = y_pred.values

                # Obtener los residuos
                residuals = results.resid
                dict_corr_temp[f'residuals - ({i_ind} - {j_dep})'] = residuals.values

                # Calcular el coeficiente de determinación (R^2)
                r_squared = results.rsquared
                dict_corr_temp[f'R^2 - ({i_ind} - {j_dep})'] = r_squared

                # Calcular el coeficiente de determinación ajustado
                n = len(df_analysis)
                p = len(results.params)
                adjusted_r_squared = 1 - (1 - r_squared) * (n - 1) / (n - p - 1)
                dict_corr_temp[f'Adjusted R^2 - ({i_ind} - {j_dep})'] = adjusted_r_squared

                # Calcular el error típico (error estándar de la estimación)
                std_error = results.bse[-1]
                dict_corr_temp[f'STD error - ({i_ind} - {j_dep})'] = std_error

                # Obtener el coeficiente de intercepción
                intercept = results.params[0]
                dict_corr_temp[f'b0 - ({i_ind} - {j_dep})'] = intercept

                # Obtener el coeficiente de la variable independiente
                b1 = results.params[1]
                dict_corr_temp[f'b1 - ({i_ind} - {j_dep})'] = b1

                # Obtener el estadístico t
                t_statistic = results.tvalues[1]
                dict_corr_temp[f't_statistic - ({i_ind} - {j_dep})'] = t_statistic

    # Ejemplo "dict_corr_temp = {'Corr (AVG_Q1_to_Q3 - AVG_MATCH)': 0.897098186871295, 'Corr (DIFF - AVG_MATCH)': 0.8530396584626179}"
    return dict_corr_temp
# END ---------                                                                                    # # #
# ==================================================================================================================== #


# ==================================================================================================================== #
#                                                                                                     #
# ==================================================================================================================== #
def analysis_x_teams(id_league, name_home, name_away):
    try:
        # Ejemplo: tupla_names_teams = ('Union De Santa Fe', 'Ferro', 'Quimsa')
        # PUNTOS DE Q_1, Q_2 Y Q_3 DE UN PARTIDO ESPECÍFICO ----------------
        query = f'''SELECT  teams.name_team,			
                            matches.is_home,
                            (match_statistics.avg_q1_match + match_statistics.avg_q2_match + match_statistics.avg_q3_match)/3,
                            match_statistics.avg_q1_match,
                            match_statistics.avg_q2_match,
                            match_statistics.avg_q3_match,
                            match_statistics.avg_q4_match,
                            match_statistics.avg_match,
                            matches.points_difference
                    FROM match_statistics
                    JOIN matches ON match_statistics.matches_id_match = matches.id_match
                    JOIN teams_has_matches ON matches.id_match = teams_has_matches.matches_id_match
                    JOIN teams ON teams_has_matches.teams_id_team = teams.id_team
                    JOIN teams_has_leagues ON teams.id_team = teams_has_leagues.teams_id_team  
                    WHERE teams.name_team IN ("{name_home}", "{name_away}") 
                      AND teams_has_leagues.leagues_id_league = {id_league}
                    ORDER BY match_statistics.avg_match'''

        result_data_statistics = fs_select_row(query)
        del query

        # Nombre de las columnas en el Dataframe
        list_columns = ['NAME_TEAM', 'IS_HOME', 'AVG_Q1_to_Q3', 'AVG_Q1', 'AVG_Q2', 'AVG_Q3', 'AVG_Q4', 'AVG_MATCH', 'DIFF']
        # Variables independientes:  'AVG_Q1_to_Q3', 'AVG_Q1', 'AVG_Q2', 'AVG_Q3', 'DIFF'
        # Variables dependientes: 'AVG_Q4', 'AVG_MATCH'

        # DataFrame.
        df_get_statistics = pd.DataFrame(data=result_data_statistics, columns=list_columns)

        # Correlación de Home sin importar si es local o visitante.
        home_h_a = cal_corr(df_get_statistics, name_home)

        # Correlación de Home sí es local.
        home_h = cal_corr(df_get_statistics, name_home, is_home=1)

        # Correlación de Home sí es visitante.
        home_a = cal_corr(df_get_statistics, name_home, is_home=0)

        # Correlación de Away sin importar si es local o visitante.
        away_h_a = cal_corr(df_get_statistics, name_away)

        # Correlación de Away sí es local.
        away_h = cal_corr(df_get_statistics, name_away, is_home=1)

        # Correlación de Away sí es visitante.
        away_a = cal_corr(df_get_statistics, name_away, is_home=0)

        # Agregar las correlaciones de cada llamada a la función "cal_corr()", que son fuertes (corr > a 0.75 o corr > -0.75)
        dict_corr_teams = {'home_h_a': home_h_a,
                           'home_h': home_h,
                           'home_a': home_a,
                           'away_h_a': away_h_a,
                           'away_h': away_h,
                           'away_a': away_a}

        # for i in dict_corr_teams:
        #     print(i, dict_corr_teams[i])

        print(dict_corr_teams)

        # while True:
        #     msn_to_show = '\nSeleccione las columnas a mostrar:'
        #
        #     msn = show_options(list_with_options=list_columns, msn_to_show=msn_to_show, range_options=1)
        #
        #     select_options_df = int(input('\nSeleccione:\n\t1: '
        #                                   '\n\t2: ______ .\n\t3: ______.\n\t0: Salir\n\n\t-> '))
        #
        #     if select_options_df == 1:
        #         list_columns_selected = []
        #         while True:
        #             select_column = int(input(msn + '\n\n\t-> '))
        #
        #             if 0 < select_column <= len(list_columns):
        #
        #                 column_choose = list_columns[select_column-1]
        #
        #                 if column_choose not in list_columns_selected:
        #                     # Agregar el ID de la liga o nombre del equipo.
        #                     list_columns_selected.append(column_choose)
        #                     # Dividir el string cada salto de línea y crear una lista.
        #                     lineas = msn.splitlines()
        #
        #                     # Agregar información de opción seleccionada.
        #                     lineas[select_column + 1] = f'\tTHIS OPTION WAS SELECTED AS HOME ------------ {lineas[select_column + 1].replace(": ", "")[2:]}'
        #
        #                     # Unir las líneas modificadas en un nuevo string.
        #                     msn = '\n'.join(lineas)
        #
        #             # 0: SALIR.
        #             elif select_column == 0:
        #                 break
        #
        #         # Selección fuera del rango
        #         else:
        #             print('\tIngrese un número que esté dentro de la lista.\n')
        #
        #         try:
        #             # print('\n')
        #             print(df_get_statistics.loc[:, list_columns_selected])
        #
        #         except Exception as e:
        #             print(f'No se generó la lista de columnas para mostrar en el DataFrame.\n{e}')
        #
        #     elif select_options_df == 2:
        #         # Ejemplo: tuple_names_teams = ['Union De Santa Fe', 'San Lorenzo']
        #         # "tuple_names_teams" es uno de los argumentos que recibe la función "show_statistics"
        #         data_home = df_get_statistics[df_get_statistics['name_team'] == tuple_names_teams[0]]
        #         data_away = df_get_statistics[df_get_statistics['name_team'] == tuple_names_teams[1]]
        #         print(data_home[['name_team', 'avg_h', 'mdn_h', 'max_h', 'min_h']])
        #         print('\n')
        #         print(data_away[['name_team', 'avg_a', 'mdn_a', 'max_a', 'min_a']])
        #
        #     # 0: SALIR
        #     elif select_options_df == 0:
        #         break

    except Exception as e:
        print(f'EXCEPTION IN calculate_statistics.py.show_statistics\n{e}')
# END ---------                                                                                    # # #
# ==================================================================================================================== #