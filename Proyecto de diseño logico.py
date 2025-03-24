
import matplotlib.pyplot as plt
import pandas as pd


def validar_hexadecimal(hex_str):
    """Verifica si el número ingresado está en el rango 000 a FFF"""
    try:
        if 0 <= int(hex_str, 16) <= 0xFFF:  # Convierte la cadena hexadecimal a decimal y
                                            #verifica si está en el rango permitido
            return True  
    except ValueError:  
        pass  
    return False  


def convertir_numeros(hex_str):
    """Convierte un número hexadecimal a decimal, binario y octal"""
    decimal = int(hex_str, 16)  # Convierte el número hexadecimal a decimal
    binario = bin(decimal)[2:].zfill(12)  # Convierte a binario, elimina el prefijo
                                          #"0b (que saldria normalmente para indicar
                                          #que esta en binario)" y completa con ceros hasta 12 bits
    octal = oct(decimal)[2:]  # Convierte a octal y elimina el prefijo "0o (lo mismo que con binario)"
    return decimal, binario, octal  

# para el dato binario ingresado el programa muestra la figura de la señal digital de codificación NRZI.

def generar_nrzi_bipolar(bits):
    """Genera la señal NRZI en representación bipolar (+V y -V)."""
    tiempo = [0]          # comienza en t = 0
    señal = [1]            # estado inicial en +V antes de t=0
    nivel_actual = 1       # la señal empieza en +V

    for i, bit in enumerate(bits):
        tiempo.append(i)            # mantiene el nivel antes del bit
        señal.append(nivel_actual)

        if bit == '1':               # si el bit es 1, invierte la señal
            nivel_actual *= -1  

        tiempo.append(i)         # marca el final del bit
        señal.append(nivel_actual)
    
    # asegurar que la señal se extienda después del último bit
    tiempo.append(len(bits))
    señal.append(nivel_actual)

    return tiempo, señal

def graficar_nrzi(binario):
    """Grafica la señal NRZI bipolar correctamente."""
    tiempo, señal = generar_nrzi_bipolar(binario)

    plt.figure(figsize=(10, 3))
    plt.step(tiempo, señal, where='post', linewidth=2, color='b')
    plt.ylim(-1.5, 1.5)
    plt.yticks([-1, 0, 1], ["-V", "0", "+V"])
    plt.xticks(range(0, len(binario) + 1))
    plt.xlabel("Tiempo")
    plt.ylabel("Amplitud")
    plt.title("Codificación NRZI Bipolar")
    plt.grid(True)

    print("Presiona ENTER para cerrar la gráfica...")
    plt.show(block=False)  # No bloquea la ejecución para esperar la tecla

    plt.waitforbuttonpress()  # Espera hasta que el usuario presione una tecla (ENTER)
    plt.close()  # Cierra la ventana de la gráfica





# permitir al usuario definir si quiere usar paridad par o impar;

def solicitar_paridad():
    while True:

        paridad = input("Seleccione el tipo de paridad (par/impar): ").lower()
        
        if paridad in ['par', 'impar']:
            return paridad
        else:
            print("Opción no válida. Por favor ingrese 'par' o 'impar'.")


# codificar los datos binarios con el código de Hamming (17,12) y mostrar una tabla con los bits de datos y paridad.

def codificar_hamming(binario, tipo_paridad):
    bits_datos = [int(bit) for bit in binario] # convertir cadena de bits a lista de enteros
    hamming = [0] * 17
    j = 0
    
    # insertar bits de datos
    for i in range(17):
        if (i + 1) not in [1, 2, 4, 8, 16]:
            hamming[i] = bits_datos[j]
            j += 1

    # función corregida para calcular paridad
    def calcular_paridad(pos):
        count_ones = sum(
            hamming[i] 
            for i in range(17) 
            if (i + 1) & pos
        )
        if tipo_paridad == 'par':
            return 1 if count_ones % 2 == 0 else 0  # Even: 1 si conteo es par
        else:
            return 1 if count_ones % 2 != 0 else 0  # Odd: 1 si conteo es impar
    
    # calcular bits de paridad
    for pos in [1, 2, 4, 8, 16]:
        hamming[pos - 1] = calcular_paridad(pos)
    
    return ''.join(map(str, hamming)) # convertir lista de enteros a cadena de bits



def mostrar_tabla_hamming(binario, hamming, tipo_paridad):
    # lista de posiciones (base 1) y sus tipos
    posiciones = range(1, 18)
    tipos = [
        "p1", "p2", "d1", "p3", "d2", "d3", "d4", "p4", 
        "d5", "d6", "d7", "d8", "d9", "d10", "d11", "p5", "d12"
    ]
    
    # datos sin paridad (para mostrar en tabla)
    datos_sin_paridad = []
    j = 0
    for i in range(17):
        if (i + 1) in [1, 2, 4, 8, 16]:  # posiciones de paridad
            datos_sin_paridad.append("")
        else:
            datos_sin_paridad.append(binario[j])
            j += 1
    
    # crear DataFrame
    df = pd.DataFrame({
        "Posición": posiciones,
        "Tipo": tipos,
        "Palabra de Datos (sin paridad)": datos_sin_paridad,
        "p1": [hamming[0] if i == 0 else "" for i in range(17)],
        "p2": [hamming[1] if i == 1 else "" for i in range(17)],
        "p4": [hamming[3] if i == 3 else "" for i in range(17)],
        "p8": [hamming[7] if i == 7 else "" for i in range(17)],
        "p16": [hamming[15] if i == 15 else "" for i in range(17)],
        "Palabra de Datos (con paridad)": list(hamming)
    })
    
    # mostrar tabla
    print("\n--- Tabla de Codificación Hamming (17,12) ---")
    
    # configurar pandas para mostrar todas las filas/columnas
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)
    print(df.to_string(index=False))
    




while True:
    hex_input = input("\nIngrese un número hexadecimal (000 a FFF) o 'salir' para terminar: ").upper()
    # .upper() convierte la entrada a mayúsculas ejemplo si se esbribe 6ab -> 6AB para poder trabajar bien
    
    if hex_input == "SALIR":  
        print("Programa terminado.")
        break  

    if validar_hexadecimal(hex_input):  # Verifica si la entrada es un número hexadecimal válido
        decimal, binario, octal = convertir_numeros(hex_input)  # Convierte a decimal, binario y octal
        
        print("\nTabla de Conversiones:")
        print(f"{'Hexadecimal':<12}{'Decimal':<12}{'Binario':<16}{'Octal':<8}")
        print(f"{hex_input:<12}{decimal:<12}{binario:<16}{octal:<8}")
        

        graficar_nrzi(binario)  # Generar la gráfica NRZI

        tipo_paridad = solicitar_paridad()

        hamming_codificado = codificar_hamming(binario, tipo_paridad)
        mostrar_tabla_hamming(binario, hamming_codificado, tipo_paridad)


    else:
        print("Error: Ingrese un número válido entre 000 y FFF o escriba 'salir'.") 








    
