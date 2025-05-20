
# io_utils.py : para funciones de entrada/salida/escritura de archivos FASTA.


def escribir_fasta(grupos, genoma, log_path):
    
    total_genoma = len(genoma)  #Escribe las secuencias FASTA agrupadas por TF
    for tf in grupos:
        ruta_resultados = f"output/{tf}.fasta"              # Donde se guardan los resultados 
        with open(ruta_resultados, "w") as archivo_fa:                  #Se adecua al formato FASTA
            for i, (start, end) in enumerate(grupos[tf], 1):
                if start < 0 or end > total_genoma:
                    with open(log_path, "a") as log:
                        log.write(f"Advertencia: Coordenadas fuera de rango para {tf} (start={start}, end={end})\n")
                    continue
                secuencia = genoma[start:end]
                encabezado = f">{tf}_Peak{i}_{start}-{end}"
                archivo_fa.write(encabezado + "\n")
                archivo_fa.write(secuencia + "\n")


def limpiar_logs():   #Limpia los archivos de log de errores
    
    open(r"output/log_errores_peaks.txt", "w").close()
    open(r"output/log_errores_extraccion.txt", "w").close()