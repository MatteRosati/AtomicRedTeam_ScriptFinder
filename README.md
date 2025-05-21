# 🔍 Atomic Red Team - Script Finder

Uno script Python per monitorare automaticamente i **nuovi test** nella repository ufficiale [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team), confrontarli con uno storico e salvare i risultati in un file Excel.

## ✅ Funzionalità principali

- Scarica e analizza i file YAML dei test Atomic Red Team.
- Estrae:
  - ID tecnica MITRE (es: `T1059.001`)
  - Numero e nome del test
  - Piattaforme supportate (`Windows`, `Linux`, `macOS`, etc.)
  - Executor (`cmd`, `powershell`, etc.)
- Registra solo i **nuovi test** trovati in un file di log.
- Aggiorna un file Excel (`atomic_tests.xlsx`) con tutti i test rilevati.

---

## 🛠️ Requisiti

- Windows con **Python 3.8+** installato  
  [Scarica Python per Windows](https://www.python.org/downloads/windows/)

---

## 📦 Installazione rapida (Windows)

1. **Scarica o clona questa repository**:

```bash
git clone https://github.com/MatteRosati/AtomicRedTeam_ScriptFinder.git
cd AtomicRedTeam_ScriptFinder
````

2. **Esegui il setup automatico** per creare un ambiente virtuale ed installare i pacchetti necessari:

```bat
.\environment_setup.bat
```

> Questo comando:
>
> * Crea un ambiente virtuale nella cartella `venv`
> * Installa i moduli: `pandas`, `pyyaml`, `requests`, `openpyxl`
> * Ti mostra come avviare lo script

---

## 🚀 Esecuzione dello script

Una volta creato l'ambiente, puoi **lanciare lo script** premendo semplicemente **invio**.
All'antivirus non piacerà affatto.

---

## 📁 File generati

| Nome file           | Descrizione                                           |
| ------------------- | ----------------------------------------------------- |
| `atomic_tests.xlsx` | File Excel contenente tutti i test trovati            |
| `nuovi_test.log`    | Log dei test nuovi trovati rispetto al run precedente |

> Alla prima esecuzione, tutti i test trovati verranno considerati "nuovi" se non si importa l'Excel contenuto nella repo, aggiornato al **20.5.2025**.

---

## 🧰 Moduli Python usati

* `pandas`
* `pyyaml`
* `requests`
* `openpyxl`

Questi vengono installati automaticamente da `environment_setup.bat`.

---

## 🧠 Note

* Lo script scarica ad ogni esecuzione la versione più recente della repo Atomic Red Team.
* Il confronto avviene su base **completa**: ogni test è identificato da tecnica, numero, nome, piattaforma ed executor.

---

## 🧠 Conclusione

* Di volta in volta che viene eseguito, prima di lanciare lo script, scaricare la repository coi file da qui. **si raccomanda di pulire TUTTI i file che vengono creati nella cartella venv (ambiente virtuale creato per l'esecuzione) prima di inserire i file aggiornati su GitHub.**

---