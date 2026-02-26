# 🔥 AI Shorts Generator

Transforme vídeos longos em shorts virais automaticamente usando IA, ou selecione manualmente os trechos desejados com um editor de timeline interativo.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=flat-square&logo=fastapi)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## ✨ Funcionalidades

### 🤖 Geração Automática com IA
- **Análise inteligente** do vídeo usando heatmap do YouTube e transcrição
- Detecção automática dos **melhores momentos** para shorts
- Geração de até **3 shorts** por vídeo com os trechos mais relevantes
- **Legendas automáticas** (ASS) com estilo profissional

### 📹 Editor Manual de Timeline
- **Player de vídeo** integrado no navegador
- **Timeline interativa** com playhead e barra de progresso
- Marcação manual de **início/fim** dos trechos desejados
- Suporte a **múltiplos segmentos** por vídeo
- Preview e reprodução de cada segmento antes de gerar
- Marcadores de **legendas na timeline** para referência visual

### ✂️ Seletor Visual de Crop
- Preview do frame do vídeo com overlay interativo
- **Retângulo 9:16 arrastável** para escolher a posição do crop
- Coordenadas normalizadas (funciona com qualquer resolução)
- Integrado ao editor manual e ao modo IA

### 🎬 Renderização de Shorts
- Crop automático para formato **9:16** (vertical/portrait)
- Escala para **1080p** com filtro Lanczos (alta qualidade)
- **Legendas queimadas** (burn-in) com estilo bold e fade
- Único passo de FFmpeg — renderização **ultrafast**
- Otimizado para web com `faststart` flag

### 📝 Transcrição Inteligente
- **Prioridade**: legendas do YouTube (instantâneo, sem download)
- **Fallback**: transcrição com Whisper (modelo `base`)
- Suporte a múltiplos idiomas (PT, EN, ES, PT-BR)
- Modelo Whisper carregado como **singleton** (memória eficiente)

### 📊 Análise de Conteúdo
- **Heatmap do YouTube**: detecta picos de engajamento
- **Análise por keywords**: scoring de segmentos por palavras-chave
- Seleção inteligente de trechos não-sobrepostos

---

## 🚀 Instalação

### Pré-requisitos

- **Python 3.10+** (recomendado 3.11 ou 3.12)
- **FFmpeg** instalado e acessível no PATH
- **Git** (para clonar o repositório)

#### Instalar FFmpeg

**Windows (via winget):**
```bash
winget install Gyan.FFmpeg
```

**Windows (via Chocolatey):**
```bash
choco install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

Verifique se está funcionando:
```bash
ffmpeg -version
```

### Passo a Passo

**1. Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/ai-shorts-generator.git
cd ai-shorts-generator
```

**2. Crie o ambiente virtual:**
```bash
python -m venv .myvenv
```

**3. Ative o ambiente:**

Windows (PowerShell):
```powershell
.\.myvenv\Scripts\Activate.ps1
```

Linux/macOS:
```bash
source .myvenv/bin/activate
```

**4. Instale as dependências:**
```bash
pip install -r requirements.txt
```

> ⚠️ **Nota**: O `openai-whisper` requer PyTorch. Na primeira execução, o Whisper baixará o modelo (~140MB). Se você usa apenas vídeos do YouTube com legendas disponíveis, o Whisper não será necessário.

**5. Inicie o servidor:**
```bash
python main.py
```

Ou use o script automatizado (Windows):
```powershell
.\start.ps1
```

**6. Acesse no navegador:**
```
http://localhost:8000
```

Para acessar de **outros dispositivos na rede local**, use o IP da máquina:
```
http://<SEU-IP>:8000
```

---

## 📖 Como Usar

### Modo IA Automático
1. Cole o link do vídeo (YouTube, TikTok, etc.)
2. Clique em **🤖 IA Auto**
3. Aguarde a análise e geração automática
4. Baixe os shorts gerados

### Modo Manual (Editor de Timeline)
1. Cole o link do vídeo
2. Clique em **📹 Carregar** — o vídeo será baixado e carregado no player
3. Navegue pelo vídeo usando o player
4. Clique em **🟢 Marcar Início** no ponto desejado
5. Avance até o final do trecho e clique **🔴 Marcar Fim**
6. Repita para adicionar mais segmentos
7. (Opcional) Use **✂️ Selecionar Área de Crop** para ajustar a posição do crop
8. Clique em **🚀 Gerar Shorts dos Segmentos**

---

## 📁 Estrutura do Projeto

```
AIGENERATEVIDEO/
├── main.py              # API FastAPI (endpoints + cache)
├── processor.py         # Pipeline de processamento (IA + Manual)
├── downloader.py        # Download de vídeos via yt-dlp
├── transcriber.py       # Transcrição com Whisper
├── ai_analyzer.py       # Análise de heatmap + keywords
├── editor.py            # Renderização FFmpeg (crop + legendas)
├── analyze_logs.py      # Utilitário de análise de logs
├── start.ps1            # Script de inicialização (Windows)
├── requirements.txt     # Dependências Python
├── static/
│   ├── index.html       # Interface principal
│   ├── script.js        # Lógica do frontend
│   ├── style.css        # Estilos (dark theme)
│   ├── timeline.js      # Editor de timeline
│   └── crop.js          # Seletor visual de crop
├── downloads/           # Vídeos temporários (auto-limpeza)
├── outputs/             # Shorts gerados
└── logs/                # Logs da aplicação
```

---

## ⚙️ Configuração

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| Chave API | Gemini/OpenAI (opcional, para análise avançada) | Campo na UI |
| Porta | Porta do servidor | `8000` |
| Resolução de saída | Resolução dos shorts | `608x1080` (9:16) |
| Modelo Whisper | Modelo de transcrição | `base` |

---

## 🛠️ Tecnologias

| Componente | Tecnologia |
|------------|------------|
| Backend | FastAPI + Uvicorn |
| Download | yt-dlp |
| Transcrição | OpenAI Whisper |
| Edição | FFmpeg (libx264) |
| Frontend | HTML5 + Vanilla JS + CSS |
| IA | Google Generative AI (Gemini) |

---

## 📋 API Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/` | Interface web |
| `POST` | `/load` | Carrega vídeo para o player |
| `POST` | `/preview` | Extrai thumbnail para crop |
| `POST` | `/process` | Gera shorts com IA |
| `POST` | `/process-manual` | Gera shorts dos segmentos manuais |
| `GET` | `/status/{job_id}` | Status do processamento |

---

## 📄 Licença

MIT License — Use livremente.
