import pytest
import sys
sys.path.append('.')
from src.text_preprocessor import clean_text, preprocess_text

def test_clean_text():
    assert clean_text("<p>Hello World!</p>") == "hello world"
    assert clean_text("123 Test ---") == "test"
    assert clean_text("") == ""

def test_preprocess_text():
    # 'running' lemmatized to 'run', 'dogs' to 'dog', 'the' is stopword
    assert "run dog" in preprocess_text("The running dogs")
    assert preprocess_text("") == ""
