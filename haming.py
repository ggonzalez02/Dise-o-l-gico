import matplotlib.pyplot as plt
import pandas as pd
from tabulate import tabulate  

#función para verificar si el input de usuario es un número hexadecimal 
def validar_hexadecimal(hex_str):
    try:
        if 0 <= int(hex_str, 16) <= 0xFFF: # si el valor que viene de hex_str está entre el rango return true 
            return True  
    except ValueError:  # de otra forma devuelva false y tire mensaje de error 
        pass  
    return False  

# Función que convierte un string hexadecimal a decimal, binario y octal
def convertir_numeros(hex_str):
    decimal = int(hex_str, 16)
    binario = bin(decimal)[2:].zfill(12)
    octal = oct(decimal)[2:]
    return decimal, binario, octal # retorna los valores resultantes 

# Función para implementar la señal NZRI en bipolar 
def generar_nrzi_bipolar(bits):
    tiempo = [0] # Va a akmacenar cambios en el tiempo 
    señal = [1] # Va a almacenar los valores de voltaje de la señal 
    nivel_actual = 1 # Se usa para tener un conteo del nivel de voltaje actual 
# for para poder recorrer cad bit de la cadena 
    for i, bit in enumerate(bits):
        tiempo.append(i) # Se guarda el instante de tiempo actual en tiempo 
        señal.append(nivel_actual) # se guarda el nivel de voltaje actual 

        if bit == '1': # Cambia de nivel solo cuando el bit es 1 
            nivel_actual *= -1  # invierte el valor de nivel actual 

        tiempo.append(i) # va a guardar el nuevo nivel 
        señal.append(nivel_actual) # guarda nuevo voltaje 
    
    tiempo.append(len(bits))
    señal.append(nivel_actual)

    return tiempo, señal

# Grafica la señal NRZI bipolarmente , recive el valor en binario
def graficar_nrzi(binario):
    
    tiempo, señal = generar_nrzi_bipolar(binario) #carga valores de tiempo y voltaje 

    plt.figure(figsize=(10, 3)) #Crea la pantalla 
    plt.step(tiempo, señal, where='post', linewidth=2, color='b') # características de la linea a graficar 
    plt.ylim(-1.5, 1.5) # limites verticales 
    plt.yticks([-1, 0, 1], ["-V", "0", "+V"]) #Etiquetas 
    plt.xticks(range(0, len(binario) + 1)) # limites del eje x
    plt.xlabel("Tiempo") # eje x etiqueta
    plt.ylabel("Amplitud") # eje y etiqueta 
    plt.title("Codificación NRZI Bipolar") # titulo de la grafica 
    plt.grid(True)
    # Cierran la grafica 
    print("Presiona ENTER en la terminal para continuar...")
    plt.show(block=False)
    input()
    plt.close()

#solicita al usuario que elija paridad par o impar 
def solicitar_paridad():
    while True:
        paridad = input("Seleccione el tipo de paridad (par/impar): ").lower()
        
        if paridad in ['par', 'impar']:
            return paridad
        else:
            print("Opción no válida. Por favor ingrese 'par' o 'impar'.")

# Implementación para la codificación de Hamming 
def codificar_hamming(binario, tipo_paridad):

    bits_datos = [int(bit) for bit in binario] # pasa la el string de binarios a una lista de enteros 
    hamming = [0] * 17 # se inicializa una lista con 17 ceros 
    j = 0 
    
    # Insertar bits de datos
    for i in range(17): 
        if (i + 1) not in [1, 2, 4, 8, 16]: # se colocan los bits de datos en posiciones no reservados d1 d2....
            if j < len(bits_datos): # bits de paridad en p1 , p2 ....
                hamming[i] = bits_datos[j]
                j += 1
    
    # Calcular bits de paridad por medio de su posciones, -1 porque empieza en 0 
    for pos in [1, 2, 4, 8, 16]:
        idx = pos - 1
        
        # Contar unos en los bits verificados (excluyendo el bit de paridad)
        count_ones = sum(
            hamming[i] 
            for i in range(17) 
            if i != idx and (i + 1) & pos # verifica de donde proviene el uno y si es del grupo que cubre el bit de paridad 
        )
        
        # Establecer bit de paridad según el tipo
        if tipo_paridad == 'par':
            # Para paridad par, queremos un número total par de unos
            hamming[idx] = 1 if count_ones % 2 == 0 else 0
        else:  # impar
            # Para paridad impar, queremos un número total impar de unos
            hamming[idx] = 0 if count_ones % 2 == 0 else 1
    
    return ''.join(map(str, hamming)) # devuelve el resultado en una cadena para poder ser printeado 


