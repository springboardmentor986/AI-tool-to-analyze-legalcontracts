def chunk_text_for_ui(text, size=500):
    return [text[i:i+size] for i in range(0, len(text), size)]