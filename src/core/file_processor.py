import pandas as pd
from tqdm import tqdm
import os
import datetime
import time
import json
from rich.console import Console
from rich.table import Table
from src.core.regex_engine import RegexAnalyzer
from src.core.llm_analyzer import LocalLLMAnalyzer

def process_log_file(file_path: str, threshold: int, output_csv: str = None):
    """
    Reads a CSV or text file using pandas, runs regex analysis line by line, 
    evaluates high-score entries via LLM, and saves the output to a CSV.
    """
    if not output_csv:
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        output_csv = f"audit_report_{timestamp}.csv"

    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    # Determine file type and load into a pandas DataFrame
    if file_path.lower().endswith('.csv'):
        try:
            df = pd.read_csv(file_path)
            # Find the target column
            target_col = None
            for col in df.columns:
                if col.lower() in ['log', 'message']:
                    target_col = col
                    break
            
            # Fallback to the first column if no 'log' or 'message' is found
            if not target_col and len(df.columns) > 0:
                target_col = df.columns[0]
                
            if not target_col:
                print("Error: CSV file is empty or has no columns.")
                return
                
            logs = df[target_col].astype(str).tolist()
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return
    else:
        # Assume it's a raw text or log file
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                logs = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"Error reading text file: {e}")
            return

    if not logs:
        print("No logs found in the provided file.")
        return

    analyzer = RegexAnalyzer()
    
    # We only initialize the LLM Analyzer if there's at least one high-score entry,
    # but for simplicity, we can initialize it right away.
    llm = LocalLLMAnalyzer()
    
    results = []
    
    # Benchmarking Variables
    total_regex_time = 0.0
    total_ai_time = 0.0
    ai_request_count = 0
    total_logs = len(logs)
    
    print(f"Starting bulk analysis of {total_logs} log entries...")
    
    start_total_time = time.perf_counter()
    
    for log_entry in tqdm(logs, desc="Analyzing Logs", unit="log"):
        # 1. Regex Match
        regex_start = time.perf_counter()
        regex_result = analyzer.analyze(log_entry)
        regex_time = time.perf_counter() - regex_start
        total_regex_time += regex_time
        
        score = regex_result['score']
        matches = regex_result['matches']
        
        # 2. LLM Evaluation if needed
        llm_verdict = "N/A"
        if score >= threshold:
            ai_start = time.perf_counter()
            llm_verdict = llm.evaluate_log(log_entry, score, matches)
            ai_time = time.perf_counter() - ai_start
            total_ai_time += ai_time
            ai_request_count += 1
            
        # Append to results
        results.append({
            "log_entry": log_entry,
            "severity": "HIGH" if score >= threshold else "LOW",
            "confidence_score": score,
            "matched_signatures": ", ".join(matches) if matches else "None",
            "mitre_technique_placeholder": "TBD",
            "llm_verdict": llm_verdict
        })
        
    end_total_time = time.perf_counter()
    total_execution_time = end_total_time - start_total_time
    
    # Calculate Metrics
    regex_throughput = (total_logs / total_regex_time) if total_regex_time > 0 else 0
    ai_filtering_efficiency = ((total_logs - ai_request_count) / total_logs * 100) if total_logs > 0 else 0
    average_ai_latency = (total_ai_time / ai_request_count) if ai_request_count > 0 else 0
    
    # --- Visual Reporting ---
    console = Console()
    print()  # Empty line for UI polish after tqdm
    table = Table(title="LogSentry Performance Metrics", style="cyan", title_style="bold magenta")
    table.add_column("Metric", style="bold green", no_wrap=True)
    table.add_column("Value", style="bold yellow")
    
    table.add_row("Total Logs Processed", str(total_logs))
    table.add_row("Total Execution Time", f"{total_execution_time:.2f}s")
    table.add_row("Regex Throughput", f"{regex_throughput:.2f} logs/sec")
    table.add_row("AI Filtering Efficiency", f"{ai_filtering_efficiency:.2f}%")
    table.add_row("Average AI Latency", f"{average_ai_latency:.2f}s/req")
    
    console.print(table)
    print()
    
    # --- Professional Metadata Storage (JSON) ---
    stats_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "total_logs": total_logs,
        "total_execution_time_s": round(total_execution_time, 4),
        "regex_throughput_logs_per_s": round(regex_throughput, 2),
        "ai_filtering_efficiency_pct": round(ai_filtering_efficiency, 2),
        "average_ai_latency_s": round(average_ai_latency, 4),
        "ai_requests_made": ai_request_count
    }
    
    try:
        with open("benchmark_stats.json", "w", encoding="utf-8") as f:
            json.dump(stats_data, f, indent=4)
    except Exception as e:
        console.print(f"[bold red]Warning: Failed to save benchmark_stats.json: {e}[/bold red]")
        
    # Compile the final report
    report_df = pd.DataFrame(results)
    
    try:
        report_df.to_csv(output_csv, index=False, encoding='utf-8')
        print(f"Analysis complete! Audit report successfully saved to: {os.path.abspath(output_csv)}")
    except Exception as e:
        print(f"Failed to save output to {output_csv}. Error: {e}")
