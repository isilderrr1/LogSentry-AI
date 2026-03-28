Read this in: [English](README.md) | [Italiano](README_IT.md)

# 🛡️ LogSentry AI - Hybrid Local Intelligence Log Analyzer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code style: rich](https://img.shields.io/badge/code%20style-rich-magenta.svg)](https://github.com/Textualize/rich)

**LogSentry AI** is a privacy-first, hybrid cybersecurity tool designed for local security auditing. It seamlessly integrates a blazing-fast deterministic Regex scoring engine with an advanced Local Large Language Model (e.g., DeepSeek-R1 via LM Studio) to identify anomalies, phishing attempts, and malicious payloads. Built on a **Zero-Trust Privacy Architecture**, all analysis occurs directly on your machine. No data leaves your network!

---

## 🔒 Core Value
- **Zero Data Leakage**: All analysis runs 100% locally. You can confidently audit sensitive production logs or emails without risking data leaks to external APIs or third-party cloud models.
- **Hybrid Local Intelligence**: Why rely solely on computationally expensive LLMs or rigid static rules? LogSentry utilizes a two-tier approach. A deterministic Heuristic Engine quickly filters the noise, and a powerful local LLM provides Semantic Triage only for high-risk anomalies.

## 🚀 Performance & Efficiency (Benchmark)
LogSentry AI is designed to save massive amounts of computational resources compared to full-AI analysis pipelines. In our latest test benchmarks:
- **Regex Throughput**: ~60,000 logs/sec (High-speed pre-filtering).
- **AI Filtering Efficiency**: **97.0%** (Only 3% of logs required expensive LLM inference).
- **Avg AI Latency**: ~26s per request (Using DeepSeek-R1 local inference).

*Result: This hybrid approach saves 97% of computational resources compared to full-AI analysis.*

## ⚙️ Technical Maturity & Engineering
- **Configuration**: Environment-based setup (`.env`) for seamless multi-stage deployment.
- **Resiliency**: Graceful degradation logic ensures the tool remains fully functional for Regex processing even if the local AI server is offline.
- **Data Standards**: SOC-ready schema output natively including `severity`, `confidence_score`, and `mitre_technique_placeholder`.
- **Outputs**: Dual-format export providing a structured data-only `.csv` alongside a telemetry `benchmark_stats.json` file.

---

## 🔄 Workflow
1. **Deterministic Signature Matching**: Ingests massive `.csv` or `.txt` sets. Scans lines against established attack signatures like SQLi, Path Traversal, obfuscated Base64, and XSS.
2. **Risk Scoring & Threshold Gating**: Each matched signature cumulatively builds a dynamic "Threat Score".
3. **Contextual Semantic Analysis (LLM Triage)**: If the Threat Score surpasses the safety threshold, the system dynamically routes the log to a local LLM API for a Model-generated security verdict, parsing the model's inner analysis securely.
4. **Performance Telemetry & Reporting**: Generates SOC-ready reports and benchmark summaries upon completion.

## ✨ Core Features
- **Interactive TUI**: An Analyst-optimized Terminal Interface for rapid audit, fully keyboard-navigable and powered by `rich` and `questionary`.
- **Bulk Pandas Processing**: Process massive log files seamlessly with real-time `tqdm` progress tracking.

## 📸 Screenshots
![Main Menu](menu_screenshot.png)
![Analysis Results](results_screenshot.png)

## 📋 Prerequisites
- **Python 3.10+**
- **LM Studio** (Running a local server model like DeepSeek-R1, Llama, or Qwen).

---

## 🛠 Installation

Ensure you have cloned or downloaded this repository.

### Clone the Repository
```bash
git clone git@github.com:isilderrr1/LogSentry-AI.git
cd LogSentry-AI
```

### Setup (Windows / macOS / Linux)
```bash
# 1. Create and activate a virtual environment
python -m venv venv
# Windows: .\venv\Scripts\Activate.ps1
# Mac/Linux: source venv/bin/activate

# 2. Install the application and dependencies
pip install -e .

# 3. Configure the Environment
cp .env.example .env
# Edit .env to set your LM_STUDIO_URL and LM_STUDIO_MODEL
```

---

## 💻 Usage

### 1. Analyst-Optimized TUI
To launch the interactive Terminal User Interface, simply run the global command from anywhere within the virtual environment:
```bash
logsentry
```

### 2. Legacy Scripting CLI
For CI/CD or lightweight automation scripting:
```bash
python -m src.cli.main analyze "GET /admin?user=root' OR 1=1--"
```

---

## ⚠️ Threat Model
LogSentry AI is designed as an asynchronous internal auditing tool used for batch forensic analysis of collected logs. It is **NOT** intended to be deployed as a real-time, inline Intrusion Detection System (IDS) or Intrusion Prevention System (IPS). It provides a second layer of triage for SOC analysts to rapidly filter noisy data asynchronously.

## 🚧 Technical Limitations
- **Model-dependent Accuracy**: The quality of the security verdicts is heavily dependent on the chosen local LLM; hallucinations or false positives may occur.
- **Hardware Bound Latency**: Local LLM inference is computationally expensive. Very large batches of high-threshold logs can result in significant processing delays dependent strictly on your local hardware specifications.
- **Context Window Constraints**: Ensure your local LLM configuration provides an adequate context window for large stack traces or dense log payloads.

## 📄 License
This project is licensed under the MIT License.
