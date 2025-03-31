import pytest
from unittest.mock import patch, Mock
import pandas as pd
import os
from transformer.extract_pdf import extract_tables_from_pdf, main

def test_extract_tables_success():
    mock_tables = [pd.DataFrame({'OD': ['test']})]
    
    with patch('tabula.read_pdf', return_value=mock_tables):
        result = extract_tables_from_pdf('fake.pdf')
        assert result == mock_tables

def test_extract_tables_failure():
    with patch('tabula.read_pdf', side_effect=Exception('PDF Error')):
        result = extract_tables_from_pdf('fake.pdf')
        assert result is None

def test_main_pdf_not_found():
    with patch('os.path.exists', return_value=False):
        result = main()
        assert result is None

def test_main_success():
    mock_tables = [pd.DataFrame({'OD': ['test']})]
    
    with patch('os.path.exists', return_value=True), \
         patch('transformer.extract_pdf.extract_tables_from_pdf', return_value=mock_tables), \
         patch('os.makedirs'), \
         patch('pandas.to_pickle'):
        result = main()
        assert result is True

def test_main_extraction_error():
    with patch('os.path.exists', return_value=True), \
         patch('transformer.extract_pdf.extract_tables_from_pdf', side_effect=Exception('Error')):
        result = main()
        assert result is False 