
# Función para abrir y leer el archivo del genoma (FASTA)
def abrir_archivo_genoma(archivo_genoma):
    # Verificar si el archivo existe y luego abrirlo
    file = None
    try:
        file = open(archivo_genoma, 'r')
        lineas = file.readlines()
        # Verificar si es un archivo FASTA válido
        if not lineas or not lineas[0].startswith(">"):
            print("Error: El archivo FASTA no tiene formato válido o está corrupto.")
            return None
        # Concatenar el resto del archivo (sin la cabecera)
        genoma = "".join([line.strip() for line in lineas[1:]])  # Omitir la cabecera
        return genoma
    except FileNotFoundError:
        print(f"Error: El archivo {archivo_genoma} no se encuentra.")
        return None
    finally:
        if file:
            file.close()


# Función para guardar el genoma en un archivo en la carpeta 'results'
def guardar_genoma_en_resultados(genoma):
    ruta_resultados = r"C:\Users\yeimi\peak_analysis\results\genoma_procesado.txt"
    try:
        with open(ruta_resultados, 'w') as archivo:
            archivo.write(genoma)
        print(f"El genoma procesado se ha guardado correctamente en: {ruta_resultados}")
    except Exception as e:
        print(f"Error al guardar el archivo de genoma: {e}")


# Función principal
def main():
    # Ruta del archivo de genoma
    archivo_genoma = r"C:\Users\yeimi\peak_analysis\data\E_coli_K12_MG1655_U00096.3.txt"
    
    # Abrir y leer el archivo de genoma
    genoma = abrir_archivo_genoma(archivo_genoma)
    
    if genoma is None:
        print("Error: No se pudieron cargar los archivos correctamente. Saliendo.")
        return
    
    # Guardar el genoma procesado en 'results'
    guardar_genoma_en_resultados(genoma)
    
    # Calcular el número total de letras en el genoma
    total_nucleotidos = len(genoma)
    
    # Imprimir información sobre el genoma cargado
    print(f"Archivo de genoma cargado correctamente. Longitud del genoma: {total_nucleotidos} caracteres.")
    

if __name__ == "__main__":
    main()
