
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

    # Saltamos la primera línea
    lineas = lineas[1:]

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


def agrupar_y_mostrar(peaks):
    grupos = {}
    for pico in peaks:
        tf = pico["TF_name"]
        if tf not in grupos:
            grupos[tf] = []
        grupos[tf].append((pico["start"], pico["end"]))

    contador = 1
    for tf in grupos:
        print(f"{contador}. TF_name: {tf}")
        for i in range(len(grupos[tf])):
            start, end = grupos[tf][i]
            print(f"   - Peak {i+1}: start = {start}, end = {end}")
        contador += 1


# Ejecutar
archivo_peaks = r"C:\Users\yeimi\peak_analysis\data\union_peaks_file.tsv"

# Limpiar log al inicio
open(r"C:\Users\yeimi\peak_analysis\results\log_errores.txt", "w").close()

lista_peaks = cargar_peaks(archivo_peaks)
agrupar_y_mostrar(lista_peaks)
