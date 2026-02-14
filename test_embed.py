from gemini_llm import embed_text

vec = embed_text("hello world")
print(len(vec))
print(vec[:5])
