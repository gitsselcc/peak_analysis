# peaks.py : Carga, limpieza y agrupamiento de coordenadas de picos.

def registrar_log(mensaje, archivo):
    """
    Registra un mensaje en el archivo de log proporcionado.
    """
    with open(archivo, "a") as archivo_log:
        archivo_log.write(mensaje + "\n")

def cargar_peaks(archivo_peaks, log_path):
    """
    Carga y valida los picos desde un archivo TSV.
    Corrige coordenadas invertidas y omite líneas inválidas.
    """
    lista_peaks = []
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
            start_peak = columnas[3].split(".")[0]
            end_peak = columnas[4].split(".")[0]
            try:
                start = int(start_peak)
                end = int(end_peak)
                if start > end:
                    registrar_log(f"Advertencia: Coordenadas invertidas para {tf_name}. Se corrigieron: start={start}, end={end}", log_path)
                    start, end = end, start
                lista_peaks.append({"TF_name": tf_name, "start": start, "end": end})
            except:
                registrar_log(f"Advertencia: Coordenadas no válidas, línea omitida: {linea.strip()}", log_path)
        else:
            registrar_log(f"Advertencia: Línea incompleta, se omite: {linea.strip()}", log_path)
    return lista_peaks

def agrupar_peaks(peaks):
    """
    Agrupa los picos en un diccionario por TF_name.
    """
    grupos = {}
    for pico in peaks:
        tf = pico["TF_name"]
        if tf not in grupos:
            grupos[tf] = []
        grupos[tf].append((pico["start"], pico["end"]))
    return grupos
