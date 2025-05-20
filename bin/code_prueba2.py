
def cargar_genoma(fasta_path):
    """Carga el genoma desde un archivo FASTA y devuelve una cadena."""
    try:
        with open(fasta_path, 'r') as f:
            lineas = f.readlines()
            secuencia = ''.join([linea.strip() for linea in lineas if not linea.startswith('>')])
        return secuencia
    except FileNotFoundError:
        print(f"Error: no se encontró el archivo '{fasta_path}'")
        return None
    except Exception as e:
        print(f"Error al leer el archivo FASTA: {e}")
        return None

def leer_picos(tsv_path):
    """Lee el archivo TSV y organiza los picos por TF_name."""
    tf_dict = {}
    try:
        with open(tsv_path, 'r') as f:
            for linea in f:
                columnas = linea.strip().split('\t')
                if len(columnas) < 6:
                    continue
                tf_name, peak_id, _, start, end, strand = columnas[:6]
                try:
                    start = int(start)
                    end = int(end)
                    if strand != '+':
                        continue  # solo cadena forward
                    if tf_name not in tf_dict:
                        tf_dict[tf_name] = []
                    tf_dict[tf_name].append((peak_id, start, end))
                except ValueError:
                    continue
        return tf_dict
    except FileNotFoundError:
        print(f"Error: no se encontró el archivo '{tsv_path}'")
        return {}

def extraer_y_guardar(tf_dict, genoma, salida_dir, force=True, log_path="C:/Users/yeimi/peak_analysis/results/log.txt"):
    import os
    if not os.path.exists(salida_dir):
        os.makedirs(salida_dir)
        print(f"Info: Output directory created: {salida_dir}")

    with open(log_path, 'w') as log:
        for tf_name, picos in tf_dict.items():
            archivo_salida = os.path.join(salida_dir, f"{tf_name}.fa")

            if os.path.exists(archivo_salida) and not force:
                print(f"Archivo {archivo_salida} ya existe. Omitido.")
                continue

            with open(archivo_salida, 'w') as fa:
                for peak_id, start, end in picos:
                    if start > end:
                        start, end = end, start
                        log.write(f"Advertencia: Coordenadas invertidas para {peak_id}. Corregido a {start}-{end}.\n")

                    if start < 0 or end > len(genoma):
                        log.write(f"Advertencia: Coordenadas fuera de rango para {peak_id}: {start}-{end}.\n")
                        continue

                    secuencia = genoma[start:end]
                    fa.write(f">{peak_id}\n")
                    for i in range(0, len(secuencia), 60):
                        fa.write(secuencia[i:i+60] + '\n')

def main():
    # Asignación clara de archivos a variables
    genoma_archivo = "C:/Users/yeimi/peak_analysis/data/E_coli_K12_MG1655_U00096.3.txt"
    picos_archivo = "C:/Users/yeimi/peak_analysis/data/union_peaks_file.tsv"
    carpeta_resultados = "C:/Users/yeimi/peak_analysis/results"

    genoma = cargar_genoma(genoma_archivo)
    if not genoma:
        return

    peaks = leer_picos(picos_archivo)
    if not peaks:
        return

    extraer_y_guardar(peaks, genoma, carpeta_resultados, force=True)

    print(f"El archivo '{genoma_archivo}' se ha analizado y se han encontrado los peaks del archivo '{picos_archivo}'.")
    print(f"Los resultados se han guardado en la carpeta: '{carpeta_resultados}'.")

if __name__ == "__main__":
    main()
