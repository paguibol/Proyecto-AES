import os
import sys
import subprocess
from datetime import datetime


NETWORKS = {"1": "4G", "2": "3G"}
BALANCES = {"1": "Prepago", "2": "Pospago", "3": "Sin saldo"}
TESTS = {
    "1": "Run all",
    "2": "Internet",
    "3": "Messenger",
    "4": "MMS",
    "5": "Twitter",
    "6": "Youtube",
    "7": "Gmail"
}


def choose(prompt, options):
    print(prompt)
    for k, v in options.items():
        print(f" {k}) {v}")
    while True:
        sel = input("Selecciona: ").strip()
        if sel in options:
            return options[sel]
        print("Opción inválida. Intenta de nuevo.")


def build_filename(test, network, balance):
    return f"Proyecto_AES_{test} {network} {balance}.py"

def build_filename_all(network, balance):
    return f"run_all_AES {network} {balance}.py"

def main():
    print("=== Menú de pruebas AES ===")
    while True:
        network = choose("Elige la red:", NETWORKS)
        balance = choose("Elige tipo de saldo:", BALANCES)
        test = choose("Elige la prueba:", TESTS)

        if test == "Run all":
            run_filename = build_filename_all(network, balance)
            if not os.path.exists(run_filename):
                print(f"Archivo no encontrado: {run_filename}")
            else:
                print(f"Ejecutando: {run_filename}")
                try:
                    completed = subprocess.run([sys.executable, run_filename])
                    print(f"{run_filename} terminado con código: {completed.returncode}")
                except Exception as e:
                    print(f"Error al ejecutar {run_filename}: {e}")
        else:
            filename = build_filename(test, network, balance)
            if not os.path.exists(filename):
                print(f"Archivo no encontrado: {filename}")
            else:
                print(f"Lanzando: {filename}")
                try:
                    completed = subprocess.run([sys.executable, filename])
                    print(f"Terminado con código: {completed.returncode}")
                except Exception as e:
                    print(f"Error al ejecutar {filename}: {e}")

        again = input("Volver al menú? (s/n): ").strip().lower()
        if again not in ("s", "si", "y", "yes"):
            print("Saliendo. Hasta luego.")
            break


if __name__ == "__main__":
    main()
