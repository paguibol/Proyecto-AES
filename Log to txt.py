from time import sleep
from datetime import datetime
import zipfile
import uiautomator2 as u2
import os
import subprocess
import shutil
from common import adb

IMPORT_FOLDER = os.path.join("logs", "imported")
NETWORK_FOLDERS = {
    "3G": os.path.join("logs", "3G"),
    "4G": os.path.join("logs", "4G"),
}
NETWORK_KEYWORDS = {"3G", "4G"}


def ensure_log_folders():
    os.makedirs(IMPORT_FOLDER, exist_ok=True)
    for folder in NETWORK_FOLDERS.values():
        os.makedirs(folder, exist_ok=True)


def detect_network_type(name):
    normalized_name = name.lower()
    for network_type in NETWORK_KEYWORDS:
        if network_type.lower() in normalized_name:
            return network_type
    return None


def move_to_network_folder(source_path, network_type):
    destination_folder = NETWORK_FOLDERS[network_type]
    destination_path = os.path.join(destination_folder, os.path.basename(source_path))
    if os.path.exists(destination_path):
        name, extension = os.path.splitext(os.path.basename(source_path))
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        destination_path = os.path.join(destination_folder, f"{name}_{timestamp}{extension}")
    shutil.move(source_path, destination_path)
    print(f"Moved to {network_type}: {os.path.basename(destination_path)}")


def organize_logs():
    for item in os.listdir(IMPORT_FOLDER):
        source_path = os.path.join(IMPORT_FOLDER, item)
        network_type = detect_network_type(item)
        if not network_type:
            print(f"Unclassified item left in imported: {item}")
            continue
        move_to_network_folder(source_path, network_type)


def extract_zip():
    device_name = adb("shell getprop ro.product.model")
    ensure_log_folders()
    print(f"Extracting logs from: {device_name}")
    remote_paths = ["/sdcard/bbklog_zip/."]
    for remote_path in remote_paths:
        extract = subprocess.run(
            ["adb", "pull", remote_path, IMPORT_FOLDER],
            capture_output=True,
            text=True,
        )
        if extract.returncode == 0:
            print(f"Logs extracted successfully from: {remote_path}")
            if extract.stdout:
                print(extract.stdout.strip())
            return
    print("Failed to extract logs.")
    if extract.stderr:
        print(extract.stderr.strip())


def unzip_logs():
    for netwerk_folder in NETWORK_FOLDERS.values():
        for item in os.listdir(netwerk_folder):
            if item.endswith(".zip"):
                zip_path = os.path.join(netwerk_folder, item)
                try:
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(netwerk_folder)
                    print(f"Extracted: {zip_path}")
                except Exception as e:
                    print(f"Error extracting {zip_path}: {e}")

def main():
    extract_zip()
    sleep(120)
    organize_logs()
    sleep(30)  
    unzip_logs()


if __name__ == "__main__":
    main()