Read this in: [English](README.md) | [Italiano](README_IT.md)

# 🛡️ LogSentry AI - Analizzatore Locale Intelligente Ibrido

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code style: rich](https://img.shields.io/badge/code%20style-rich-magenta.svg)](https://github.com/Textualize/rich)

**LogSentry AI** è uno strumento di sicurezza informatica ibrido, focalizzato sulla privacy e progettato per l'auditing locale. Integra un velocissimo motore deterministico Regex con un avanzato Local Large Language Model (es. DeepSeek-R1 tramite LM Studio) per identificare anomalie, tentativi di phishing e payload malevoli. Basato su un'architettura **Zero-Trust Privacy**, tutta l'analisi avviene direttamente sulla tua macchina. Nessun dato lascia la tua rete!

---

## 🔒 Valore Fondamentale
- **Zero Data Leakage** (Nessuna Perdita di Dati): Tutta l'analisi viene eseguita al 100% in locale. Puoi esaminare log di produzione o e-mail sensibili con sicurezza, senza rischiare fughe di dati verso API esterne.
- **Intelligenza Locale Ibrida**: Perché affidarsi esclusivamente ai costosi LLM o a rigide regole statiche? LogSentry utilizza un approccio a due livelli. Un motore euristico deterministico filtra rapidamente il rumore, mentre un potente LLM locale offre un Triage Semantico solo per le anomalie ad alto rischio.

## 🚀 Prestazioni ed Efficienza (Benchmark)
LogSentry AI è progettato per risparmiare enormi quantità di risorse computazionali rispetto alle pipeline di analisi esclusivamente IA. Nei nostri test di benchmark più recenti:
- **Throughput Regex**: ~60.000 log/sec (Pre-filtraggio ad alta velocità).
- **Efficienza di Filtraggio IA**: **97,0%** (Solo il 3% dei log ha richiesto la costosa inferenza del LLM).
- **Latenza IA Media**: ~26s per richiesta (Utilizzando l'inferenza locale di DeepSeek-R1).

*Risultato: Questo approccio ibrido risparmia il 97% delle risorse computazionali rispetto a un'analisi interamente basata sull'IA.*

## ⚙️ Maturità Tecnica e Ingegnerizzazione
- **Configurazione**: Setup basato sull'ambiente (`.env`) per un deployment multi-stadio fluido.
- **Resilienza**: Una logica di degradazione controllata (Graceful Degradation) garantisce che lo strumento rimanga completamente operativo per l'elaborazione Regex anche se il server IA locale è offline.
- **Standard Dati**: Output con schema pronto per il SOC, che include nativamente `severity`, `confidence_score` e `mitre_technique_placeholder`.
- **Output Multipli**: Esportazione in doppio formato che fornisce un `.csv` strutturato di soli dati affiancato a un file di telemetria `benchmark_stats.json`.

---

## 🔄 Flusso di Lavoro (Workflow)
1. **Corrispondenza Deterministica delle Firme (Signature Matching)**: Ingerisce massicci file in formato `.csv` o `.txt`. Scansiona le righe per identificare firme di attacco consolidate (SQLi, Path Traversal, Base64 offuscato, XSS).
2. **Scoring del Rischio e Filtraggio tramite Soglia**: Ogni firma rilevata incrementa cumulativamente il "Threat Score" dinamico.
3. **Analisi Semantica Contestuale (Triage LLM)**: Se il Threat Score supera la soglia di sicurezza, il sistema inoltra dinamicamente il log all'API del LLM locale per un verdetto di sicurezza generato dal modello, decodificando l'analisi interna.
4. **Telemetria delle Prestazioni e Reportistica**: Genera report pronti per il livello SOC e riepiloghi di benchmark al completamento.

## ✨ Funzionalità Principali
- **TUI Interattiva**: Un'Interfaccia per Terminale ottimizzata per gli analisti per audit rapidi, navigabile tramite frecce direzionali, supportata da `rich` e `questionary`.
- **Elaborazione Massiva con Pandas**: Processa file di log pesanti in modo ottimale con la barra di progresso in tempo reale di `tqdm`.

## 📸 Screenshot
![Menu Principale](menu_screenshot.png)
![Risultati Analisi](results_screenshot.png)

## 📋 Prerequisiti
- **Python 3.10+**
- **LM Studio** (Server locale in esecuzione con modelli come DeepSeek-R1, Llama o Qwen).

---

## 🛠 Installazione

Assicurati di aver clonato o scaricato questo repository.

### Clona il Repository
```bash
git clone git@github.com:isilderrr1/LogSentry-AI.git
cd LogSentry-AI
```

### Setup (Windows / macOS / Linux)
```bash
# 1. Crea e attiva un ambiente virtuale
python -m venv venv
# Windows: .\venv\Scripts\Activate.ps1
# Mac/Linux: source venv/bin/activate

# 2. Installa l'applicazione e le dipendenze
pip install -e .

# 3. Configura l'Ambiente
cp .env.example .env
# Modifica .env per inserire LM_STUDIO_URL e LM_STUDIO_MODEL
```

---

## 💻 Utilizzo

### 1. TUI Ottimizzata per Analisti
Per lanciare l'Interfaccia per Terminale, esegui il comando globale dall'interno dell'ambiente virtuale:
```bash
logsentry
```

### 2. CLI globale per l'automazione
Per pipeline CI/CD o per automazioni tramite script:
```bash
python -m src.cli.main analyze "GET /admin?user=root' OR 1=1--"
```

---

## ⚠️ Threat Model
LogSentry AI è progettato come strumento di auditing asincrono interno per l'analisi forense in batch dei log raccolti. **NON** è destinato a essere distribuito come Intrusion Detection System (IDS) o Intrusion Prevention System (IPS) in linea e in tempo reale. Fornisce un secondo livello di triage per analisti SOC per filtrare rapidamente rumore e dati in modo asincrono.

## 🚧 Limitazioni Tecniche
- **Accuratezza Dipendente dal Modello**: La qualità dei verdetti di sicurezza dipende fortemente dal server LLM locale scelto; possono verificarsi allucinazioni o falsi positivi.
- **Latenza Legata all'Hardware**: L'inferenza del LLM locale è computazionalmente costosa. Lotti molto grandi di log ad alto rischio comportano ritardi di elaborazione che dipendono strettamente dalle specifiche del tuo hardware locale.
- **Limiti della Finestra di Contesto**: Assicurati che il tuo LLM locale abbia una finestra di contesto adeguata per analizzare stack trace ampi o payload densi.

## 📄 Licenza
Questo progetto è distribuito sotto licenza MIT.
