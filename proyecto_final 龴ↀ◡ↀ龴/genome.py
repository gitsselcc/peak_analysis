# genome.py : Lectura del archivo de genoma en formato FASTA.
#Abre y procesa el archivo FASTA del genoma. Retorna una cadena con el genoma y su longitud
def abrir_genoma(archivo_genoma):
   
    try:
        with open(archivo_genoma, 'r') as file:             #Abre el archivo en modo lectura 
            lineas = file.readlines()
             # Verifica si el archivo está vacío o no tiene el formato FASTA adecuado.
            if not lineas or not lineas[0].startswith(">"):
                print("Error: El archivo FASTA no tiene formato válido o está corrupto.")
                return None, 0
            # Une las líneas del genoma en una sola cadena, omite la primera por que es la cabecera
            genoma = "".join([line.strip() for line in lineas[1:]])
            return genoma, len(genoma)
    except FileNotFoundError: #Manejo de error archivo no existe
        print(f"Error: El archivo {archivo_genoma} no se encuentra.")
        return None, 0
    except Exception as e:   #Manejo de error archivo nos e puede abrir
        print(f"Error al abrir el archivo del genoma: {e}")
        return None, 0
