from conn.conn_functions_shared import select_row as fs_select_row
import pandas as pd
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats


# ==================================================================================================================== #
#                                                                                                   #
# ==================================================================================================================== #
def cal_analysis_statistic(df_get_statistics, name_team, is_home=2):
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
        df_temp_normalized = pd.concat([df_temp['Name_Team'], df_temp_normalized], axis=1)

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
    # Sí al llamar la función "cal_analysis_statistic()" se solicita análisis estadístico 
    # del "name_team" si "is_home = 0" o "is_home = 1"
    if is_home == 0 or is_home == 1:
        if is_home == 0:
            str_is_home += 'Away'
        elif is_home == 1:
            str_is_home += 'Home'

        # Dataframe temporal con las columnas necesarias para la solicitud a la llamada de la función "cal_analysis_statistic()"     
        df_temp = df_get_statistics[(df_get_statistics['Name_Team'] == f'{name_team}') & (df_get_statistics['Is_Home'] == is_home)]

        # Obtener el DataFrame normalizado con base en "df_temp" para los equipos Home y Away.
        df_temp_normalized = get_df_temp(df_temp)

    # Sí al llamar la función "cal_analysis_statistic()" se solicita análisis estadístico 
    # del "name_team" indistintamente de "is_home" (todos los resultados)
    elif is_home == 2:
        str_is_home += 'Home y Away'
        
        # Dataframe temporal con las columnas necesarias para la solicitud a la llamada de la función "cal_analysis_statistic()"     
        df_temp = df_get_statistics[df_get_statistics['Name_Team'] == f'{name_team}']

        # Obtener el DataFrame normalizado con base en "df_temp" para los equipos Home y Away.
        df_temp_normalized = get_df_temp(df_temp)

    # END --------- DESIGN DATAFRAMES                                                                              # # #
    # ================================================================================================================ #

    # ================================================================================================================ #
    # ANALYSIS STATISTIC AND VISUALIZATION                                                                              #
    # ================================================================================================================ #
    # Análizar orrelaciones entre variables independientes con las variables dependientes del equipo local.
    list_columns_ind = ['Avg_Q1_to_Q3', 'Avg_Q1', 'Avg_Q2', 'Avg_Q3', 'DIFF_Q3', 'Is_Home']
    list_columns_dep = ['Avg_Q4', 'Avg_Match']

    # Iterar sobre variables independientes.
    for i_ind in list_columns_ind:
        # Iterar sobre variables dependientes
        for j_dep in list_columns_dep:
            # Calcular correlación con máximo 7 decimas
            corr_temp = round(df_temp[i_ind].corr(df_temp[j_dep]), 7)

            # Sí la correlación calculada es fuerte:
            if (corr_temp >= 0.75) or (corr_temp <= -0.75):
                # Agregar correlación al diccionario "dict_corr_temp{}"
                dict_corr_temp[f'Corr_pearson ({i_ind} - {j_dep})'] = corr_temp

                # Separar las variables independientes (x) y dependiente (y)
                var_x = df_temp[i_ind]
                var_y = df_temp[j_dep]

                # Agregar una constante a los datos de entrada para calcular el término de intercepción (bo)
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
                n = len(df_temp)
                p = len(results.params)
                adjusted_r_squared = round(1 - (1 - r_squared) * (n - 1) / (n - p - 1), 7)
                dict_corr_temp[f'Adjusted R^2 - ({i_ind} - {j_dep})'] = adjusted_r_squared

                # Calcular el error típico (error estándar de la estimación)
                std_error = round(results.bse[-1], 7)
                dict_corr_temp[f'STD error - ({i_ind} - {j_dep})'] = std_error

                # Obtener el coeficiente de intercepción (b0)
                intercept = round(results.params[0], 7)
                dict_corr_temp[f'b0 - ({i_ind} - {j_dep})'] = intercept

                # Obtener el coeficiente de la variable independiente
                b1 = round(results.params[1], 7)
                dict_corr_temp[f'b1 - ({i_ind} - {j_dep})'] = b1

                # Obtener el estadístico t
                t_statistic = round(results.tvalues[1], 7)
                dict_corr_temp[f't_statistic - ({i_ind} - {j_dep})'] = t_statistic

                # ==================================================================================================== #
                # PERZONALIZED DATAFRAME FOR GRAPHICS                                                                  #
                # ==================================================================================================== #
                df_graphic = pd.DataFrame({f'{i_ind}_normd': df_temp_normalized[i_ind], f'{j_dep}_normd': df_temp_normalized[j_dep],
                                           f'{i_ind}': df_temp[i_ind], f'{j_dep}': df_temp[j_dep], 
                                          'Predicted': y_pred, 'DIFF_Q3': df_temp['DIFF_Q3'], 'DIFF_F': df_temp['DIFF_F'], 'Residuals': residuals,
                                          'Is_Win': df_temp['Is_Win']})
                
                print('\n')
                print(df_graphic[[f'{i_ind}_normd', f'{j_dep}_normd']])
                print(df_graphic[[f'{i_ind}', f'{j_dep}', 'Predicted', 'DIFF_Q3', 'DIFF_F', 'Residuals', 'Is_Win']])
                # END --------- PERZONALIZED DATAFRAME FOR GRAPHICS                                                # # #
                # ==================================================================================================== #

                # ==================================================================================================== #
                # VISUALIZATION                                                                                        #
                # ==================================================================================================== #
                # Crear figura uno que contiene la gráfica.
                fig_1, ax = plt.subplots()
                
                # Crear una figura con un nombre personalizado
                fig_1.canvas.manager.set_window_title(f'{name_team} - {str_is_home}')

                # Crear gráfico  de dispersión con Seaborn, con los datos normalizados.
                sns.regplot(x=df_temp_normalized[i_ind], y=df_temp_normalized[j_dep], data=df_temp_normalized[[i_ind, j_dep]],
                            scatter_kws={'color': 'blue'}, line_kws={'color': 'red'}, ax=ax)

                # Calcular la ecuación de la recta
                slope, intercept_normalized, _, p_value, _ = stats.linregress(x=df_temp_normalized[i_ind], y=df_temp_normalized[j_dep])
                equation = f'y = {slope:.2f}x + {intercept_normalized:.2f}'

                # Leyenda en la parte superior de la gráfica
                msn_one_graphics = f'Equation: {equation}\nCorr_Pearson: {corr_temp}\nR²: {r_squared}\nAdjusted R²: {adjusted_r_squared}' \
                                   f'\nSTD_error: {std_error}'

                # Leyenda en la parte inferior de la gráfica
                msn_two_graphics = f'\nIntercept: {intercept}\nb1: {b1}\nt statistic: {t_statistic}\nP value: {round(p_value, 7)}' \
                                   f'\nAvg Residuals: {round(df_graphic["Residuals"].median(), 7)}'

                # Agregar la ecuación de la recta al gráfico
                ax.text(0.01, 0.73, msn_one_graphics, ha='left')
                ax.text(0.61, min(df_temp_normalized[j_dep]), msn_two_graphics, ha='left')
                ax.set_xlabel(i_ind)
                ax.set_ylabel(j_dep)
                ax.set_title(f'{name_team} - {str_is_home}')
                ax.set_xlim(-0.05, 1.05)
                ax.set_ylim(-0.05, 1.05)
                # Cuadrícula solo en la figura del la gráfica
                ax.grid()

                # ==================================================================================================== #
                # Función para mostrar las coordenadas al pasar el mouse sobre la gráfica                              #
                # ==================================================================================================== #
                # Variables para almacenar las anotaciones de las coordenadas
                anotaciones = []
                def mostrar_coordenadas(event):
                    if event.inaxes:
                        # Eliminar las anotaciones existentes
                        for anotacion in anotaciones:
                            anotacion.remove()
                        anotaciones.clear()
                
                        # Obtener las coordenadas del mouse
                        x_coord = event.xdata
                        y_coord = event.ydata
                
                        # Mostrar las coordenadas si están dentro de los límites del gráfico
                        if x_coord is not None and y_coord is not None:
                            texto = f'({x_coord:.2f}, {y_coord:.2f})'
                            anotacion = ax.annotate(texto, (x_coord, y_coord))
                            anotaciones.append(anotacion)
                
                        # Actualizar el gráfico
                        plt.draw()
                # END --------- Función para mostrar las coordenadas al pasar el mouse sobre la gráfica            # # #
                # ==================================================================================================== #
                
                # Registrar el evento de mover el mouse sobre la gráfica
                fig_1.canvas.mpl_connect('motion_notify_event', mostrar_coordenadas)
                
                # Mostrar el gráfico
                plt.show()
                # END --------- VISUALIZATION                                                                      # # #
                # ==================================================================================================== #
    # END --------- ANALYSIS STATISTIC AND VISUALIZATION                                                           # # #
    # ================================================================================================================ #

    # Ejemplo "dict_corr_temp = {'Corr (AVG_Q1_to_Q3 - AVG_MATCH)': 0.897098186871295, 'Corr (DIFF_Q3 - AVG_MATCH)': 0.8530396584626179}"
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
                            matches.is_win,
                            (match_statistics.avg_q1_match + match_statistics.avg_q2_match + match_statistics.avg_q3_match)/3,
                            match_statistics.avg_q1_match,
                            match_statistics.avg_q2_match,
                            match_statistics.avg_q3_match,
                            match_statistics.avg_q4_match,
                            match_statistics.avg_match,
                            matches.points_diff_q3,
                            matches.points_diff_final
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
        list_columns = ['Name_Team', 'Is_Home', 'Is_Win', 'Avg_Q1_to_Q3', 'Avg_Q1', 'Avg_Q2', 'Avg_Q3', 'Avg_Q4', 'Avg_Match', 'DIFF_Q3', 'DIFF_F']
        # Variables independientes:  'AVG_Q1_to_Q3', 'AVG_Q1', 'AVG_Q2', 'AVG_Q3', 'DIFF_Q3'
        # Variables dependientes: 'AVG_Q4', 'AVG_MATCH'
        
        # DataFrame.
        df_get_statistics = pd.DataFrame(data=result_data_statistics, columns=list_columns)

        # Análisis y datos estadísticos de Home sin importar si fue local o visitante.
        home_h_a = cal_analysis_statistic(df_get_statistics, name_home)

        # Análisis y datos estadísticos de Home sí fue local.
        home_h = cal_analysis_statistic(df_get_statistics, name_home, is_home=1)

        # Análisis y datos estadísticos de Home sí fue visitante.
        home_a = cal_analysis_statistic(df_get_statistics, name_home, is_home=0)

        # Análisis y datos estadísticos de Away sin importar si fue local o visitante.
        away_h_a = cal_analysis_statistic(df_get_statistics, name_away)

        # Análisis y datos estadísticos de Away sí fue local.
        away_h = cal_analysis_statistic(df_get_statistics, name_away, is_home=1)

        # Análisis y datos estadísticos de Away sí fue visitante.
        away_a = cal_analysis_statistic(df_get_statistics, name_away, is_home=0)

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

    except Exception as e:
        print(f'EXCEPTION IN calculate_statistics.py.show_statistics\n{e}')
# END ---------                                                                                    # # #
# ==================================================================================================================== #