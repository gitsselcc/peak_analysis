
# Función para registrar mensajes en el log de errores
def registrar_log(mensaje):
    ruta_log = r"C:\Users\yeimi\peak_analysis\results\log_errores.txt"
    archivo_log = open(ruta_log, "a")
    archivo_log.write(mensaje + "\n")
    archivo_log.close()

# Función para abrir y procesar el archivo del genoma (FASTA)
def abrir_y_guardar_genoma(archivo_genoma):
    try:
        with open(archivo_genoma, 'r') as file:
            lineas = file.readlines()
            if not lineas or not lineas[0].startswith(">"):
                print("Error: El archivo FASTA no tiene formato válido o está corrupto.")
                return None, 0
            genoma = "".join([line.strip() for line in lineas[1:]])
            ruta_guardado = r"C:\Users\yeimi\peak_analysis\results\genoma_procesado.txt"
            with open(ruta_guardado, 'w') as salida:
                salida.write(genoma)
            print(f"El genoma procesado se ha guardado correctamente en 'results'")
            return genoma, len(genoma)
    except FileNotFoundError:
        print(f"Error: El archivo {archivo_genoma} no se encuentra.")
        return None, 0
    except Exception as e:
        print(f"Error al abrir el archivo del genoma: {e}")
        return None, 0

# Función para cargar, limpiar y validar los peaks
def cargar_peaks(archivo_peaks):
    peaks = []
    try:
        with open(archivo_peaks, 'r') as archivo:
            lineas = archivo.readlines()
    except:
        print("Error: No se pudo abrir el archivo de picos.")
        return []

    lineas = lineas[1:]  # Omitir encabezado
    for linea in lineas:
        columnas = linea.strip().split("\t")
        if len(columnas) >= 5:
            tf_name = columnas[2]
            start_raw = columnas[3].split(".")[0]
            end_raw = columnas[4].split(".")[0]
            try:
                start = int(start_raw)
                end = int(end_raw)
                if start > end:
                    registrar_log(f"Advertencia: Coordenadas invertidas para {tf_name}. Se corrigieron: start={start}, end={end}")
                    start, end = end, start
                peaks.append({"TF_name": tf_name, "start": start, "end": end})
            except:
                registrar_log(f"Advertencia: Coordenadas no válidas, línea omitida: {linea.strip()}")
        else:
            registrar_log(f"Advertencia: Línea incompleta, se omite: {linea.strip()}")
    return peaks

# Agrupa los peaks y guarda el resumen
def agrupar_y_guardar(peaks):
    grupos = {}
    for pico in peaks:
        tf = pico["TF_name"]
        if tf not in grupos:
            grupos[tf] = []
        grupos[tf].append((pico["start"], pico["end"]))

    ruta_resultados = r"C:\Users\yeimi\peak_analysis\results\listado_de_peaks.txt"
    with open(ruta_resultados, "w") as archivo_resultados:
        contador = 1
        for tf in grupos:
            archivo_resultados.write(f"{tf}:\n")
            for i, (start, end) in enumerate(grupos[tf]):
                archivo_resultados.write(f"   - Peak {i+1}: {start}-{end}\n")
            contador += 1
    return len(grupos) > 0

# Función principal
def main():
    # Limpiar log al inicio
    open(r"C:\Users\yeimi\peak_analysis\results\log_errores.txt", "w").close()

    # Archivos de entrada
    archivo_genoma = r"C:\Users\yeimi\peak_analysis\data\E_coli_K12_MG1655_U00096.3.txt"
    archivo_peaks = r"C:\Users\yeimi\peak_analysis\data\union_peaks_file.tsv"

    # Procesar genoma
    genoma, total_nucleotidos = abrir_y_guardar_genoma(archivo_genoma)
    if genoma is None:
        print("Error: No se pudo procesar el genoma. Saliendo.")
        return

    # Procesar peaks
    lista_peaks = cargar_peaks(archivo_peaks)
    resultados_guardados = agrupar_y_guardar(lista_peaks)

    # Mensaje final
    if resultados_guardados:
        print("Proceso completado. El listado de peaks junto con los posibles errores se ha guardado en 'results'.")
    else:
        print("No se procesaron picos válidos. El listado de peaks y errores se ha guardado en 'results'.")

    print(f"Longitud total del genoma: {total_nucleotidos} letras.")

if __name__ == "__main__":
    main()
