
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



# Función principal
def main():
    # Rutas de los archivos
    archivo_genoma = r"C:\Users\yeimi\peak_analysis\data\E_coli_K12_MG1655_U00096.3.txt"
    
    # Abrir y leer los archivos
    genoma = abrir_archivo_genoma(archivo_genoma)
    
    if genoma is None :
        print("Error: No se pudieron cargar los archivos correctamente. Saliendo.")
        return
    
    # Imprimir información sobre los archivos cargados
    print(f"Archivo de genoma cargado correctamente. Longitud del genoma: {len(genoma)} caracteres.")
    
    # Aquí puedes continuar con el procesamiento del genoma y los picos

if __name__ == "__main__":
    main()
