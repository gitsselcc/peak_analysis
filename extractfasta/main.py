
# main.py: controlador principal del programa

import genome
import peaks
import io_utils

def main():
    io_utils.limpiar_logs()

    # Archivos de entrada
    archivo_genoma = "data/E_coli_K12_MG1655_U00096.3.txt"
    archivo_peaks = "data/union_peaks_file.tsv"

    # Procesar genoma
    genoma, longitud = genome.abrir_genoma(archivo_genoma)
    if genoma is None:
        print("Error. No se pudo leer el genoma. Saliendo.")
        return

    # Procesar peaks
    lista_peaks = peaks.cargar_peaks(archivo_peaks, "output/log_errores_peaks.txt")
    if not lista_peaks:
        print("No se encontraron picos validos. Saliendo.")
        return

    grupos = peaks.agrupar_peaks(lista_peaks)

    # Guardar archivos FASTA
    io_utils.escribir_fasta(grupos, genoma, "output/log_errores_extraccion.txt")

    print(f"Proceso completado. Las listas de nucleotidos segun cada peak se encuentran en /output.")
    print(f"Genoma con la cantidad de {longitud} nucleotidos.")

if __name__ == "__main__":
    main()
