# 🎮 Know Your Fan - FURIA — Plataforma de Validação e Análise de Fãs de eSports

**Know Your Fan** é uma aplicação desenvolvida com foco em clubes e organizações de eSports que desejam **conhecer melhor sua base de fãs**. A plataforma coleta e analisa dados pessoais, comportamentais e sociais dos usuários, com validação automatizada de documentos e visualização de interesses em tempo real.

______________________________________________________________________

## 📌 Funcionalidades Principais

- 📑 Upload e validação de documentos via OCR (com OpenCV e Tesseract)
- 🔍 Análise de presença e relevância em redes sociais (simulada ou integrável com APIs)
- 📊 Visualização interativa dos interesses e comportamentos dos fãs
- 🧠 Controle de fluxo de navegação por etapas com gerenciamento de estado no Streamlit

__________________________________________________________

## 🚀 Como Rodar Localmente

### 1. Clone o repositório

``bash
git clone https://github.com/rodrigo278/KnowYourFan.git
cd KnowYourFan

__________________________________________________

2. Crie um ambiente virtual
   
python -m venv venv
source venv/bin/activate   # No Windows: venv\Scripts\activate

______________________________________________________

3.  Instale as dependências
Se estiver usando Poetry:
poetry install

Ou crie um requirements.txt com:
streamlit
opencv-python
pytesseract
pandas
plotly
numpy
Pillow

E instale com:

pip install -r requirements.txt
⚠️ Pré-requisito: Certifique-se de ter o Tesseract OCR instalado e configurado.
Linux (Ubuntu): sudo apt install tesseract-ocr
Windows/Mac: Download oficial

___________________________________________________________

4. Execute o app
bash
Copiar
Editar
streamlit run app.py

_____________________________________________________________

Estrutura do Projeto:
KnowYourFan/
├── app.py                         # Aplicação principal Streamlit
├── pyproject.toml                # Dependências (formato Poetry)
├── uv.lock                       # Lockfile de dependências
├── .replit                       # Configuração para ambiente Replit
├── .streamlit/config.toml       # Configurações de tema do Streamlit
├── assets/logo.svg              # Logotipo da aplicação
└── utils/
    ├── __init__.py
    ├── data_visualization.py    # Geração de gráficos com Plotly
    ├── document_validator.py    # Validação OCR de documentos
    └── social_media.py          # Análise simulada de redes sociais

_________________________________________________________

Tecnologias Utilizadas:
Python 3.10+

Streamlit — Interface interativa e rápida para protótipos web

OpenCV + Tesseract — OCR e processamento de imagem

Plotly — Visualização de dados

Pandas / NumPy — Manipulação de dados

Poetry — Gerenciador de dependências moderno



Autor: Rodrigo Silva
