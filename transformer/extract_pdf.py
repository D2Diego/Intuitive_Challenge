import tabula
import pandas as pd
import os

def extract_tables_from_pdf(pdf_path):
    """
    Extrai todas as tabelas do PDF usando tabula
    """
    print("Extraindo tabelas do PDF...")
    try:
        # Extrai todas as tabelas de todas as páginas
        # lattice=True para tabelas com linhas visíveis
        # pages='all' para todas as páginas
        tables = tabula.read_pdf(
            pdf_path,
            pages='all',
            multiple_tables=True,
            lattice=True
        )
        print(f"Foram encontradas {len(tables)} tabelas no PDF")
        return tables
    except Exception as e:
        print(f"Erro ao extrair tabelas: {str(e)}")
        return None

def main():
    # Procura o PDF do Anexo I com o nome correto
    pdf_path = "scraper/downloads/pdfs/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"Arquivo {pdf_path} não encontrado!")
        print("Execute primeiro o download_pdfs.py do scraper")
        return None
    
    try:
        # Cria o diretório temp se não existir
        temp_dir = 'transformer/temp'
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
            
        # Extrai as tabelas
        tables = extract_tables_from_pdf(pdf_path)
        if tables:
            # Salva as tabelas para processamento posterior
            pd.to_pickle(tables, f'{temp_dir}/raw_tables.pkl')
            print("Tabelas extraídas e salvas com sucesso!")
            return True
    except Exception as e:
        print(f"Erro durante a extração: {str(e)}")
        print("\nDicas de solução:")
        print("1. Certifique-se que o Java está instalado (necessário para o tabula-py)")
        print("2. Instale as dependências:")
        print("   pip3 install tabula-py pandas jpype1")
    
    return False

if __name__ == "__main__":
    main() 