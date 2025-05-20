#Monitoreo de errores a lo largo de la implementacion del codigo se registraran.
def registrar_log(mensaje):
    ruta_log = r"C:\Users\yeimi\peak_analysis\results\log_errores.txt"
    archivo_log = open(ruta_log, "a")
    archivo_log.write(mensaje + "\n")
    archivo_log.close()


def cargar_peaks(archivo_peaks):
    peaks = []

    try:
        archivo = open(archivo_peaks, 'r')
        lineas = archivo.readlines()
        archivo.close()
    except:
        print("Error: No se pudo abrir el archivo de picos.")
        return []

    # Saltamos la primera línea, ya que ahi se encuentra el encabezado
    lineas = lineas[1:]
    #El tab es lo que separa las columnas de nuestro archivo, por lo que lo usaremos para delimitar
    for linea in lineas:
        columnas = linea.strip().split("\t")
        if len(columnas) >= 5:
            tf_name = columnas[2]                       #Columna de los TF
            start_peaks = columnas[3].split(".")[0]     #Columna de los start_peaks
            end_peaks = columnas[4].split(".")[0]       #Columna de los end_peaks
                                                        #Tanto la columna 4 y 5 se elimino el 0 y el punto
            try:
                start = int(start_peaks)
                end = int(end_peaks)

                if start > end:
                    registrar_log(f"Advertencia: Coordenadas invertidas para {tf_name}. Se corrigieron: start={start}, end={end}")
                    start, end = end, start         #Monitoreo de errores, revision de que peaks no esten invertidos

                peaks.append({
                    "TF_name": tf_name,
                    "start": start,
                    "end": end
                })
            except:
                registrar_log(f"Advertencia: Coordenadas no válidas, línea omitida: {linea.strip()}")
        else:
            registrar_log(f"Advertencia: Línea incompleta, se omite: {linea.strip()}")

    return peaks


def agrupar_y_guardar(peaks):               #Agrupar los peaks por nombre en base a su TF, ir recorriendo para encontrar los grupos
    grupos = {}
    for pico in peaks:
        tf = pico["TF_name"]
        if tf not in grupos:
            grupos[tf] = []
        grupos[tf].append((pico["start"], pico["end"]))

    # Guardar en archivo de resultados
    with open(r"C:\Users\yeimi\peak_analysis\results\listado_de_peaks.txt", "w") as archivo_resultados:
        contador = 1
        for tf in grupos:
            archivo_resultados.write(f"{tf}: {contador}\n")
            for i in range(len(grupos[tf])):
                start, end = grupos[tf][i]
                archivo_resultados.write(f"   - Peak {i+1}: {start}-{end}\n")
            contador += 1

    return len(grupos) > 0  # Si se procesaron picos correctamente


# Ejecutar
archivo_peaks = r"C:\Users\yeimi\peak_analysis\data\union_peaks_file.tsv"

# Limpiar log al inicio
open(r"C:\Users\yeimi\peak_analysis\results\log_errores.txt", "w").close()

lista_peaks = cargar_peaks(archivo_peaks)

# Verificamos si hubo picos procesados correctamente
resultados_guardados = agrupar_y_guardar(lista_peaks)

# Imprimir si hubo errores y guardar los resultados
if resultados_guardados:
    print("Proceso completado. El listado de peaks junto con los posibles errores se ha guardado en 'results'.")
else:
    print("No se procesaron picos válidos. El listado de peaks y errores se ha guardado en 'results'.")
