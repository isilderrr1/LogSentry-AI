import sys
import os
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint
from rich.table import Table
from rich.align import Align

# Ensure root folder is added to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.core.regex_engine import RegexAnalyzer
from src.core.llm_analyzer import LocalLLMAnalyzer
from src.core.file_processor import process_log_file

console = Console()

def display_banner():
    banner_text = Text(
        "LOGSENTRY AI\n"
        "Advanced Static Log & Email Analyzer\n"
        "powered by AI", 
        justify="center", style="bold magenta"
    )
    aligned_text = Align.center(banner_text)
    panel = Panel(aligned_text, border_style="magenta", padding=(1, 2))
    console.print(panel)

def display_results(score: int, matches: list, llm_verdict: str):
    # Regex Table
    table = Table(title="Regex Analysis Results", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="dim", width=20)
    table.add_column("Value")
    
    if score >= 80:
        score_style = "bold red"
        border_color = "red"
        level = "Critical"
    elif score >= 50:
        score_style = "bold yellow"
        border_color = "yellow"
        level = "Warning"
    else:
        score_style = "bold green"
        border_color = "green"
        level = "Info"
        
    table.add_row("Threat Score", f"[{score_style}]{score} ({level})[/{score_style}]")
    
    match_str = ", ".join(matches) if matches else "None detected"
    table.add_row("Signatures Matched", match_str)
    
    console.print(table)
    
    # LLM Verdict Panel
    if llm_verdict and llm_verdict != "N/A":
        llm_panel = Panel(
            llm_verdict, 
            title=f"[{score_style}]Local LLM Verdict ({level})[/{score_style}]", 
            border_style=border_color, 
            padding=(1, 1)
        )
        console.print(llm_panel)

def single_string_flow():
    log_text = questionary.text("Enter the raw log string to analyze:").ask()
    if not log_text:
        return
        
    threshold_str = questionary.text("Enter threat threshold (default: 50):", default="50").ask()
    if threshold_str is None:
        return
    
    try:
        threshold = int(threshold_str)
    except ValueError:
        threshold = 50
        
    with console.status("[bold green]Running regex engine...[/bold green]"):
        analyzer = RegexAnalyzer()
        result = analyzer.analyze(log_text)
        score = result['score']
        matches = result['matches']
        
    llm_verdict = "N/A"
    if score >= threshold:
        with console.status("[bold yellow]Threat threshold met! Routing to Local LLM...[/bold yellow]"):
            llm = LocalLLMAnalyzer()
            llm_verdict = llm.evaluate_log(log_text, score, matches)
            
    display_results(score, matches, llm_verdict)
    
    # Confirm to continue
    questionary.confirm("Press Enter to return to main menu...", default=True).ask()

def file_processing_flow():
    file_path = questionary.path("Enter the path to the log or CSV file:").ask()
    if not file_path:
        return
        
    threshold_str = questionary.text("Enter threat threshold (default: 50):", default="50").ask()
    if threshold_str is None:
        return
        
    try:
        threshold = int(threshold_str)
    except ValueError:
        threshold = 50
        
    console.print(f"\n[bold cyan]Starting bulk processing for '{file_path}'...[/bold cyan]")
    # Process log file natively runs its own loop and output print
    process_log_file(file_path, threshold)
    
    questionary.confirm("\nPress Enter to return to main menu...", default=True).ask()

def main():
    display_banner()
    
    while True:
        try:
            choice = questionary.select(
                "Select an action:",
                choices=[
                    "🔍 Analyze a single log string",
                    "📁 Analyze a log file (CSV/TXT)",
                    "❌ Exit"
                ]
            ).ask()
            
            if choice == "🔍 Analyze a single log string":
                single_string_flow()
            elif choice == "📁 Analyze a log file (CSV/TXT)":
                file_processing_flow()
            elif choice == "❌ Exit" or choice is None:
                console.print("[bold green]Exiting LogSentry AI. Stay safe![/bold green]")
                break
                
        except KeyboardInterrupt:
            console.print("\n[bold red]Operation cancelled by user. Exiting...[/bold red]")
            break

if __name__ == "__main__":
    main()
