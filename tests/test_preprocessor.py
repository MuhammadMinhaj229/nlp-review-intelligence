import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.text_preprocessor import clean_text, preprocess_text

def test_clean_text():
    assert clean_text("<p>Hello World!</p>") == "hello world"
    assert clean_text("123 Test ---") == "test"
    assert clean_text("") == ""

def test_preprocess_text():
    assert "run dog" in preprocess_text("The running dogs")
    assert preprocess_text("") == ""
