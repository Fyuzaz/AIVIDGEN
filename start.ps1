# Script de Inicialização - AI Shorts Generator

Write-Host "--- Iniciando AI Shorts Generator ---" -ForegroundColor Cyan

# 1. Verificar ambiente virtual
if (-Not (Test-Path ".myvenv")) {
    Write-Host "[!] Ambiente .myvenv não encontrado. Criando..." -ForegroundColor Yellow
    python -m venv .myvenv
}

# 2. Ativar ambiente e instalar dependências básicas se necessário
Write-Host "[*] Ativando ambiente virtual..." -ForegroundColor Green
& ".\.myvenv\Scripts\Activate.ps1"

# 3. Garantir pastas necessárias
if (-Not (Test-Path "logs")) { mkdir logs }
if (-Not (Test-Path "downloads")) { mkdir downloads }
if (-Not (Test-Path "outputs")) { mkdir outputs }

# 4. Iniciar o servidor
Write-Host "[*] Servidor iniciando em http://localhost:8000" -ForegroundColor Green
python main.py
