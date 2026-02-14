from extract_text import extract_text
from gemini_llm import analyze_text

def analyze_contract(file_path: str):
    text = extract_text(file_path)
    analysis = analyze_text(text)
    return analysis

if __name__ == "__main__":
    result = analyze_contract("sample_contracts/sample1.txt")
    print(result)
