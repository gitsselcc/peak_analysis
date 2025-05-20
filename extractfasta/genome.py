
# genome.py : Modulo encargado de la lectura y el rpocesamiento del archivo FASTA del genoma

def abrir_genoma(archivo_genoma):  #arruinaste mis sueños pepe, ahora solo abrira el archivo y no guardara su version procesada
    try:
        with open(archivo_genoma, 'r') as file:  #Abre el archivo en modo lectura 
            lineas = file.readlines()
            if not lineas or not lineas[0].startswith(">"):    #Verificar el formato FASTA 
                print("Error: El archivo FASTA no tiene formato válido o está corrupto.")  #si NO es FASTA, mensaje de error
                return None, 0
            genoma = "".join([line.strip() for line in lineas[1:]])   #Eliminar primera linea, espacios, unir las lineas (limpiar el formato)
            return genoma, len(genoma)   #Guardar la cantidad de letras (el genoma)
    except FileNotFoundError:
        print(f"Error: El archivo {archivo_genoma} no se encuentra.")
        return None, 0                                                          #Manejo general de errores, el archivo no existe o hay errores al abrirlo
    except Exception as e:
        print(f"Error al abrir el archivo del genoma: {e}")
        return None, 0