def mostrar_tabla_hamming(binario, hamming, tipo_paridad):

    # Convertir a listas de enteros
    bits_hamming = [int(bit) for bit in hamming] 
    
    # lista de encabezados para la tabla 
    headers = ["", "p1", "p2", "d1", "p3", "d2", "d3", "d4", "p4", "d5", "d6", "d7", "d8", "d9", "d10", "d11", "p5", "d12"]
    
    # Crear mapa de bits de datos
    data_bits = {}
    j = 0
    for i in range(17):
        if (i + 1) not in [1, 2, 4, 8, 16]:  # No es posición de bit de paridad
            data_bits[i] = j
            j += 1
    
    # lista para meter los datos para la tabla
    rows = [] 
    
    # Palabra sin pariedad en la tabla 
    sin_paridad = ["Palabra de datos (sin paridad):"]
    for i in range(17):
        if i in data_bits and data_bits[i] < len(binario):
            sin_paridad.append(binario[data_bits[i]])
        else:
            sin_paridad.append("")
    rows.append(sin_paridad)
    
    # Bits de paridad se colca su valor en la tabla y el bit que afecta 
    for p_pos, p_nombre in [(0, "p1:"), (1, "p2:"), (3, "p3:"), (7, "p4:"), (15, "p5:")]:
        p_valor = p_pos + 1
        row = [p_nombre]
        
        for i in range(17):
            if i == p_pos:  # Es el propio bit de paridad
                row.append(str(bits_hamming[i]))
            elif (i + 1) & p_valor:  # Es un bit verificado por este bit de paridad
                row.append(str(bits_hamming[i]))
            else:
                row.append("")
        
        rows.append(row)
    
    # Palabra con paridad para la tabla 
    con_paridad = ["Palabra de datos (con paridad):"]
    for i in range(17):
        con_paridad.append(str(bits_hamming[i]))
    rows.append(con_paridad)
    
    # Mostrar tabla usando tabulate para que se puedan alinear bien 
    print("\ntabla No 1 Cálculo de los bits de paridad en el código Hamming")
    print(tabulate(rows, headers=headers, tablefmt="plain"))


# Implementación de detección de errores 
def detectar_error(hamming_con_error, tipo_paridad):

    bits = [int(bit) for bit in hamming_con_error]
    x = 0 # almacena el bit erróneo en del código 
    
    # Va a iterar sobre los bits de paridad por lo cuál se especifica la posición 
    for p_valor in [1, 2, 4, 8, 16]:
        
        
        # Contar unos en los bits cubiertos por este bit de paridad
        bits_cubiertos = [i for i in range(len(bits)) if (i + 1) & p_valor]
        unos = sum(bits[i] for i in bits_cubiertos)
        
        # Comprobar si la paridad es correcta (suma debe de ser par)
        if tipo_paridad == 'par':
            paridad_correcta = unos % 2 == 0
        else:  # impar (suma debe de ser impar )
            paridad_correcta = unos % 2 == 1
        
        # Si hay error en este bit de paridad, sumarlo a la posición del error indicando su posición 
        if not paridad_correcta:
            x += p_valor
    # se mapea 31 espacios depués por lo que se tuvo que restarle 31 a la posición para que se detecte bien el lugar donde se hace el error 
    if x > 0:
        return 31 - x
    else:
        return 0

