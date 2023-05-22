from conn.conn_functions_shared import select_row as fs_select_row
import pandas as pd
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats


# ==================================================================================================================== #
#                                                                                                   #
# ==================================================================================================================== #
def cal_corr(df_get_statistics, name_team, is_home=2):
    # ================================================================================================================ #
    # CALCULATE DF_NORMALIZED                                                                                          #
    # ================================================================================================================ #
    def get_df_temp(df_temp):
        # Seleccionar solo las columnas numéricas
        columns_to_normalize = df_temp.columns[df_temp.dtypes != object]

        # Normalización min-max en las columnas numéricas
        df_temp_normalized = (df_temp[columns_to_normalize] - df_temp[columns_to_normalize].min()) / (
                              df_temp[columns_to_normalize].max() - df_temp[columns_to_normalize].min())

        df_temp_normalized = df_temp_normalized.round(5)

        # Concatenar la columna de nombres con el DataFrame normalizado
        df_temp_normalized = pd.concat([df_temp['NAME_TEAM'], df_temp_normalized], axis=1)

        return df_temp_normalized
    # END --------- CALCULATE DF_NORMALIZED                                                                        # # #
    # ================================================================================================================ #

    # Diccionario para almacenar las correlaciones fuertes una sola llamada de la función "cal_corr"
    dict_corr_temp = {}

    # Variable usada en los labels de las gráficas y tablas
    str_is_home = ''

    # ================================================================================================================ #
    # DESIGN DATAFRAMES                                                                                                #
    # ================================================================================================================ #
    # Sí se solicita correlaciones del "name_team" si "is_home = 0" o "is_home = 1"
    if is_home == 0 or is_home == 1:
        if is_home == 0:
            str_is_home += 'Away'
        elif is_home == 1:
            str_is_home += 'Home'

        df_temp = df_get_statistics[(df_get_statistics['NAME_TEAM'] == f'{name_team}') & (df_get_statistics['IS_HOME'] == is_home)]

        # Obtener el DataFrame normalizado con base en "df_temp" para los equipos Home y Away.
        df_temp_normalized = get_df_temp(df_temp)

    # Sí se solicita correlaciones del "name_team" indistintamente de "is_home" (todos los resultados)
    elif is_home == 2:
        str_is_home += 'Home y Away'
        df_temp = df_get_statistics[df_get_statistics['NAME_TEAM'] == f'{name_team}']

        # Obtener el DataFrame normalizado con base en "df_temp" para los equipos Home y Away.
        df_temp_normalized = get_df_temp(df_temp)

    # END --------- DESIGN DATAFRAMES                                                                              # # #
    # ================================================================================================================ #

    # ================================================================================================================ #
    # ANALYSIS STATISTIC AND VISUALIZATION                                                                              #
    # ================================================================================================================ #
    # Correlaciones entre variables independientes con las variables dependientes del equipo local
    list_columns_ind = ['AVG_Q1_to_Q3', 'AVG_Q1', 'AVG_Q2', 'AVG_Q3', 'DIFF']
    list_columns_dep = ['AVG_Q4', 'AVG_MATCH']

    # Iterar sobre variables independientes.
    for i_ind in list_columns_ind:
        # Iterar sobre variables dependientes
        for j_dep in list_columns_dep:
            corr_temp = round(df_temp[i_ind].corr(df_temp[j_dep]), 7)

            # Sí la correlación calculada es fuerte:
            if (corr_temp >= 0.75) or (corr_temp <= -0.75):
                # Agregar correlación
                dict_corr_temp[f'Corr ({i_ind} - {j_dep})'] = corr_temp

                df_analysis = df_temp[[i_ind, j_dep]]

                # Separar las variables independientes (x) y dependiente (y)
                var_x = df_analysis[i_ind]
                var_y = df_analysis[j_dep]

                # Agregar una constante a los datos de entrada para calcular el término de intercepción
                var_x = sm.add_constant(var_x)

                # Ajustar el modelo de regresión lineal
                model = sm.OLS(var_y, var_x)
                results = model.fit()

                # Obtener los valores ajustados o predichos.
                # y_pred = (coeficiente de intercepción + coeficiente de la variable independiente * variable independiente)
                y_pred = results.predict(var_x)
                dict_corr_temp[f'Predicted values - ({i_ind} - {j_dep})'] = y_pred.values

                # Obtener los residuos
                residuals = results.resid
                dict_corr_temp[f'residuals - ({i_ind} - {j_dep})'] = residuals.values

                # Calcular el coeficiente de determinación (R^2)
                r_squared = round(results.rsquared, 7)
                dict_corr_temp[f'R^2 - ({i_ind} - {j_dep})'] = r_squared

                # Calcular el coeficiente de determinación ajustado
                n = len(df_analysis)
                p = len(results.params)
                adjusted_r_squared = round(1 - (1 - r_squared) * (n - 1) / (n - p - 1), 7)
                dict_corr_temp[f'Adjusted R^2 - ({i_ind} - {j_dep})'] = adjusted_r_squared

                # Calcular el error típico (error estándar de la estimación)
                std_error = round(results.bse[-1], 7)
                dict_corr_temp[f'STD error - ({i_ind} - {j_dep})'] = std_error

                # Obtener el coeficiente de intercepción
                intercept = round(results.params[0], 7)
                dict_corr_temp[f'b0 - ({i_ind} - {j_dep})'] = intercept

                # Obtener el coeficiente de la variable independiente
                b1 = round(results.params[1], 7)
                dict_corr_temp[f'b1 - ({i_ind} - {j_dep})'] = b1

                # Obtener el estadístico t
                t_statistic = round(results.tvalues[1], 7)
                dict_corr_temp[f't_statistic - ({i_ind} - {j_dep})'] = t_statistic

                # ==================================================================================================== #
                # VISUALIZATION                                                                                        #
                # ==================================================================================================== #
                # Crear figura uno que contiene la gráfica.
                fig_1, ax = plt.subplots()

                # Crear gráfico  de dispersión con Seaborn, con los datos normalizados.
                sns.regplot(x=df_temp_normalized[i_ind], y=df_temp_normalized[j_dep], data=df_temp_normalized[[i_ind, j_dep]],
                            scatter_kws={'color': 'blue'}, line_kws={'color': 'red'}, ax=ax)

                # Calcular la ecuación de la recta
                slope, intercept_normalized, _, p_value, _ = stats.linregress(x=df_temp_normalized[i_ind], y=df_temp_normalized[j_dep])
                equation = f'y = {slope:.2f}x + {intercept_normalized:.2f}'

                # Leyenda en la parte superior de la gráfica
                msn_one_graphics = f'Equation: {equation}\nCorr_Pearson: {corr_temp}\nR²: {r_squared}\nAdjusted R²: {adjusted_r_squared}'

                # Leyenda en la parte inferior de la gráfica
                msn_two_graphics = f'\nSTD_error: {std_error}\nIntercept: {intercept}\nb1: {b1}\nt statistic: {t_statistic}' \
                                   f'\nP value: {round(p_value, 7)}'

                # Agregar la ecuación de la recta al gráfico
                ax.text(0.01, 0.8, msn_one_graphics, ha='left')
                ax.text(0.61, min(df_temp_normalized[j_dep]), msn_two_graphics, ha='left')
                ax.set_xlabel(i_ind)
                ax.set_ylabel(j_dep)
                ax.set_title(f'{name_team} - {str_is_home}')
                ax.set_xlim(-0.05, 1.05)
                ax.set_ylim(-0.05, 1.05)
                # Cuadrícula solo en la figura del la gráfica
                ax.grid()

                # ==================================================================================================== #
                # DEF CREATES TABLES                                                                                   #
                # ==================================================================================================== #
                def create_table_data(i_ind, j_dep, df_temp, ax, title_table):
                    # Crea una lista vacía para almacenar los datos de la tabla,
                    # y agrega la lista de encabezados de columna a table_data
                    table_data = [[i_ind.lower(), j_dep.lower()]]
                    table_data.extend(df_temp[[i_ind, j_dep]].values.tolist())

                    ax.axis('off')
                    table = ax.table(cellText=table_data, loc='center')
                    table.auto_set_font_size(True)

                    # Ajustar el espacio entre celdas para hacer lugar al título
                    plt.subplots_adjust(top=0.85)

                    # Agregar título al eje de las coordenadas y centrarlo
                    ax.set_title(title_table, pad=5)

                    # Ajustar el tamaño vertical de la tabla
                    num_rows = len(table_data) - 1  # Excluir la fila de encabezados
                    table_height = num_rows * 0.05  # Altura de cada fila (ajustar según sea necesario)
                    table.scale(1, table_height)

                    # Establecer negrita en la fuente de los rótulos de la tabla
                    for key, cell in table.get_celld().items():
                        if key[0] == 0:  # Filas de rótulos
                            cell.get_text().set_fontweight('bold')
                # END --------- CREATES TABLES                                                                     # # #
                # ==================================================================================================== #

                # Crear figura número dos que contiene las tablas
                fig_2, (ax2, ax3) = plt.subplots(1, 2)

                # Crear Table 1: Datos reales
                create_table_data(i_ind, j_dep, df_temp, ax2, 'REAL DATA')

                # Crear Table 2: datos normalizados
                create_table_data(i_ind, j_dep, df_temp_normalized, ax3, 'NORMALIZED DATA')

                # ==================================================================================================== #
                # Función para mostrar las coordenadas al pasar el mouse sobre la gráfica                              #
                # ==================================================================================================== #
                def mostrar_coordenadas(event):
                    if event.inaxes:
                        x_coord = event.xdata
                        y_coord = event.ydata
                        plt.annotate(f'({x_coord:.2f}, {y_coord:.2f})', (x_coord, y_coord))

                # Registrar el evento de mover el mouse sobre la gráfica
                plt.connect('motion_notify_event', mostrar_coordenadas)
                # END --------- Función para mostrar las coordenadas al pasar el mouse sobre la gráfica            # # #
                # ==================================================================================================== #

                # Mostrar el gráfico
                plt.show()
                # END --------- VISUALIZATION                                                                      # # #
                # ==================================================================================================== #
    # END --------- ANALYSIS STATISTIC AND VISUALIZATION                                                           # # #
    # ================================================================================================================ #

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

        # print(dict_corr_teams['home_h_a'])
        # print(dict_corr_teams['home_h'])
        # print(dict_corr_teams['home_a'])
        # print(dict_corr_teams['away_h_a'])
        # print(dict_corr_teams['away_h'])
        # print(dict_corr_teams['away_a'])



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