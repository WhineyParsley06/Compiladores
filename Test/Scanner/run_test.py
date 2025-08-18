import subprocess
import os
import sys

# Ruta a tu script y carpeta de pruebas. Ejecutar desde carpeta raiz
BMINOR_SCRIPT = 'bminor.py'
TEST_FOLDER = os.path.join('test', 'scanner')

# Diccionario: nombre del archivo -> salida esperada
test_cases = {
    'good0.bminor': 0,
    'good1.bminor': 0,
    'good2.bminor': 0,
    'good3.bminor': 0,
    'good4.bminor': 0,
    'good5.bminor': 0,
    'good6.bminor': 0,
    'good7.bminor': 0,
    'good8.bminor': 0,
    'good9.bminor': 0,
    'bad0.bminor': 0,
    'bad1.bminor': 0,
    'bad2.bminor': 0,
    'bad3.bminor': 0,
    'bad4.bminor': 0,
    'bad5.bminor': 0,
    'bad6.bminor': 0,
    'bad7.bminor': 0,
    'bad8.bminor': 0,
    'bad9.bminor': 0,
}

print("=== Ejecutando pruebas ===\n")
for file_name, expected_exit in test_cases.items():
    path = os.path.join(TEST_FOLDER, file_name)
    result = subprocess.run(['python', BMINOR_SCRIPT, '--scan', path], stdout=sys.stdout,stderr=sys.stderr,text=True)
    actual_exit = result.returncode

    status = 'OK' if actual_exit == expected_exit else 'ERROR'
    print(f"\n{file_name}: esperado={expected_exit}, obtenido={actual_exit} → {status}\n")