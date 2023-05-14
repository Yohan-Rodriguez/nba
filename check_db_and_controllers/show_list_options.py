
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
