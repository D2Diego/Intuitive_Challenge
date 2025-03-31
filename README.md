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

# Sistema de Busca de Prestadores de Saúde

Um sistema para busca de prestadores de saúde no Brasil utilizando dados da ANS (Agência Nacional de Saúde Suplementar).

## Pré-requisitos

- Python 3.8+
- Node.js 14+
- PostgreSQL
- Ambiente de Execução Java (JRE)

## Configuração do Backend

1. Crie um ambiente virtual e ative:

```bash
python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows
```

2. Instale as dependências do Python:

```bash
pip install -r requirements.txt
```

3. Crie um arquivo `.env` no diretório `operator-search-api` com as credenciais do banco de dados:

```
DB_HOST=localhost
DB_NAME=db_intuitive_care
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
```

4. Execute o servidor backend:

```bash
cd operator-search-api
python run.py
```

A API estará disponível em `http://localhost:5000`

## Configuração do Frontend

1. Instale as dependências do Node.js:

```bash
cd my-vue-ts-app
yarn install
```

2. Execute o servidor de desenvolvimento:

```bash
yarn serve
```

A aplicação estará disponível em `http://localhost:8080`

## Executando os Testes

Para executar os testes, basta rodar o seguinte comando na raiz do projeto:

```bash
pytest
```

