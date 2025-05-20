
# genome.py : Modulo encargado de la lectura y el rpocesamiento del archivo FASTA del genoma

def abrir_genoma(archivo_genoma):  #arruinaste mis sueños pepe, ahora solo abrira el archivo y no guardara su version procesada
    try:
        with open(archivo_genoma, 'r') as file:  #Abre el archivo en modo lectura 
            lineas = file.readlines()
            if not lineas or not lineas[0].startswith(">"):    #Verificar el formato FASTA 
                print("Error: El archivo FASTA no tiene formato válido o está corrupto.")  #si NO es FASTA, mensaje de error
                return None, 0
            genoma = "".join([line.strip() for line in lineas[1:]])   #Eliminar primera linea, espacios, unir las lineas (limpiar el formato)
            return genoma, len(genoma)   #Guardar la cantidad de letras (el genoma)
    except FileNotFoundError:
        print(f"Error: El archivo {archivo_genoma} no se encuentra.")
        return None, 0                                                          #Manejo general de errores, el archivo no existe o hay errores al abrirlo
    except Exception as e:
        print(f"Error al abrir el archivo del genoma: {e}")
        return None, 0


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


# io_utils.py : para funciones de entrada/salida/escritura de archivos FASTA.


def escribir_fasta(grupos, genoma, log_path):
    
    total_genoma = len(genoma)  #Escribe las secuencias FASTA agrupadas por TF
    for tf in grupos:
        ruta_resultados = f"results/{tf}.fasta"              # Donde se guardan los resultados 
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
    
    open(r"results/log_errores_peaks.txt", "w").close()
    open(r"results/log_errores_extraccion.txt", "w").close()


#main.py: controlador principal del programa

def main():
    limpiar_logs()
# Archivos de entrada
    archivo_genoma = r"data/E_coli_K12_MG1655_U00096.3.txt"
    archivo_peaks = r"data/union_peaks_file.tsv"
# Procesar genoma
    genoma, longitud = abrir_genoma(archivo_genoma)
    if genoma is None:
        print("Error.No se pudo leer el genoma. Saliendo.")
# Procesar peaks/errores en peaks
    peaks = cargar_peaks(archivo_peaks, "results/log_errores_peaks.txt")
    grupos = agrupar_peaks(peaks)
    if archivo_peaks is None:
        print("Archivo peaks no se encuentra. Saliendo.")
    escribir_fasta(grupos, genoma, "results/log_errores_extraccion.txt")

    print(f"Proceso completado. Las listas de nucleotidos segun cada peak se encuentran en /results. Genoma con la cantidad de {longitud} nucleotidos.")

if __name__ == "__main__":
    main()