# Implementación para mostrar la tabla 2 de verificación de errores 
def mostrar_tabla_verificacion(hamming_con_error, error_pos, tipo_paridad):
    # Similar a la tabla 1 pero con columnas para el resultado de correcto o error 
    bits = [int(bit) for bit in hamming_con_error]
    
    # Crear lista de encabezados
    headers = ["", "p1", "p2", "d1", "p3", "d2", "d3", "d4", "p4", "d5", "d6", "d7", "d8", "d9", "d10", "d11", "p5", "d12", "Prueba de paridad", "Bit de paridad"]
    
    # Preparar filas para la tabla
    rows = []
    
    # Palabra recibida
    recibida = ["Palabra de datos recibida:"]
    for bit in bits:
        recibida.append(str(bit))
    recibida.extend(["", ""])  # Columnas para "Prueba de paridad" y "Bit de paridad"
    rows.append(recibida)
    
    # Verificación de bits de paridad
    resultados = []
    for p_pos, p_nombre in [(0, "p1:"), (1, "p2:"), (3, "p3:"), (7, "p4:"), (15, "p5:")]:
        p_valor = p_pos + 1
        
        # Bits cubiertos por este bit de paridad
        bits_cubiertos = [i for i in range(len(bits)) if (i + 1) & p_valor]
        unos = sum(bits[i] for i in bits_cubiertos)
        
        # Verificar si la paridad es correcta
        if tipo_paridad == 'par':
            paridad_correcta = unos % 2 == 0
        else:  # impar
            paridad_correcta = unos % 2 == 1
        
        # Crear fila
        row = [p_nombre]
        for i in range(17):
            if i in bits_cubiertos:
                row.append(str(bits[i]))
            else:
                row.append("")
        
        # Añadir resultado
        resultado = "Correcto" if paridad_correcta else "Error"
        bit_resultado = "0" if paridad_correcta else "1"
        row.append(resultado)
        row.append(bit_resultado)
        
        rows.append(row)
        resultados.append((resultado, bit_resultado))
    
    # Mostrar tabla usando tabulate
    print("\nTabla No.2 Comprobación de los bits de paridad (con un bit cambiado)")
    print(tabulate(rows, headers=headers, tablefmt="plain"))
    
    # Resultado
    if error_pos > 0:
        print(f"\nSe detectó un error en la posición: {error_pos}")
    
    # Corrección si hay un error lo corrige invirtiendo el bit 
    if 1 <= error_pos <= len(hamming_con_error):
        hamming_corregido = list(hamming_con_error)
        hamming_corregido[error_pos-1] = '1' if hamming_corregido[error_pos-1] == '0' else '0'
        hamming_corregido = ''.join(hamming_corregido)
        print(f"Palabra corregida: {hamming_corregido}")
        print("\n Se detectó correctamente la posición del error.")
            
# Implementación para que el usuario pueda corregir el bit deseado para poder crear un error 
def modificar_bit(hamming):

    print("\nMODIFICAR UN BIT PARA SIMULAR UN ERROR")
    # pregunta al usuario por la posición y se asegura de que sea una una posición correcta, por eso try 
    while True:
        try:
            posicion = int(input(f"Ingrese la posición del bit a modificar (1-{len(hamming)}): "))
            if 1 <= posicion <= len(hamming):
                break
            else:
                print(f"Error: Ingrese un número entre 1 y {len(hamming)}.")
        except ValueError:
            print("Error: Ingrese un número válido.")
    
    # Ajustar para índice  ya que empieza desde 0 
    posicion_indice = posicion - 1
    
    # Modificar el bit (invertirlo) para que muestre cuál bit se cambió y el bit original. no tiene nada que ver con la tabla 
    hamming_lista = list(hamming)
    hamming_lista[posicion_indice] = '1' if hamming_lista[posicion_indice] == '0' else '0'
    # display del binario original y el cambiado con error
    hamming_con_error = ''.join(hamming_lista)
    print(f"Bit en posición {posicion} modificado: {hamming} → {hamming_con_error}")
    
    return hamming_con_error, posicion


# --- Bucle principal del programa  para que se pueda seguir ejecutando el programa ---
#Menú para el programa, salir termina el programa y hace llamado a las funciones anteriores con sus respectivo valores que les entra 
while True:
    hex_input = input("\nIngrese un número hexadecimal (000 a FFF) o 'salir' para terminar: ").upper() # upper para que si se mete a sea A 
    
    if hex_input == "SALIR":  
        print("Programa terminado.")
        break  

    if validar_hexadecimal(hex_input):  
        decimal, binario, octal = convertir_numeros(hex_input)  
        
        print("\nTabla de Conversiones:")
        print(f"{'Hexadecimal':<12}{'Decimal':<12}{'Binario':<16}{'Octal':<8}")
        print(f"{hex_input:<12}{decimal:<12}{binario:<16}{octal:<8}")
        
        graficar_nrzi(binario)  

        tipo_paridad = solicitar_paridad()

        hamming_codificado = codificar_hamming(binario, tipo_paridad)
        mostrar_tabla_hamming(binario, hamming_codificado, tipo_paridad)

        # Detección y corrección de errores
        respuesta = input("\n¿Desea simular un error modificando un bit? (s/n): ").lower()
        if respuesta == 's':
            # Modificar un bit y obtener la nueva cadena con error
            hamming_con_error, pos_modificada = modificar_bit(hamming_codificado)
            
            # Detectar la posición del error
            pos_error = detectar_error(hamming_con_error, tipo_paridad)
            
            # Mostrar la tabla de verificación
            mostrar_tabla_verificacion(hamming_con_error, pos_error, tipo_paridad)

    else:
        print("Error: Ingrese un número válido entre 000 y FFF o escriba 'salir'.")