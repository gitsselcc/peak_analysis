
# Función para registrar mensajes en el log de errores de peaks
def registrar_log(mensaje, archivo="log_errores_peaks.txt"):
    ruta_log = fr"C:\Users\yeimi\peak_analysis\results\{archivo}"           #Cuando se encuentren errores en los peaks, se podra ir escribiendo en el archivo creado en results
    with open(ruta_log, "a") as archivo_log:                                # f y r para cadena raw formateada que nos permitira insertar el nombre dinamicamente y no tener problemas con carcatereres especiales
        archivo_log.write(mensaje + "\n")

# Función para abrir y procesar el archivo del genoma (FASTA) E.Coli
def abrir_y_guardar_genoma(archivo_genoma):
    try:
        with open(archivo_genoma, 'r') as file:             #Abrir archivo modo lectura (no queremos problemas jsjs)
            lineas = file.readlines()
            if not lineas or not lineas[0].startswith(">"):         #Verificar su formato FASTA
                print("Error: El archivo FASTA no tiene formato válido o está corrupto.")       #Si no es FASTA, mensaje de error
                return None, 0
            genoma = "".join([line.strip() for line in lineas[1:]])                 #Eliminar la primera linea, eliminar espacios, unir todas las lineas
            ruta_guardado = r"C:\Users\yeimi\peak_analysis\results\genoma_procesado.txt"        #La ruta donde guardare mi archivo
            with open(ruta_guardado, 'w') as salida:                #abrir el archivo de mi ruta dada, modo escritura para sobreescribir
                salida.write(genoma)                            #Guardar la secuencia procesada
            print(f"El genoma procesado se ha guardado correctamente en 'results'")
            return genoma, len(genoma)                          #Guardar la cantidad de letras, la longitud del genoma
    except FileNotFoundError:
        print(f"Error: El archivo {archivo_genoma} no se encuentra.")                   #Casos  de errores, el archivo no se encuentra o hay errores al abrirlo
        return None, 0
    except Exception as e:
        print(f"Error al abrir el archivo del genoma: {e}")
        return None, 0

# Función para cargar, limpiar y validar los peaks
def cargar_peaks(archivo_peaks):
    peaks = []                          #Lista vacia donde guardaremos los peaks procesados
    try:
        with open(archivo_peaks, 'r') as archivo:
            lineas = archivo.readlines()
    except:                                     #Errores de Apertura
        print("Error: No se pudo abrir el archivo de picos.")
        return []                               #Devuelve la lista

    lineas = lineas[1:]  # Omitir encabezado, no queremos ruido
    for linea in lineas:                        #Recorrer las lineas de mi archivo
        columnas = linea.strip().split("\t")        #Las columnas se delimitan por tabulaciones, las usaremos
        if len(columnas) >= 5:                          #Verificar que sea un archivo con estructura que nos permita extraer TF, peak end and start
            tf_name = columnas[2]                           #La columna de TF
            start_peak = columnas[3].split(".")[0]          #La columna de start peak y end peak, debemos eliminar el . y el 0
            end_peak = columnas[4].split(".")[0]
            try:
                start = int(start_peak)             #Convertimos coordenadas a numeros enteros, por si acaso 
                end = int(end_peak)
                if start > end:                         #Posible error, que esten al reves los peaks, los corregimos con...
                    registrar_log(f"Advertencia: Coordenadas invertidas para {tf_name}. Se corrigieron: start={start}, end={end}")      #Si se hace un cambio, se registrara en log y seguira el codigo
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

# Extrae secuencias desde el genoma según coordenadas de los peaks
def extraer_y_guardar_secuencias(peaks, genoma):
    grupos = {}
    total_genoma = len(genoma)

    for pico in peaks:
        tf = pico["TF_name"]
        start, end = pico["start"], pico["end"]

        if start < 0 or end > total_genoma:
            registrar_log(f"Advertencia: Coordenadas fuera de rango para {tf} (start={start}, end={end})", "log_errores_extraccion.txt")
            continue

        secuencia = genoma[start:end]
        if tf not in grupos:
            grupos[tf] = []
        grupos[tf].append((start, end, secuencia))

    for tf in grupos:
        ruta_fasta = fr"C:\Users\yeimi\peak_analysis\results\{tf}.fasta"
        with open(ruta_fasta, "w") as archivo_fasta:
            for i, (start, end, secuencia) in enumerate(grupos[tf], 1):
                encabezado = f">{tf}_Peak{i}_pos{start}-{end}"
                archivo_fasta.write(encabezado + "\n")
                archivo_fasta.write(secuencia + "\n")

# Función principal
def main():
    # Limpiar logs al inicio
    open(r"C:\Users\yeimi\peak_analysis\results\log_errores.txt", "w").close()
    open(r"C:\Users\yeimi\peak_analysis\results\log_errores_extraccion.txt", "w").close()

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

    # Extraer secuencias y guardarlas
    extraer_y_guardar_secuencias(lista_peaks, genoma)

    # Mensaje final
    if resultados_guardados:
        print("Proceso completado. El listado de peaks junto con los posibles errores se ha guardado en 'results'.")
    else:
        print("No se procesaron picos válidos. El listado de peaks y errores se ha guardado en 'results'.")

    print(f"Longitud total del genoma: {total_nucleotidos} letras.")
    print("Las extracciones de secuencias se han guardado en la carpeta 'results'.")

if __name__ == "__main__":
    main()
