# genome.py : Lectura del archivo de genoma en formato FASTA.
#Abre y procesa el archivo FASTA del genoma. Retorna una cadena con el genoma y su longitud
def abrir_genoma(archivo_genoma):
   
    try:
        with open(archivo_genoma, 'r') as file:             #Abre el archivo en modo lectura 
            lineas = file.readlines()
            if not lineas or not lineas[0].startswith(">"):
                print("Error: El archivo FASTA no tiene formato válido o está corrupto.")
                return None, 0
            genoma = "".join([line.strip() for line in lineas[1:]])
            return genoma, len(genoma)
    except FileNotFoundError:
        print(f"Error: El archivo {archivo_genoma} no se encuentra.")
        return None, 0
    except Exception as e:
        print(f"Error al abrir el archivo del genoma: {e}")
        return None, 0
