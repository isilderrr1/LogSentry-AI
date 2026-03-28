Read this in: [English](README.md) | [Italiano](README_IT.md)

# 🛡️ LogSentry AI - Analizzatore Locale Intelligente di Log

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code style: rich](https://img.shields.io/badge/code%20style-rich-magenta.svg)](https://github.com/Textualize/rich)

**LogSentry AI** è uno strumento di sicurezza informatica ibrido, focalizzato sulla privacy e progettato per l'auditing locale. Integra un velocissimo motore di punteggio Regex con un avanzato Local Large Language Model (es. DeepSeek-R1 tramite LM Studio) per identificare anomalie, tentativi di phishing e payload malevoli direttamente sulla tua macchina. Nessun dato lascia mai la tua rete!

---

## 🔒 Perché LogSentry AI?
- **Zero Data Leakage** (Nessuna Perdita di Dati): Tutta l'analisi viene eseguita al 100% in locale sulla tua macchina. Puoi esaminare log di produzione o e-mail sensibili con sicurezza, senza rischiare fughe di dati verso API esterne o modelli cloud di terze parti.
- **Architettura Ibrida**: Perché affidarsi esclusivamente alle allucinazioni dell'IA o a rigide regole statiche? LogSentry utilizza un approccio a due livelli: un motore Regex deterministico filtra rapidamente il rumore, mentre un potente LLM locale in grado di ragionare (come DeepSeek-R1) offre un'analisi profonda e contestuale solo per le anomalie ad alto rischio.

## ⚙️ Flusso di Lavoro (Workflow)
1. **Filtro Regex**: Ingerisce massicci file in formato `.csv` o `.txt`. Scansiona le righe per identificare firme di attacco consolidate (SQLi, Path Traversal, Base64 offuscato, XSS).
2. **Punteggio di Rischio (Risk Scoring)**: Ogni firma rilevata incrementa cumulativamente il "Threat Score" dinamico.
3. **Ragionamento DeepSeek**: Se il Threat Score supera la soglia di sicurezza (default: 50), il sistema inoltra dinamicamente il log all'API del LLM locale per un verdetto avanzato di sicurezza informatica, decodificando in modo sicuro anche il ragionamento interno del modello.

## ✨ Funzionalità Principali
- **TUI Interattiva**: Una bellissima interfaccia utente su terminale (TUI), navigabile tramite frecce direzionali, supportata da `rich` e `questionary`.
- **Elaborazione Massiva con Pandas**: Processa file di log pesanti in modo ottimale con la barra di progresso in tempo reale di `tqdm`.
- **Reportistica con Timestamp**: Genera automaticamente file `audit_report_YYYYMMDD_HHMMSS.csv` sicuri e cronologicamente tracciati, contenenti i verdetti puliti e le istruzioni di risposta agli incidenti forniti dall'IA.

## 📸 Screenshot
![Menu Principale](menu_screenshot.png)
![Risultati Analisi](results_screenshot.png)

## 📋 Prerequisiti
- **Python 3.10+**
- **LM Studio** (Server locale in esecuzione con modelli come DeepSeek-R1, Llama o Qwen).

---

## 🚀 Installazione

Assicurati di aver clonato o scaricato questo repository. Quindi, imposta l'ambiente in base al tuo Sistema Operativo:

### Clona il Repository
```bash
git clone git@github.com:isilderrr1/LogSentry-AI.git
cd LogSentry-AI
```

### Windows
```powershell
# 1. Crea un ambiente virtuale
python -m venv venv

# 2. Attiva l'ambiente
.\venv\Scripts\Activate.ps1

# 3. Installa l'applicazione e le dipendenze
pip install -e .
```

### macOS / Linux
```bash
# 1. Crea un ambiente virtuale
python3 -m venv venv

# 2. Attiva l'ambiente
source venv/bin/activate

# 3. Installa l'applicazione e le dipendenze
pip install -e .
```

---

## 💻 Utilizzo

### 1. TUI Interattiva
Per lanciare l'elegante Terminal User Interface (TUI), esegui semplicemente il comando globale da qualsiasi punto all'interno dell'ambiente virtuale:
```bash
logsentry
```

### 2. CLI globale per l'automazione
Per pipeline CI/CD o per automazioni tramite script senza l'ausilio di interfacce interattive, puoi utilizzare il comando legacy diretto al core processor Python:
```bash
python -m src.cli.main analyze "GET /admin?user=root' OR 1=1--"
```

---

## 🧠 Configurazione Intelligenza Artificiale (LM Studio)
Per configurare il collegamento alla tua IA locale:
1. Apri **LM Studio** e avvia il server locale di inferenza.
2. Il codice punta di default a `http://10.5.0.2:1234/v1` (se il tuo LM Studio opera esclusivamente su localhost, ricordati di modificare l'IP in `src/core/llm_analyzer.py` su `http://localhost:1234/v1`).
3. Aggiorna la stringa identificativa `model` all'interno di `src/core/llm_analyzer.py` in modo che corrisponda al nome esatto del modello che hai caricato in run-time (es. `deepseek-r1-distill-qwen-14b`).

## 📄 Licenza
Questo progetto è distribuito sotto licenza MIT.
