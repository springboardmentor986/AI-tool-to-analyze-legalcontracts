# test_loaders.py

import os
import pytest
from src.clauseai.loaders import load_contract


# --- Test: Valid PDF File ---
def test_load_pdf():
    file_path = "tests/sample.pdf"   # make sure this file exists
    if not os.path.exists(file_path):
        pytest.skip("PDF file not found")

    result = load_contract(file_path)
    assert result is not None
    assert isinstance(result, str)
    assert len(result) > 0


# --- Test: Valid DOCX File ---
def test_load_docx():
    file_path = "tests/sample.docx"   # make sure this file exists
    if not os.path.exists(file_path):
        pytest.skip("DOCX file not found")

    result = load_contract(file_path)
    assert result is not None
    assert isinstance(result, str)
    assert len(result) > 0


# --- Test: Invalid File ---
def test_invalid_file():
    with pytest.raises(Exception):
        load_contract("invalid.txt")


# --- Test: Empty Input ---
def test_empty_input():
    with pytest.raises(Exception):
        load_contract("")
