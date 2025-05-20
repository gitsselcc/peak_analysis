
# peaks.py : Modulo encargado de cargar, limpiar y validar los peaks (ya no guarda un archivo de peaks)

#submodulo (se encarga de los errores que encontrariamos al hacer el proceso de los peaks)
def registrar_log(mensaje, archivo):
    
    with open(archivo, "a") as archivo_log:   #Registra mensajes en un archivo de log
        archivo_log.write(mensaje + "\n")
#Carga, limpia y valida los peaks del archivo que le proporcionaremos
def cargar_peaks(archivo_peaks, log_path):
    peaks = []                    #Lista vacia donde guardaremos los peaks procesados
    try:
        with open(archivo_peaks, 'r') as archivo:
            lineas = archivo.readlines()
    except:                         #Manejo de errores de apertura
        print("Error: No se pudo abrir el archivo de picos.")
        return []                      #Devuelve la lista vacia

    lineas = lineas[1:]  # Omitir encabezado evitar el ruido
    for linea in lineas:                #Recorrer las lineas de mi archivo
        columnas = linea.strip().split("\t")        #Usar las tabulaciones (que delimitan las columnas)
        if len(columnas) >= 5:                      #Verificar que tenga estructura suficiente para extraer TF, peak start and end
            tf_name = columnas[2]                   #La columna TF
            start_peak = columnas[3].split(".")[0]      #La columna de start peak y en peak donde hay q eliminar el . y el 0
            end_peak = columnas[4].split(".")[0]
            try:
                start = int(start_peak)             #Convertimos coordenadas a numeros enteros 
                end = int(end_peak)
                if start > end:      #Si se da el caso que los peaks esten invertidos, podremos corregir con...
                    registrar_log(f"Advertencia: Coordenadas invertidas para {tf_name}. Se corrigieron: start={start}, end={end}", log_path)  #Si se hace un cambio, se registra en el log y el codigo sigue
                    start, end = end, start
                peaks.append({"TF_name": tf_name, "start": start, "end": end})
            except:
                registrar_log(f"Advertencia: Coordenadas no válidas, línea omitida: {linea.strip()}", log_path)  #Si la conversion a numeros enteros falla
        else:
            registrar_log(f"Advertencia: Línea incompleta, se omite: {linea.strip()}", log_path)            #Si la linea tiene menos de cinco columnas 
    return peaks
# Agrupa los peaks y guarda el resumen
def agrupar_peaks(peaks):
    grupos = {}                 #Diccionario vacio
    for pico in peaks:              #Recorre la lista
        tf = pico["TF_name"]            #Obtiene el nombre del TF el factor de transcripcion
        if tf not in grupos:            #Si TF no esta en un grupo lo crea, a partir de alli, lo que tengan en mismo TF entraran a dicho grupo
            grupos[tf] = []
        grupos[tf].append((pico["start"], pico["end"]))
    return grupos