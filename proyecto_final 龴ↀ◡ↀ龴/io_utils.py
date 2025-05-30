# io_utils.py : Funciones de entrada/salida y escritura de archivos FASTA.

import os
#Escribe las secuencias en grupos de TF en archivos FASTA y registra advertencias si las corrdenadas estan fuera de rango 
# Además, registra advertencias si las coordenadas están fuera de rango del genoma
def escribir_fasta(grupos, genoma, log_path, output_dir):
   
    total_genoma = len(genoma)
    for tf in grupos:
        ruta_resultados = os.path.join(output_dir, f"{tf}.fasta")
        with open(ruta_resultados, "w") as archivo_fa:
            for i, (start, end) in enumerate(grupos[tf], 1):
                if start < 0 or end > total_genoma:
                    with open(log_path, "a") as log:
                        log.write(f"Advertencia: Coordenadas fuera de rango para {tf} (start={start}, end={end})\n")
                    continue
                secuencia = genoma[start:end]
                encabezado = f">{tf}_Peak{i}_{start}-{end}"
                archivo_fa.write(encabezado + "\n")
                archivo_fa.write(secuencia + "\n")

# Crea o limpia los archivos de log en el directorio de salida.
def limpiar_logs(output_dir):
   
    open(os.path.join(output_dir, "log_errores_peaks.txt"), "w").close()
    open(os.path.join(output_dir, "log_errores_extraccion.txt"), "w").close()


def revisar_log(log_path, nombre_log):
    """
    Muestra si hubo errores en el log y cuántos.
    """
    try:
        with open(log_path, "r") as f:
            lineas = f.readlines()
            if lineas:
                print(f" {len(lineas)} advertencias registradas en {nombre_log}:")
                for i, linea in enumerate(lineas, 1):
                    print(f"  Línea {i}: {linea.strip()}")
            else:
                print(f" No se registraron errores en {nombre_log}.")
    except FileNotFoundError:
        print(f" No se encontró el archivo de log: {log_path}")
