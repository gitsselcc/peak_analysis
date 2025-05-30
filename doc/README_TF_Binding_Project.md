

# Proyecto de Automatización para la Identificación de Sitios de Unión de Factores de Transcripción en _E. coli_ mediante ChIP-Seq

## Resumen

```
      |\      _,,,---,,_           
ZZZzz /,`.-'`'    -.  ;-;;,_     :dna: ¡Hola!
     |,4-  ) )-,_. ,\ (  `'-'     
    '---''(_/--'  `-'\_)          

```

Este proyecto tiene como objetivo automatizar el proceso de identificación de las regiones específicas de unión de 144 factores de transcripción (TFs) en el genoma completo de _Escherichia coli_. Estas regiones han sido determinadas experimentalmente mediante la técnica de ChIP-seq.

Se desarrolló una herramienta en Python que, a partir de un archivo de picos y un archivo FASTA del genoma, genera archivos FASTA individuales para cada TF, conteniendo las secuencias correspondientes a sus sitios de unión.

## Archivos de Entrada

###  Archivo de Picos (`union_peaks_file.tsv`)

Contiene información sobre las regiones de unión detectadas para los factores de transcripción. Las columnas más relevantes son:

-   `Dataset_Ids`: Identificadores de los experimentos.
    
-   `TF_name`: Nombre del factor de transcripción.
    
-   `Peak_start`: Posición inicial del sitio de unión.
    
-   `Peak_end`: Posición final del sitio de unión.
    
-   `Peak_center`: Centro del pico.
    
-   `Peak_number`: Identificador numérico del pico.
    
-   `Max_Fold_Enrichment`: Enriquecimiento máximo observado.
    
-   `Max_Norm_Fold_Enrichment`: Enriquecimiento normalizado.
    
-   `Proximal_genes`: Genes cercanos al sitio de unión.
    
-   `Center_position_type`: Tipo de posición del centro del pico (intergénica, intrónica, etc.).
    

### :alien: Archivo del Genoma (`E_coli_k12_MG16655_U00096.3`)

Archivo en formato FASTA que contiene la secuencia completa del genoma de _E. coli_.

## Objetivos del Proyecto

### :scream_cat:  Generación de Archivos FASTA

Desarrollar un programa que extraiga las secuencias de ADN correspondientes a los sitios de unión de cada TF, y genere un archivo FASTA independiente para cada uno de ellos.


## Plan de Implementación

1.  **Desarrollo del Extractor de Secuencias**  
    Programación de los módulos en Python para leer el genoma, procesar el archivo de picos, agrupar las coordenadas por TF y generar los archivos FASTA.
    
2.  **Integración y Pruebas**  
    Verificación del funcionamiento de todos los módulos, control de errores, y validación de resultados en ejemplos reales.
    
3.  **Documentación y Preparación para Despliegue**  
    Creación de esta documentación y preparación del entorno para facilitar el uso del programa en cualquier computadora mediante línea de comandos.
    

## Buenas Prácticas de Desarrollo  :heart_eyes_cat:

El proyecto se desarrolló siguiendo las siguientes buenas prácticas:

-   **Estructura Modular**: El código se organizó en módulos independientes (`main.py`, `genome.py`, `peaks.py`, `io_utils.py`) para facilitar el mantenimiento y la comprensión.
    
-   **Control de Versiones**: Uso de Git para gestionar los cambios en el desarrollo del proyecto.
    
-   **Documentación Clara**: Comentarios y nombres descriptivos en el código, además de este README explicativo.
    
-   **Manejo de Errores**: Validación de entradas, corrección automática de coordenadas invertidas, y registro de errores en archivos de log.
    

## Resultados

Se generaron archivos FASTA individuales para cada uno de los 144 factores de transcripción. Cada archivo contiene las secuencias correspondientes a los sitios de unión identificados por ChIP-seq, extraídas directamente del genoma. Los archivos están organizados automáticamente en un directorio de salida especificado por el usuario. :trollface:

