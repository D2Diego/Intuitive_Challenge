import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

def download_pdf(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f'Download concluído: {filename}')
        return True
    else:
        print(f'Erro ao baixar {filename}')
        return False

def main():
    url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
    
    if not os.path.exists('scraper/downloads/pdfs'):
        os.makedirs('scraper/downloads/pdfs')
    
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        pdf_files = []
        for link in soup.find_all('a'):
            href = link.get('href', '')
            text = link.get_text().lower()
            
            if 'anexo i' in text or 'anexo ii' in text:
                if href.endswith('.pdf'):
                    full_url = urljoin(url, href)
                    filename = os.path.join('scraper/downloads/pdfs', os.path.basename(href))
                    download_pdf(full_url, filename)
        
        print('\nDownload dos PDFs finalizado!')
    else:
        print('Erro ao acessar o site')

if __name__ == "__main__":
    main() 