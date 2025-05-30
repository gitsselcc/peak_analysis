# main.py: controlador principal del programa

import genome
import peaks
import io_utils
import argparse
import os

def main():
    # Argumentos por línea de comandos
    parser = argparse.ArgumentParser(description="Extractor de secuencias FASTA por coordenadas de picos.")
    parser.add_argument("--genome", required=True, help="Ruta del archivo FASTA del genoma")
    parser.add_argument("--peaks", required=True, help="Ruta del archivo de picos TSV")
    parser.add_argument("--output", default="output", help="Directorio de salida (por defecto: output/)")
    args = parser.parse_args()

    # Crear carpeta de salida si no existe
    os.makedirs(args.output, exist_ok=True)

    # Limpiar logs
    io_utils.limpiar_logs(args.output)

    # Procesar genoma
    genoma, longitud = genome.abrir_genoma(args.genome)
    if genoma is None:
        print("Error. No se pudo leer el genoma. Saliendo.")
        return

    # Procesar peaks
    lista_peaks = peaks.cargar_peaks(args.peaks, f"{args.output}/log_errores_peaks.txt")
    if not lista_peaks:
        print("No se encontraron picos válidos. Saliendo.")
        return

    grupos = peaks.agrupar_peaks(lista_peaks)

    # Guardar archivos FASTA
    io_utils.escribir_fasta(grupos, genoma, f"{args.output}/log_errores_extraccion.txt", args.output)

# Revisar logs
    io_utils.revisar_log(f"{args.output}/log_errores_peaks.txt", "log_errores_peaks.txt")
    io_utils.revisar_log(f"{args.output}/log_errores_extraccion.txt", "log_errores_extraccion.txt")


    print(f"Proceso completado. Las secuencias FASTA están en {args.output}/")
    print(f"Genoma con una longitud de {longitud} nucleótidos.")

if __name__ == "__main__":
    main()
