import click
import sys
import os

# Ensure the root folder is added to path when script is executed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.core.regex_engine import RegexAnalyzer
from src.core.llm_analyzer import LocalLLMAnalyzer
from src.core.file_processor import process_log_file

@click.group()
def cli():
    """Static Log & Email Analyzer CLI"""
    pass

@cli.command()
@click.argument('log_text')
@click.option('--threshold', default=50, help='Regex score threshold to trigger LLM analysis')
def analyze(log_text: str, threshold: int):
    """Analyzes a single log string."""
    click.echo(f"Analyzing log: '{log_text}'")
    
    # 1. Regex Baseline Analysis
    analyzer = RegexAnalyzer()
    result = analyzer.analyze(log_text)
    
    score = result['score']
    matches = result['matches']
    
    click.echo(f"\n[REGEX ENGINE] Threat Score: {score}")
    if matches:
        click.echo(f"[REGEX ENGINE] Signatures matched: {', '.join(matches)}")
    else:
        click.echo("[REGEX ENGINE] No malicious signatures detected.")
    
    # 2. LLM Evaluation if threshold met
    if score >= threshold:
        click.echo(f"\n[ALERT] Threat score >= threshold ({score} >= {threshold}). Forwarding to Local LLM...")
        llm = LocalLLMAnalyzer()
        llm_verdict = llm.evaluate_log(log_text, score, matches)
        click.echo("\n[LLM VERDICT]")
        click.echo(llm_verdict)
    else:
        click.echo(f"\n[INFO] Alert score below threshold (< {threshold}). No LLM analysis needed.")

@cli.command('analyze-file')
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--threshold', default=50, help='Regex score threshold to trigger LLM analysis')
def analyze_file(file_path: str, threshold: int):
    """Analyzes a bulk log or CSV file."""
    click.echo(f"Initializing bulk file analysis for: '{file_path}'")
    click.echo(f"LLM Threshold is set to: {threshold}")
    process_log_file(file_path, threshold)

if __name__ == '__main__':
    cli()
