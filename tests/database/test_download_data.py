import pytest
from unittest.mock import patch, Mock
import pandas as pd
import io
import zipfile
from database.download_data import (
    create_directory,
    download_file,
    process_zip_content,
    download_demonstracoes_contabeis,
    download_operadoras_ativas
)

def test_create_directory():
    with patch('os.path.exists', return_value=False), \
         patch('os.makedirs') as mock_makedirs:
        create_directory('test_dir')
        mock_makedirs.assert_called_once_with('test_dir')

def test_create_directory_exists():
    with patch('os.path.exists', return_value=True), \
         patch('os.makedirs') as mock_makedirs:
        create_directory('test_dir')
        mock_makedirs.assert_not_called()

def test_download_file_success():
    mock_response = Mock()
    mock_response.content = b"test content"
    mock_response.raise_for_status = Mock()
    
    with patch('requests.get', return_value=mock_response):
        content = download_file('http://test.com/file.zip')
        assert content == b"test content"

def test_download_file_failure():
    with patch('requests.get', side_effect=Exception('Download error')):
        content = download_file('http://test.com/file.zip')
        assert content is None

def test_process_zip_content():
    # Cria um DataFrame de teste
    test_df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
    
    # Cria um arquivo CSV em memória
    csv_buffer = io.StringIO()
    test_df.to_csv(csv_buffer, index=False, encoding='utf-8', sep=';')
    csv_content = csv_buffer.getvalue().encode('utf-8')
    
    # Cria um arquivo ZIP em memória
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        zip_file.writestr('test.csv', csv_content)
    
    # Testa o processamento
    result_df = process_zip_content(zip_buffer.getvalue())
    pd.testing.assert_frame_equal(result_df, test_df)

def test_process_zip_content_no_csv():
    # Cria um ZIP sem arquivos CSV
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        zip_file.writestr('test.txt', b'test content')
    
    result = process_zip_content(zip_buffer.getvalue())
    assert result is None

@patch('database.download_data.download_file')
@patch('database.download_data.process_zip_content')
@patch('requests.get')
@patch('os.makedirs')
def test_download_demonstracoes_contabeis(mock_makedirs, mock_get, mock_process, mock_download):
    # Mock da resposta HTML
    mock_response = Mock()
    mock_response.text = '''
        <html>
            <a href="file1.zip">File 1</a>
            <a href="file2.zip">File 2</a>
        </html>
    '''
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response
    
    # Mock do processamento
    mock_df = pd.DataFrame({'col1': [1]})
    mock_process.return_value = mock_df
    mock_download.return_value = b'zip content'
    
    with patch('pandas.DataFrame.to_csv'):
        download_demonstracoes_contabeis([2023])

def test_download_operadoras_ativas_success():
    mock_content = b"test content"
    
    with patch('database.download_data.download_file', return_value=mock_content), \
         patch('os.makedirs'), \
         patch('builtins.open', create=True):
        result = download_operadoras_ativas()
        assert result is True

def test_download_operadoras_ativas_failure():
    with patch('database.download_data.download_file', return_value=None):
        result = download_operadoras_ativas()
        assert result is False 