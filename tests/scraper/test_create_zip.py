import pytest
from unittest.mock import patch, mock_open, Mock
import os
from scraper.create_zip import create_zip, main

def test_create_zip():
    mock_pdf_files = ['test1.pdf', 'test2.pdf']
    
    with patch('os.listdir', return_value=mock_pdf_files), \
         patch('zipfile.ZipFile') as mock_zipfile, \
         patch('os.path.join', side_effect=lambda *args: '/'.join(args)):
        
        create_zip('pdf_dir', 'test.zip')
        
        mock_zipfile.assert_called_once_with('test.zip', 'w')
        
        mock_zip = mock_zipfile.return_value.__enter__.return_value
        assert mock_zip.write.call_count == 2

def test_main_with_pdfs():
    mock_pdf_files = ['test1.pdf', 'test2.pdf']
    
    with patch('os.path.exists', return_value=True), \
         patch('os.listdir', return_value=mock_pdf_files), \
         patch('os.makedirs'), \
         patch('scraper.create_zip.create_zip') as mock_create_zip:
        
        main()
        
        mock_create_zip.assert_called_once()

def test_main_no_pdfs():
    with patch('os.path.exists', return_value=True), \
         patch('os.listdir', return_value=[]), \
         patch('os.makedirs'):
        
        main()

def test_main_directory_not_found():
    with patch('os.path.exists', return_value=False), \
         patch('os.makedirs'):
        main()

def test_create_zip_with_mixed_files():
    mock_files = ['test1.pdf', 'test2.txt', 'test3.PDF']
    
    with patch('os.listdir', return_value=mock_files), \
         patch('zipfile.ZipFile') as mock_zipfile, \
         patch('os.path.join', side_effect=lambda *args: '/'.join(args)):
        
        create_zip('pdf_dir', 'test.zip')
        
        mock_zip = mock_zipfile.return_value.__enter__.return_value
        assert mock_zip.write.call_count == 2 