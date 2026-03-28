import pandas as pd
from tqdm import tqdm
import os
import datetime
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
    
    print(f"Starting bulk analysis of {len(logs)} log entries...")
    
    for log_entry in tqdm(logs, desc="Analyzing Logs", unit="log"):
        # 1. Regex Match
        regex_result = analyzer.analyze(log_entry)
        score = regex_result['score']
        matches = regex_result['matches']
        
        # 2. LLM Evaluation if needed
        llm_verdict = "N/A"
        if score >= threshold:
            llm_verdict = llm.evaluate_log(log_entry, score, matches)
            
        # Append to results
        results.append({
            "Log": log_entry,
            "Regex Score": score,
            "Signatures": ", ".join(matches) if matches else "None",
            "LLM Verdict": llm_verdict
        })
        
    # Compile the final report
    report_df = pd.DataFrame(results)
    
    try:
        report_df.to_csv(output_csv, index=False, encoding='utf-8')
        print(f"\nAnalysis complete! Audit report successfully saved to: {os.path.abspath(output_csv)}")
    except Exception as e:
        print(f"\nFailed to save output to {output_csv}. Error: {e}")
