import pandas as pd
import os

def process_tables():
    """
    Processa e combina todas as tabelas em um único DataFrame
    """
    print("Processando tabelas...")
    
    try:
        # Carrega as tabelas extraídas
        tables = pd.read_pickle('transformer/temp/raw_tables.pkl')
        
        # Lista para armazenar as tabelas válidas
        valid_tables = []
        
        for i, table in enumerate(tables):
            # Verifica se a tabela tem as colunas esperadas
            if 'OD' in table.columns or 'AMB' in table.columns:
                valid_tables.append(table)
        
        if not valid_tables:
            print("Nenhuma tabela válida encontrada")
            return None
        
        # Combina todas as tabelas válidas
        df_combined = pd.concat(valid_tables, ignore_index=True)
        
        # Substitui as abreviações
        replacements = {
            'OD': 'Seg Odontológica',
            'AMB': 'Seg Ambulatorial'
        }   
        
        # Renomeia as colunas se existirem
        df_combined = df_combined.rename(columns=replacements)
        
        # Substitui valores nas colunas
        for col in df_combined.columns:
            if col in ['Seg Odontológica', 'Seg Ambulatorial']:
                df_combined[col] = df_combined[col].replace({
                    'OD': 'Seg Odontológica',
                    'AMB': 'Seg Ambulatorial'
                })
        
        # Salva o DataFrame processado
        df_combined.to_pickle('transformer/temp/processed_table.pkl')
        print("Tabelas processadas com sucesso!")
        return True
        
    except Exception as e:
        print(f"Erro durante o processamento: {str(e)}")
        return False

def main():
    if not os.path.exists('transformer/temp/raw_tables.pkl'):
        print("Arquivo de tabelas não encontrado!")
        print("Execute primeiro o extract_pdf.py")
        return
    
    process_tables()

if __name__ == "__main__":
    main() 