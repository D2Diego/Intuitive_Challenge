import pandas as pd
import zipfile
import os

def save_and_zip(base_name):
    """
    Salva o DataFrame em CSV e cria arquivo ZIP
    """
    try:
        # Carrega o DataFrame processado
        df = pd.read_pickle('transformer/temp/processed_table.pkl')
        
        # Cria pasta para os arquivos se não existir
        output_dir = 'transformer/output'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Caminhos dos arquivos
        csv_path = f'{output_dir}/{base_name}.csv'
        zip_path = f'{output_dir}/{base_name}.zip'
        
        # Salva o CSV
        df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"CSV salvo em: {csv_path}")
        
        # Cria o ZIP
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(csv_path, os.path.basename(csv_path))
        print(f"Arquivo ZIP criado em: {zip_path}")
        
        # Remove o CSV original
        os.remove(csv_path)
        print("Arquivo CSV original removido")
        
        # Limpa arquivos temporários
        os.remove('transformer/temp/raw_tables.pkl')
        os.remove('transformer/temp/processed_table.pkl')
        print("Arquivos temporários removidos")
        
        return True
    
    except Exception as e:
        print(f"Erro ao criar arquivos de saída: {str(e)}")
        return False

def main():
    # Verifica se existe o arquivo processado
    if not os.path.exists('transformer/temp/processed_table.pkl'):
        print("Arquivo de tabela processada não encontrado!")
        print("Execute primeiro extract_pdf.py e process_tables.py")
        return
    
    # Cria os arquivos de saída
    save_and_zip("Teste_Diego_I")

if __name__ == "__main__":
    main() 