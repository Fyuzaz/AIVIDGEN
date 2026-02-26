import os
import re
from datetime import datetime

def analyze_logs(log_file="logs/app.log"):
    if not os.path.exists(log_file):
        print(f"Erro: Arquivo de log '{log_file}' não encontrado.")
        return

    with open(log_file, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()

    total_requests = 0
    errors = 0
    successes = 0
    job_ids = set()

    for line in lines:
        if "Starting process for URL" in line:
            total_requests += 1
        
        # Check for non-benign errors
        if "ERROR" in line:
            # Ignore the benign connection errors and asyncio connection lost noise
            benign_patterns = [
                "WinError 10054", 
                "ConnectionResetError", 
                "BrokenPipeError",
                "connection_lost()",
                "_call_connection_lost"
            ]
            if not any(x in line for x in benign_patterns):
                errors += 1
                
        if "Process completed successfully" in line:
            successes += 1
        
        # Extract JobID if present
        job_match = re.search(r'\[(.*?)\]', line)
        if job_match:
            job_ids.add(job_match.group(1))

    print("="*40)
    print("RELATÓRIO DE BACKLOG - AI SHORTS")
    print("="*40)
    print(f"Data da análise: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Total de requisições: {total_requests}")
    print(f"Total de JobIDs únicos: {len(job_ids)}")
    print(f"Sucessos: {successes}")
    print(f"Erros Críticos: {errors}")
    print("-" * 20)
    
    if errors > 0:
        print("\nÚLTIMOS ERROS CRÍTICOS ENCONTRADOS:")
        # Filter out benign errors for the error display too
        relevant_errors = [l for l in lines if "ERROR" in l and not any(x in l for x in ["WinError 10054", "ConnectionResetError", "BrokenPipeError"])]
        for err in relevant_errors[-5:]:
            print(f" > {err.strip()}")
    else:
        print("\nNenhum erro crítico detectado.")
    
    print("="*40)

if __name__ == "__main__":
    analyze_logs()
