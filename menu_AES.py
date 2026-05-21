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


def run_all(log_dir_base="logs"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = os.path.join(log_dir_base, f"run_all_{timestamp}")
    os.makedirs(out_dir, exist_ok=True)

    tests = [t for t in TESTS.values() if t != "Run all"]
    results = []
    for network in NETWORKS.values():
        for balance in BALANCES.values():
            for test in tests:
                filename = build_filename(test, network, balance)
                safe_name = filename.replace(" ", "_")
                log_path = os.path.join(out_dir, f"{safe_name}.log")
                if not os.path.exists(filename):
                    results.append((filename, None, "missing"))
                    with open(log_path, "w", encoding="utf-8") as f:
                        f.write(f"Archivo no encontrado: {filename}\n")
                    continue

                with open(log_path, "w", encoding="utf-8") as f:
                    f.write(f"=== Ejecutando: {filename} ===\n")
                    try:
                        completed = subprocess.run([sys.executable, filename], stdout=f, stderr=subprocess.STDOUT)
                        results.append((filename, completed.returncode, "ok"))
                    except Exception as e:
                        f.write(f"Error al ejecutar: {e}\n")
                        results.append((filename, None, "error"))

    summary_path = os.path.join(out_dir, "summary.txt")
    with open(summary_path, "w", encoding="utf-8") as s:
        s.write(f"Run all resumen - {timestamp}\n")
        for fn, code, status in results:
            s.write(f"{status}\t{code}\t{fn}\n")

    print(f"Run all completado. Logs en: {out_dir}")
    print(f"Resumen guardado en: {summary_path}")


def main():
    print("=== Menú de pruebas AES ===")
    while True:
        network = choose("Elige la red:", NETWORKS)
        balance = choose("Elige tipo de saldo:", BALANCES)
        test = choose("Elige la prueba:", TESTS)

        if test == "Run all":
            for bal in BALANCES.values():
                run_filename = f"run_all_AES {network} {bal}.py"
                if not os.path.exists(run_filename):
                    print(f"Archivo no encontrado: {run_filename}")
                    continue
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
