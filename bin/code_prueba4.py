
def cargar_genoma(fasta_path):
    """Carga el genoma desde un archivo FASTA y devuelve una única cadena de texto."""
    try:
        with open(fasta_path, 'r') as f:
            lineas = f.readlines()
            genoma = ''.join([linea.strip() for linea in lineas if not linea.startswith('>')])
        return genoma
    except Exception as e:
        print(f"Error al cargar el genoma: {e}")
        return None

def leer_archivo_picos(peaks_path):
    """Lee el archivo de picos y devuelve una lista de diccionarios con TF_name, start y end."""
    lista_picos = []
    try:
        with open(peaks_path, 'r') as f:
            for linea in f:
                columnas = linea.strip().split('\t')
                if len(columnas) < 6:
                    continue
                tf_name, peak_id, _, start, end, strand = columnas[:6]
                try:
                    start = int(start)
                    end = int(end)
                    lista_picos.append({
                        'TF_name': tf_name,
                        'peak_id': peak_id,
                        'start': start,
                        'end': end,
                        'strand': strand
                    })
                except ValueError:
                    continue
        return lista_picos
    except FileNotFoundError:
        print(f"Error: no se encontró el archivo '{peaks_path}'")
        return []

def extraer_secuencias(peaks_data, genoma):
    """Agrupa las secuencias extraídas por TF_name en un diccionario."""
    secuencias_por_tf = {}
    for pico in peaks_data:
        tf = pico['TF_name']
        peak_id = pico['peak_id']
        start = pico['start']
        end = pico['end']

        if start > end:
            start, end = end, start

        if start < 0 or end > len(genoma):
            continue

        secuencia = genoma[start:end]

        if tf not in secuencias_por_tf:
            secuencias_por_tf[tf] = []
        secuencias_por_tf[tf].append((peak_id, secuencia))
    return secuencias_por_tf

def guardar_fasta_por_tf(secuencias_por_tf, output_dir):
    import os
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Info: Output directory created: {output_dir}")

    for tf_name, lista_secuencias in secuencias_por_tf.items():
        archivo_salida = os.path.join(output_dir, f"{tf_name}.fa")
        with open(archivo_salida, 'w') as f:
            for peak_id, secuencia in lista_secuencias:
                f.write(f">{peak_id}\n")
                for i in range(0, len(secuencia), 60):
                    f.write(secuencia[i:i+60] + '\n')

def main():
    genoma_archivo = "C:/Users/yeimi/peak_analysis/data/E_coli_K12_MG1655_U00096.3.txt"
    picos_archivo = "C:/Users/yeimi/peak_analysis/data/union_peaks_file.tsv"
    carpeta_resultados = "C:/Users/yeimi/peak_analysis/results"

    genoma = cargar_genoma(genoma_archivo)
    if not genoma:
        print(f"No se encontro el genoma")
        return

    peaks = leer_archivo_picos(picos_archivo)
    if not peaks:
        (f"No se encontro el archivo peaks")
        return

    secuencias_por_tf = extraer_secuencias(peaks, genoma)
    guardar_fasta_por_tf(secuencias_por_tf, carpeta_resultados)

    print(f"El archivo '{genoma_archivo}' se ha analizado y se han encontrado los peaks del archivo '{picos_archivo}'.")
    print(f"Los resultados se han guardado en la carpeta: '{carpeta_resultados}'.")

if __name__ == "__main__":
    main()
