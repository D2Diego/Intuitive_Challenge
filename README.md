# Estrutura do Projeto - Testes de Nivelamento

## 1. TESTE DE WEB SCRAPING
Pasta: `/scraper/`
- `download_pdfs.py`: Download dos anexos
- `create_zip.py`: Compactação dos PDFs

## 2. TESTE DE TRANSFORMAÇÃO DE DADOS
Pasta: `/transformer/`
- `extract_pdf.py`: Extração das tabelas do PDF
- `process_tables.py`: Processamento e formatação dos dados
- `create_output.py`: Criação do arquivo CSV e ZIP final

## 3. TESTE DE BANCO DE DADOS
Pasta: `/database/`
- `download_data.py`: Download dos dados da ANS
- `create_tables.sql`: Criação das estruturas das tabelas
- `load_data.sql`: Importação dos dados
- `analise_despesas.sql`: Queries analíticas solicitadas

## 4. TESTE DE API
### Backend (Python/Flask)
Pasta: `/operator-search-api/`
- Implementação da API REST para busca de operadoras

### Frontend (Vue.js/TypeScript)
Pasta: `/my-vue-ts-app/`
- Interface web para consulta de operadoras

# Healthcare Provider Search System

A system to search for healthcare providers in Brazil using data from ANS (Agência Nacional de Saúde Suplementar).

## Prerequisites

- Python 3.8+
- Node.js 14+
- PostgreSQL
- Java Runtime Environment (JRE)

## Backend Setup

1. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the `operator-search-api` directory with your database credentials:

```
DB_HOST=localhost
DB_NAME=db_intuitive_care
DB_USER=your_user
DB_PASSWORD=your_password
```

4. Run the backend server:

```bash
cd operator-search-api
python run.py
```

The API will be available at `http://localhost:5000`

## Frontend Setup

1. Install Node.js dependencies:

```bash
cd my-vue-ts-app
yarn install
```

2. Run the development server:

```bash
yarn serve
```

The application will be available at `http://localhost:8080`

