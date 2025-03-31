import pytest
from unittest.mock import patch, Mock
import pandas as pd
import os
from transformer.process_tables import process_tables, main

def test_process_tables_success():
    mock_tables = [
        pd.DataFrame({'OD': ['test1']}),
        pd.DataFrame({'AMB': ['test2']})
    ]
    
    with patch('pandas.read_pickle', return_value=mock_tables), \
         patch('pandas.DataFrame.to_pickle'):
        result = process_tables()
        assert result is True

def test_process_tables_no_valid_tables():
    mock_tables = [
        pd.DataFrame({'OTHER': ['test1']}),
        pd.DataFrame({'ANOTHER': ['test2']})
    ]
    
    with patch('pandas.read_pickle', return_value=mock_tables):
        result = process_tables()
        assert result is None

def test_process_tables_error():
    with patch('pandas.read_pickle', side_effect=Exception('Error')):
        result = process_tables()
        assert result is False

def test_main_file_not_found():
    with patch('os.path.exists', return_value=False):
        main()

def test_main_success():
    with patch('os.path.exists', return_value=True), \
         patch('transformer.process_tables.process_tables') as mock_process:
        main()
        mock_process.assert_called_once() 