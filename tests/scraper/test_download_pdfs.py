import pytest
from unittest.mock import patch, Mock
import os
from scraper.download_pdfs import download_pdf, main

def test_download_pdf_success():
    # Simula uma resposta bem sucedida
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = b"fake pdf content"
    
    with patch('requests.get', return_value=mock_response):
        with patch('builtins.open', create=True) as mock_open:
            result = download_pdf('http://fake-url.com/test.pdf', 'test.pdf')
            
            assert result == True
            mock_open.assert_called_once()

def test_download_pdf_failure():
    # Simula uma resposta com erro
    mock_response = Mock()
    mock_response.status_code = 404
    
    with patch('requests.get', return_value=mock_response):
        result = download_pdf('http://fake-url.com/test.pdf', 'test.pdf')
        assert result == False

def test_main_success():
    # Simula resposta HTML com links para PDFs
    mock_html = '''
    <html>
        <a href="anexo1.pdf">Anexo I</a>
        <a href="anexo2.pdf">Anexo II</a>
    </html>
    '''
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = mock_html
    
    with patch('requests.get', return_value=mock_response), \
         patch('scraper.download_pdfs.download_pdf', return_value=True), \
         patch('os.path.exists', return_value=False), \
         patch('os.makedirs'):
        main() 

def test_main_site_error():
    mock_response = Mock()
    mock_response.status_code = 404
    
    with patch('requests.get', return_value=mock_response):
        main()  # Deve printar 'Erro ao acessar o site'

def test_main_no_matching_links():
    mock_html = '''
    <html>
        <a href="outro.pdf">Outro documento</a>
    </html>
    '''
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = mock_html
    
    with patch('requests.get', return_value=mock_response), \
         patch('os.path.exists', return_value=False), \
         patch('os.makedirs'):
        main()  # Não deve chamar download_pdf 