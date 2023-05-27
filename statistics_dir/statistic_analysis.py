import numpy as np
from conn.conn_functions_shared import select_row as fs_select_row
import pandas as pd
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats


pd.options.display.max_rows = None
pd.options.display.max_columns = None
# ==================================================================================================================== #
#                                                                                                   #
# ==================================================================================================================== #
def cal_analysis_statistic(df_get_statistics, name_team, is_home=2):
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

    # Sí al llamar la función "cal_analysis_statistic()" se solicita análisis estadístico 
    # del "name_team" indistintamente de "is_home" (todos los resultados)
    elif is_home == 2:
        str_is_home += 'Home y Away'
        
        # Dataframe temporal con las columnas necesarias para la solicitud a la llamada de la función "cal_analysis_statistic()"     
        df_temp = df_get_statistics[df_get_statistics['Name_Team'] == f'{name_team}']

    # END --------- DESIGN DATAFRAMES                                                                              # # #
    # ================================================================================================================ #

    # ================================================================================================================ #
    # ANALYSIS STATISTIC AND VISUALIZATION                                                                              #
    # ================================================================================================================ #
    # Análizar orrelaciones entre variables independientes con las variables dependientes del equipo local.
    list_columns_ind = ['Avg_Q1', 'Avg_Q2', 'Avg_Q3', 'Avg_Q1_to_Q3', 'DIFF_Q3']
    list_columns_dep = ['Avg_Q4', 'Avg_Match', 'Is_Home', 'DIFF_Q3', 'Avg_Q1_to_Q3', 'Avg_Q3', 'Avg_Q2']

    # Iterar sobre variables independientes.
    for i_ind in list_columns_ind:
        
        # Iterar sobre variables dependientes
        for j_dep in list_columns_dep:            
            # Calcular correlación con máximo 7 decimas
            corr_temp = round(df_temp[i_ind].corr(df_temp[j_dep]), 7)

            # Sí la correlación calculada es fuerte:
            if ((corr_temp >= 0.7) or (corr_temp <= -0.7)) and (i_ind != j_dep):
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
                
                # # Obtener media
                # mean_jdep = df_temp[j_dep].mean()
                # median_jdep = df_temp[j_dep].median()
                # mode_jdep = df_temp[j_dep].mode()
                # std_jdep = df_temp[j_dep].std()                

                # ==================================================================================================== #
                # PERZONALIZED DATAFRAME FOR GRAPHICS                                                                  #
                # ==================================================================================================== #
                dict_df_graphic = {f'{i_ind}': df_temp[i_ind], 
                                    f'{j_dep}': df_temp[j_dep], 
                                    'Predicted': y_pred, 
                                    'Predicted_ok?': df_temp[j_dep] >= (y_pred - 0.03),
                                    '+Area_1std': y_pred + std_error,
                                    '-Area_1std': y_pred - std_error,
                                    '+Area_2std': y_pred + 2*std_error,
                                    '-Area_2std': y_pred - 2*std_error,
                                    '+Area_3std': y_pred + 3*std_error,
                                    '-Area_3std': y_pred - 3*std_error,
                                    'Ouliers': (df_temp[j_dep]-y_pred) / std_error,
                                    'Cumulative_Prob': df_temp['Avg_Match'].cumsum() / df_temp['Avg_Match'].sum(),
                                    'Probability_Density': stats.norm.pdf(df_temp['Avg_Match'], df_temp['Avg_Match'].mean(), df_temp['Avg_Match'].std()),
                                    'DIFF_Q3': df_temp['DIFF_Q3'], 
                                    'DIFF_F': df_temp['DIFF_F'], 
                                    'Residuals': residuals,
                                    'Is_Win': df_temp['Is_Win']
                                    }
                
                df_graphic = pd.DataFrame(data=dict_df_graphic)
                              
                conditions = [(df_temp[j_dep] <= df_graphic['+Area_1std']) & (df_temp[j_dep] >= df_graphic['-Area_1std']),
                              ((df_temp[j_dep] >= df_graphic['-Area_2std']) & (df_temp[j_dep] < df_graphic['-Area_1std'])) 
                              | ((df_temp[j_dep] <= df_graphic['+Area_2std']) & (df_temp[j_dep] > df_graphic['+Area_1std'])),
                              ((df_temp[j_dep] >= df_graphic['-Area_3std']) & (df_temp[j_dep] < df_graphic['-Area_2std'])) 
                              | ((df_temp[j_dep] <= df_graphic['+Area_3std']) & (df_temp[j_dep] > df_graphic['+Area_2std'])),
                              (df_temp[j_dep] > df_graphic['+Area_3std']) | (df_temp[j_dep] < df_graphic['-Area_3std']) 
                             ]
                
                choices = [1, 2, 3, 4]
                
                df_graphic['Area'] = np.select(conditions, choices, default=0)
                
                Area_1 = len(df_graphic[df_graphic['Area'] == 1])
                Area_2 = len(df_graphic[df_graphic['Area'] == 2])
                Area_3 = len(df_graphic[df_graphic['Area'] == 3])
                Area_4 = len(df_graphic[df_graphic['Area'] == 4])
                
                print(Area_1, Area_2, Area_3, Area_4)
                
                # list_see_columns_df_graphic =  ['DIFF_F', 'DIFF_Q3', f'{i_ind}', f'{j_dep}', 'Predicted', 'Predicted_ok?', 'Ouliers', 
                #                                 'Cumulative_Prob', 'Probability_Density', 'Residuals', 'Is_Win', 'Area']
                
                list_see_columns_df_graphic =  [f'{i_ind}', f'{j_dep}', '+Area_1std', '-Area_1std', 'Area']
                
                print(f'\n\n{name_team} y {str_is_home}: {i_ind} - {j_dep}')
                # print(f'\nMean {j_dep}: {mean_jdep}\nMedina {j_dep}: {median_jdep}\nMode {j_dep}: {mode_jdep}\nSTD {j_dep}: {std_jdep}\n')
                print(df_graphic[list_see_columns_df_graphic])
                # END --------- PERZONALIZED DATAFRAME FOR GRAPHICS                                                # # #
                # ==================================================================================================== #

                # ==================================================================================================== #
                # VISUALIZATION                                                                                        #
                # ==================================================================================================== #
                # Crear figura uno que contiene la gráfica.
                fig_1, (ax, ax_2)= plt.subplots(1, 2, sharex=False, sharey=False)
                
                # Crear una figura con un nombre personalizado
                fig_1.canvas.manager.set_window_title(f'{name_team} - {str_is_home}')
                
                # Personalizar el tamaño de cada subplot
                # [x, y, width, heigth]
                ax.set_position([0.1, 0.1, 0.6, 0.8])  # Posición y tamaño del primer subplot
                ax_2.set_position([0.7, 0.1, 0.1, 0.8])  # Posición y tamaño del segundo subplot
                
                # Calcular la ecuación de la recta
                # slope, intercept, _, p_value, _ = stats.linregress(x=df_temp[i_ind], y=df_temp[j_dep])
                _, _, _, p_value, _ = stats.linregress(x=df_temp[i_ind], y=df_temp[j_dep])
                equation = f'{j_dep} = {b1:.2f}{i_ind} + {intercept:.3f}'     
                
                # Calcular el rango entre y - std y y + std
                y_j_dep = intercept + b1 * df_temp[i_ind]
                range_lower_1 = y_j_dep - std_error
                range_upper_1 = y_j_dep + std_error
                range_lower_2 = range_lower_1 - std_error
                range_upper_2 = range_upper_1 + std_error

                # Dibujar la primera área sombreada (1 sdt de distancia a la line de tendencia "y = mx + b")
                ax.fill_between(df_temp[i_ind], range_lower_1, range_upper_1, alpha=1, color='#bef202')                
                
                # num_point_1_sdt = 

                # Dibujar la segunda área sombreada (2 sdt de distancia a la line de tendencia "y = mx + b")
                ax.fill_between(df_temp[i_ind], range_lower_2, range_upper_2, alpha=0.3, color='#fea304')  

                # Dibujar la tercera área sombreada (2 sdt de distancia a la line de tendencia "y = mx + b")
                ax.fill_between(df_temp[i_ind], range_lower_2-std_error, range_upper_2+std_error, alpha=0.2, color='#b6ff00')                               
                
                # Crear gráfico  de dispersión con Seaborn
                sns.regplot(x=df_temp[i_ind], y=df_temp[j_dep], ci=None, data=df_temp[[i_ind, j_dep]],
                            scatter_kws={'color': 'blue'}, line_kws={'color': '#f5061d'}, ax=ax)
                
                # Leyenda en la parte superior de la gráfica
                msn_one_graphics = f'{equation}'

                # Leyenda en la parte inferior de la gráfica
                msn_two_graphics = f'\nCorr_Pearson: {corr_temp}\nR²: {r_squared}\nAdjusted R²: {adjusted_r_squared}\nSTD_error: {std_error}'\
                                   f'\nIntercept: {intercept}\nb1: {b1}\nt statistic: {t_statistic}\nP value: {round(p_value, 7)}'\
                                   f'\nAvg Residuals: {round(df_graphic["Residuals"].median(), 7)}'
                
                # Agregar la ecuación de la recta al gráfico
                point_x = ((max(df_temp[i_ind]) - min(df_temp[i_ind])) / 8) * 3
                lim_x = (max(df_temp[i_ind]) - min(df_temp[i_ind])) / df_temp[i_ind].count()
                lim_y = (max(df_temp[j_dep]) - min(df_temp[j_dep])) / df_temp[j_dep].count()
                max_lim_x = max(df_temp[i_ind])
                min_lim_x = min(df_temp[i_ind])
                max_lim_y = max(df_temp[j_dep]) + lim_y
                min_lim_y = min(df_temp[j_dep]) - lim_y
                
                ax_2.axis('off')
                ax.text((min_lim_x + (min_lim_x * 0.015)), (max_lim_y - (max_lim_y*0.1)), msn_one_graphics, ha='left')
                ax_2.text(0.1, 0, msn_two_graphics, ha='left')
                ax.set_xlabel(i_ind)
                ax.set_ylabel(j_dep)
                ax.set_title(f'{name_team} - {str_is_home}')
                ax.set_xlim((min(df_temp[i_ind]) - lim_x), (max(df_temp[i_ind]) + lim_x))
                ax.set_ylim((min(df_temp[j_dep]) - lim_y), (max(df_temp[j_dep]) + lim_y))
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
                
        list_columns_dep.pop(-1)
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
                            (match_statistics.avg_q1_match + match_statistics.avg_q2_match + match_statistics.avg_q3_match)/3 AS Avg_Q1_To_Q3,
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
                    ORDER BY Avg_Q1_To_Q3'''

        result_data_statistics = fs_select_row(query)
        del query

        # Nombre de las columnas en el Dataframe
        list_columns = ['Name_Team', 'Is_Home', 'Is_Win', 'Avg_Q1_to_Q3', 'Avg_Q1', 'Avg_Q2', 'Avg_Q3', 'Avg_Q4', 'Avg_Match', 'DIFF_Q3', 'DIFF_F']
        # Variables independientes:  'AVG_Q1_to_Q3', 'AVG_Q1', 'AVG_Q2', 'AVG_Q3', 'DIFF_Q3'
        # Variables dependientes: 'AVG_Q4', 'AVG_MATCH'
        
        # DataFrame.
        df_get_statistics = pd.DataFrame(data=result_data_statistics, columns=list_columns)

        # # Análisis y datos estadísticos de Home sin importar si fue local o visitante.
        # home_h_a = cal_analysis_statistic(df_get_statistics, name_home)

        # # Análisis y datos estadísticos de Home sí fue local.
        # home_h = cal_analysis_statistic(df_get_statistics, name_home, is_home=1)

        # # Análisis y datos estadísticos de Home sí fue visitante.
        # home_a = cal_analysis_statistic(df_get_statistics, name_home, is_home=0)

        # # Análisis y datos estadísticos de Away sin importar si fue local o visitante.
        # away_h_a = cal_analysis_statistic(df_get_statistics, name_away)

        # # Análisis y datos estadísticos de Away sí fue local.
        # away_h = cal_analysis_statistic(df_get_statistics, name_away, is_home=1)

        # Análisis y datos estadísticos de Away sí fue visitante.
        away_a = cal_analysis_statistic(df_get_statistics, name_away, is_home=0)

        # # Agregar las correlaciones de cada llamada a la función "cal_corr()", que son fuertes (corr > a 0.75 o corr > -0.75)
        # dict_corr_teams = {'home_h_a': home_h_a,
        #                     'home_h': home_h,
        #                     'home_a': home_a,
        #                     'away_h_a': away_h_a,
        #                     'away_h': away_h,
        #                     'away_a': away_a}

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