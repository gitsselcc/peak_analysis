# peaks.py : Carga, limpieza y agrupamiento de coordenadas de picos.

def registrar_log(mensaje, archivo):
   
    #Registra un mensaje en el archivo de log proporcionado.
    #Cada mensaje se agrega al final del archivo sin sobrescribir contenido
    with open(archivo, "a") as archivo_log: # Abre el archivo en modo "append"
        archivo_log.write(mensaje + "\n") # Escribe el mensaje y agrega un salto de línea

def cargar_peaks(archivo_peaks, log_path):
  
    #Carga y valida los picos desde un archivo TSV.
    #Corrige coordenadas invertidas y omite líneas inválidas.
    '''
    Parámetros:
    - archivo_peaks: Ruta del archivo de picos en formato TSV.
    - log_path: Ruta del archivo de log donde se registran advertencias.

    Retorna:
    - lista_peaks: Lista de diccionarios con información de cada 
    '''

    lista_peaks = [] # Inicializa la lista donde se almacenarán los picos
    try:
        with open(archivo_peaks, 'r') as archivo:
            lineas = archivo.readlines()  # Lee todas las líneas del archivo.

    except Exception as e:  # Captura cualquier error al abrir el archivo.

        print("Error: No se pudo abrir el archivo de picos.")
        return []

    lineas = lineas[1:]  # Omitir encabezado
    for linea in lineas:
        columnas = linea.strip().split("\t")
        if len(columnas) >= 5:   # Asegura que la línea tenga al menos 5 columnas válidas.
            tf_name = columnas[2]  # Extrae el nombre del factor de transcripción
            start_peak = columnas[3].split(".")[0] # Extrae la coordenada inicial, eliminando decimales si existen
            end_peak = columnas[4].split(".")[0] # Extrae la coordenada final, eliminando decimales si existen.

            try:
                start = int(start_peak) # Convierte la coordenada inicial a entero.
                end = int(end_peak)  # Convierte la coordenada final a entero.
                # Si la coordenada de inicio es mayor que la de fin, se intercambian valores.
                if start > end:
                    registrar_log(f"Advertencia: Coordenadas invertidas para {tf_name}. Se corrigieron: start={start}, end={end}", log_path)
                    start, end = end, start   # Ajuste para garantizar el orden correcto.
                lista_peaks.append({"TF_name": tf_name, "start": start, "end": end}) # Agrega el pico validado a la lista
            except:
                registrar_log(f"Advertencia: Coordenadas no válidas, línea omitida: {linea.strip()}", log_path)
        else: # Registra el error en el log si la línea no tiene el formato adecuado.
            registrar_log(f"Advertencia: Línea incompleta, se omite: {linea.strip()}", log_path)
    return lista_peaks # Retorna la lista de picos procesados


def agrupar_peaks(peaks):
   
    #Agrupa los picos en un diccionario por TF_name.
   
    grupos = {} # Inicializa el diccionario para agrupar los picos
    for pico in peaks:
        tf = pico["TF_name"] # Extrae el nombre del TF.
        # Si el TF no está en el diccionario, se inicializa con una lista vacía.
        if tf not in grupos:
            grupos[tf] = []
        grupos[tf].append((pico["start"], pico["end"])) # Agrega la coordenada del pico al grupo correspondiente.
    return grupos # Retorna el diccionario de grupos de picos
