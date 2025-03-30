import tabula
import pandas as pd
import os

def extract_tables_from_pdf(pdf_path):
    print("Extraindo tabelas do PDF...")
    try:
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
    pdf_path = "scraper/downloads/pdfs/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"Arquivo {pdf_path} não encontrado!")
        print("Execute primeiro o download_pdfs.py do scraper")
        return None
    
    try:
        temp_dir = 'transformer/temp'
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
            
        tables = extract_tables_from_pdf(pdf_path)
        if tables:
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