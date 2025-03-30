import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import time
import zipfile
import pandas as pd
import io

def create_directory(path):
    """Cria um diretório se ele não existir"""
    if not os.path.exists(path):
        os.makedirs(path)

def download_file(url):
    """Faz o download de um arquivo e retorna o conteúdo"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"Erro ao baixar {url}: {str(e)}")
        return None

def process_zip_content(zip_content):
    """Processa o conteúdo do arquivo ZIP e retorna um DataFrame"""
    try:
        # Cria um objeto ZipFile a partir do conteúdo em memória
        with zipfile.ZipFile(io.BytesIO(zip_content)) as zip_ref:
            # Encontra o arquivo CSV dentro do ZIP
            csv_files = [f for f in zip_ref.namelist() if f.endswith('.csv')]
            if not csv_files:
                return None
            
            # Lê o primeiro arquivo CSV encontrado
            with zip_ref.open(csv_files[0]) as csv_file:
                df = pd.read_csv(csv_file, encoding='utf-8', sep=';')
                return df
    except Exception as e:
        print(f"Erro ao processar ZIP: {str(e)}")
        return None

def download_demonstracoes_contabeis(anos):
    """Baixa as demonstrações contábeis dos anos especificados e cria um CSV único"""
    base_url = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"
    all_data = []
    
    for ano in anos:
        print(f"\nProcessando dados de {ano}...")
        
        # Monta URL do ano
        ano_url = urljoin(base_url, str(ano) + "/")
        
        try:
            # Obtém lista de arquivos do diretório
            response = requests.get(ano_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Encontra todos os links na página
            for link in soup.find_all('a'):
                file_name = link.get('href')
                
                # Pula links que não são arquivos ZIP
                if not file_name or not file_name.lower().endswith('.zip'):
                    continue
                
                # Monta URL completa do arquivo
                file_url = urljoin(ano_url, file_name)
                
                print(f"Baixando: {file_name}")
                zip_content = download_file(file_url)
                
                if zip_content:
                    print(f"Processando: {file_name}")
                    df = process_zip_content(zip_content)
                    if df is not None:
                        all_data.append(df)
                    time.sleep(1)  # Pausa entre downloads
                
        except Exception as e:
            print(f"Erro ao processar ano {ano}: {str(e)}")
    
    if all_data:
        # Combina todos os DataFrames
        final_df = pd.concat(all_data, ignore_index=True)
        
        # Cria diretório para o resultado
        output_dir = "resultados"
        create_directory(output_dir)
        
        # Salva o DataFrame combinado
        output_file = os.path.join(output_dir, "demonstracoes_contabeis_combinadas.csv")
        final_df.to_csv(output_file, index=False, encoding='latin1', sep=';')
        print(f"\nArquivo CSV combinado criado em: {output_file}")
    else:
        print("\nNenhum dado foi processado.")

def download_operadoras_ativas():
    """Baixa o CSV das operadoras ativas"""
    url = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv"
    print("\nBaixando dados de operadoras ativas...")
    
    try:
        content = download_file(url)
        if content:
            # Cria diretório para o resultado
            output_dir = "resultados"
            create_directory(output_dir)
            
            # Salva o arquivo
            output_file = os.path.join(output_dir, "operadoras_ativas.csv")
            with open(output_file, 'wb') as f:
                f.write(content)
            print(f"Arquivo de operadoras ativas salvo em: {output_file}")
            return True
    except Exception as e:
        print(f"Erro ao baixar dados de operadoras ativas: {str(e)}")
    return False

if __name__ == "__main__":
    # Anos para download
    anos = [2023, 2024]
    
    print("Iniciando download e processamento das demonstrações contábeis...")
    download_demonstracoes_contabeis(anos)
    
    print("\nBaixando dados de operadoras ativas...")
    download_operadoras_ativas()
    
    print("\nProcesso finalizado!")
