import os
import subprocess

# Lista de pruebas funcionales: (nombre, genome, peaks, output)
tests = [
    ("genoma_no_existe", "test/data_test/NO_EXISTE.fasta", "data/union_peaks_file.tsv"),
    ("picos_vacios", "data/E_coli_K12_MG1655_U00096.3.txt", "test/data_test/empty_peaks.tsv"),
    ("peaks_fuera_rango", "data/E_coli_K12_MG1655_U00096.3.txt", "test/data_test/picos_invertidos.tsv"),
    ("directorio_creado_auto", "data/E_coli_K12_MG1655_U00096.3.txt", "data/union_peaks_file.tsv"),
    ("picos_no_numericos", "data/E_coli_K12_MG1655_U00096.3.txt", "test/data_test/picos_no_numericos.tsv"),
    ("picos_incompletos", "data/E_coli_K12_MG1655_U00096.3.txt", "test/data_test/picos_incompleto.tsv"),
    ("picos_invertidos", "data/E_coli_K12_MG1655_U00096.3.txt", "test/data_test/picos_invertidos.tsv"),
    ("genoma_sin_encabezado", "test/data_test/fasta_sin_encabezado.txt", "data/union_peaks_file.tsv"),
    ("genoma_vacio", "test/data_test/fasta_sin_secuencia.txt", "data/union_peaks_file.tsv"),
    ("genoma_caracteres_invalidos", "test/data_test/fasta_con_caracteres_invalidos.txt", "data/union_peaks_file.tsv"),
    ("genoma_varios_encabezados", "test/data_test/fasta_con_dos_encabezados.txt", "data/union_peaks_file.tsv")
]

def run_test(name, genome, peaks):
    output = f"test/{name}"
    print(f" Ejecutando: {name}")
    os.makedirs(output, exist_ok=True)
    result = subprocess.run([
        "python", "main.py",
        "--genome", genome,
        "--peaks", peaks,
        "--output", output
    ], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("⚠️ STDERR:", result.stderr)
    print("="*60)

if __name__ == "__main__":
    for test_name, genome_path, peaks_path in tests:
        run_test(test_name, genome_path, peaks_path)
