import sys
sys.path.append('utils')
from utils.data_loader import clean_text

def test_clean_text():
    result = clean_text("Hello! Test 123")
    assert result == "hello test"
    print("✅ test_clean_text passed!")

def test_clean_text_special():
    result = clean_text("Test@with#special$chars%")
    assert result == "testwithspecialchars"
    print("✅ test_clean_text_special passed!")