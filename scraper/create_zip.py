import zipfile
import os

def create_zip(pdf_dir, zip_name):
    """
    Função para criar arquivo ZIP com os PDFs
    """
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for pdf_file in os.listdir(pdf_dir):
            if pdf_file.lower().endswith('.pdf'):
                file_path = os.path.join(pdf_dir, pdf_file)
                zipf.write(file_path)
                print(f'Arquivo {pdf_file} adicionado ao ZIP')

def main():
    # Definir diretórios
    pdf_dir = 'scraper/downloads/pdfs'
    zip_dir = 'scraper/downloads/zips'
    
    # Criar pasta para os ZIPs se não existir
    if not os.path.exists(zip_dir):
        os.makedirs(zip_dir)
    
    # Verificar se existem PDFs para compactar
    if os.path.exists(pdf_dir):
        pdfs = [f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')]
        if pdfs:
            zip_name = os.path.join(zip_dir, 'anexos.zip')
            create_zip(pdf_dir, zip_name)
            print(f'\nArquivos compactados em: {zip_name}')
            print('PDFs originais mantidos na pasta downloads/pdfs')
        else:
            print('Nenhum arquivo PDF encontrado para compactar')
    else:
        print(f'Diretório {pdf_dir} não encontrado. Execute primeiro o download_pdfs.py')

if __name__ == "__main__":
    main() 