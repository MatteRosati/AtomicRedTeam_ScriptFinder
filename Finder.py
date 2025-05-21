import os
import shutil
import requests
import zipfile
import tempfile
import yaml
import pandas as pd
from pathlib import Path
from datetime import datetime

# Configurazioni
GITHUB_REPO_ZIP = "https://github.com/redcanaryco/atomic-red-team/archive/refs/heads/master.zip"
EXCEL_FILE = "atomic_tests.xlsx"
LOG_FILE = f"nuovi_test_{datetime.now().strftime('%Y-%m-%d')}.log"

def download_and_extract_repo():
    tmp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(tmp_dir, "repo.zip")
    print("[+] Scaricamento della repository...")

    try:
        response = requests.get(GITHUB_REPO_ZIP, timeout=30)
        response.raise_for_status()
        with open(zip_path, "wb") as f:
            f.write(response.content)
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"[!] Errore durante il download della repository: {e}")

    print("[+] Estrazione archivio...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(tmp_dir)
    except zipfile.BadZipFile as e:
        raise RuntimeError(f"[!] Archivio ZIP corrotto o non valido: {e}")

    repo_path = os.path.join(tmp_dir, "atomic-red-team-master", "atomics")
    return repo_path, tmp_dir

def parse_atomic_tests(atomics_dir):
    data = []
    print("[+] Parsing dei file YAML...")
    for technique_dir in Path(atomics_dir).iterdir():
        yaml_file = technique_dir / f"{technique_dir.name}.yaml"
        if yaml_file.exists():
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    content = yaml.safe_load(f)
                    technique = content.get("attack_technique", technique_dir.name)
                    tests = content.get("atomic_tests", [])
                    for idx, test in enumerate(tests, 1):
                        data.append({
                            "Technique": technique,
                            "TestNumber": idx,
                            "TestName": test.get("name", "Unknown"),
                            "Platforms": ", ".join(test.get("supported_platforms", [])),
                            "Executor": test.get("executor", {}).get("name", "N/A")
                        })
            except Exception as e:
                print(f"[!] Errore durante il parsing di {yaml_file.name}: {e}")
    return pd.DataFrame(data)

def load_existing_tests():
    if os.path.exists(EXCEL_FILE):
        try:
            return pd.read_excel(EXCEL_FILE)
        except Exception as e:
            print(f"[!] Errore durante la lettura dell'Excel esistente: {e}")
            return pd.DataFrame(columns=["Technique", "TestNumber", "TestName", "Platforms", "Executor"])
    return pd.DataFrame(columns=["Technique", "TestNumber", "TestName", "Platforms", "Executor"])

def log_new_tests(new_tests_df):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not new_tests_df.empty:
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as log:
                log.write(f"\n=== Nuovi test trovati ({len(new_tests_df)}) - {timestamp} ===\n")
                for _, row in new_tests_df.iterrows():
                    log.write(
                        f"{row['Technique']} - Test {row['TestNumber']}: {row['TestName']} "
                        f"(Platforms: {row['Platforms']}, Executor: {row['Executor']})\n"
                    )
            print(f"[+] {len(new_tests_df)} nuovi test loggati in '{LOG_FILE}'")
        except Exception as e:
            print(f"[!] Errore durante la scrittura nel log file: {e}")
    else:
        print("[+] Nessun nuovo test trovato.")

def save_excel(dataframe):
    try:
        dataframe.to_excel(EXCEL_FILE, index=False)
        print(f"[+] File Excel aggiornato: {EXCEL_FILE}")
    except Exception as e:
        print(f"[!] Errore durante il salvataggio dell'Excel: {e}")

def main():
    try:
        atomics_path, temp_dir = download_and_extract_repo()
        new_data = parse_atomic_tests(atomics_path)
        old_data = load_existing_tests()

        merged = new_data.merge(
            old_data,
            on=["Technique", "TestNumber", "TestName", "Platforms", "Executor"],
            how='left',
            indicator=True
        )
        new_tests = merged[merged["_merge"] == "left_only"].drop(columns=["_merge"])

        log_new_tests(new_tests)
        save_excel(new_data)

    except Exception as e:
        print(f"[!] Errore critico: {e}")
    finally:
        if 'temp_dir' in locals():
            shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    main()
