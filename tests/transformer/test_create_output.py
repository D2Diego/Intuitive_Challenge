import pytest
from unittest.mock import patch, Mock
import pandas as pd
import os
from transformer.create_output import save_and_zip, main

def test_save_and_zip_success():
    mock_df = pd.DataFrame({'test': ['data']})
    
    with patch('pandas.read_pickle', return_value=mock_df), \
         patch('os.path.exists', return_value=False), \
         patch('os.makedirs'), \
         patch('pandas.DataFrame.to_csv'), \
         patch('zipfile.ZipFile'), \
         patch('os.remove'):
        
        result = save_and_zip('test_output')
        assert result is True

def test_save_and_zip_error():
    with patch('pandas.read_pickle', side_effect=Exception('Error')):
        result = save_and_zip('test_output')
        assert result is False

def test_main_file_not_found():
    with patch('os.path.exists', return_value=False):
        main()  # Should print error message

def test_main_success():
    with patch('os.path.exists', return_value=True), \
         patch('transformer.create_output.save_and_zip') as mock_save:
        main()
        mock_save.assert_called_once_with('Teste_Diego_I') 