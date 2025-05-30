
##  Casos de Prueba para el Módulo: Extractor y Creador de Secuencias FASTA

###  **1. Archivo del genoma no se encuentra**

* **Entradas:**

  * `--genome` apunta a un archivo inexistente.
  * `--peaks` es válido.
  * Directorio de salida cualquiera.

```bash
python main.py --genome NO_EXISTE.fasta --peaks data/union_peaks_file.tsv --output output/
```

* **Esperado:**

  ```
  Error: El archivo NO_EXISTE.fasta no se encuentra.
  Error. No se pudo leer el genoma. Saliendo.
  ```


###  **2. Archivo de picos vacío**

* **Entradas:**

  * Archivo FASTA válido.
  * Archivo de picos vacío (`touch data/empty_peaks.tsv`)
  * Directorio de salida cualquiera.

```bash
python main.py --genome data/E_coli_K12_MG1655_U00096.3.txt --peaks data/empty_peaks.tsv --output output/
```

* **Esperado:**

  ```
  No se encontraron picos válidos. Saliendo.
  ```

* **Opcionalmente**, se puede validar que:

  * `log_errores_peaks.txt` esté vacío o contenga "encabezado omitido" y nada más.



###  **3. Coordenadas fuera de rango del genoma**

* **Entradas:**

  * Archivo FASTA válido.
  * Archivo de picos con `end` mayor al largo del genoma (`> 4641652`).
  * Directorio de salida válido.

```bash
python main.py --genome data/E_coli_K12_MG1655_U00096.3.txt --peaks data/peaks_fuera_de_rango.tsv --output output/
```

* **Esperado:**

  ```
   Se encontraron advertencias en log_errores_extraccion.txt:
  Línea 1: Advertencia: Coordenadas fuera de rango para TF_X (start=..., end=...)
  ...
  ```

* **Validar:**

  * Archivo `log_errores_extraccion.txt` debe contener las advertencias.
  * Archivos `.fasta` válidos solo para picos correctos.

---

###  **4. Directorio de salida no existe**

* **Entradas:**

  * Archivos válidos.
  * Directorio `output_nuevo/` no existe aún.

```bash
python main.py --genome data/E_coli_K12_MG1655_U00096.3.txt --peaks data/union_peaks_file.tsv --output output_nuevo/
```

* **Esperado:**
```
No se registraron errores en log_errores_peaks.txt.
No se registraron errores en log_errores_extraccion.txt.
  Proceso completado. Las secuencias FASTA están en output_nuevo
  ```

* **Validar:**

  * El directorio `output_nuevo/` fue creado.
  * Contiene `.fasta` y `.txt` según los resultados.

