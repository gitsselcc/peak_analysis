# io_utils.py : Funciones de entrada/salida y escritura de archivos FASTA.

import os
#Escribe las secuencias en grupos de TF en archivos FASTA y registra advertencias si las corrdenadas estan fuera de rango 
# Además, registra advertencias si las coordenadas están fuera de rango del genoma
def escribir_fasta(grupos, genoma, log_path, output_dir):
   
    total_genoma = len(genoma)# Calcula la longitud total del genoma
    for tf in grupos: # Define la ruta donde se guardará el archivo FASTA para cada grupo TF
        ruta_resultados = os.path.join(output_dir, f"{tf}.fasta")
        with open(ruta_resultados, "w") as archivo_fa: # Abre el archivo FASTA en modo escritura
            for i, (start, end) in enumerate(grupos[tf], 1):  # Itera sobre cada par de coordenadas
                if start < 0 or end > total_genoma:  # Verifica que las coordenadas sean válidas dentro del rango del genoma.
                    with open(log_path, "a") as log:  # Registra el error en el archivo de log.
                        log.write(f"Advertencia: Coordenadas fuera de rango para {tf} (start={start}, end={end})\n")
                    continue # Salta a la siguiente iteración si hay un error
                secuencia = genoma[start:end] # Extrae la secuencia del genoma basada en las coordenadas dadas
                encabezado = f">{tf}_Peak{i}_{start}-{end}"  # Define el encabezado del formato FASTA con información relevante
                # Escribe el encabezado y la secuencia en el archivo FASTA.
                archivo_fa.write(encabezado + "\n")
                archivo_fa.write(secuencia + "\n")

# Crea o limpia los archivos de log en el directorio de salida.
def limpiar_logs(output_dir):
   
    open(os.path.join(output_dir, "log_errores_peaks.txt"), "w").close()   # Log de errores en coordenadas de peaks.
    open(os.path.join(output_dir, "log_errores_extraccion.txt"), "w").close()  # Log de errores en extracción de secuencias.


# Revisa un archivo de log y muestra el número de errores registrados
def revisar_log(log_path, nombre_log):

    #Muestra si hubo errores en el log y cuántos.
  
    try:  # Intenta abrir el archivo de log en modo lectura.
        with open(log_path, "r") as f:
            lineas = f.readlines()
            if lineas: # Si hay líneas en el archivo, muestra cuántos errores existen
                print(f" {len(lineas)} advertencias registradas en {nombre_log}:")
                for i, linea in enumerate(lineas, 1):  # Itera sobre cada línea para mostrar los detalles del error.
                    print(f"  Línea {i}: {linea.strip()}")
            else:
                print(f" No se registraron errores en {nombre_log}.") # Mensaje si no hay errores registrados.
    except FileNotFoundError:
        print(f" No se encontró el archivo de log: {log_path}") # Manejo de error si el archivo de log no existe.


