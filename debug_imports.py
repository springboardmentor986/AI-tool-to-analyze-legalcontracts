print("1. Starting imports...")

try:
    import os
    print("2. os imported")
except Exception as e:
    print(f"❌ os failed: {e}")

try:
    from dotenv import load_dotenv
    print("3. dotenv imported")
except Exception as e:
    print(f"❌ dotenv failed: {e}")

try:
    print("4. Attempting langchain_groq...")
    from langchain_groq import ChatGroq
    print("✅ langchain_groq SUCCESS")
except Exception as e:
    print(f"❌ langchain_groq FAILED: {e}")

try:
    print("5. Attempting langchain_google_genai...")
    from langchain_google_genai import ChatGoogleGenerativeAI
    print("✅ langchain_google_genai SUCCESS")
except Exception as e:
    print(f"❌ langchain_google_genai FAILED: {e}")

try:
    print("6. Attempting langchain_openai...")
    from langchain_openai import ChatOpenAI
    print("✅ langchain_openai SUCCESS")
except Exception as e:
    print(f"❌ langchain_openai FAILED: {e}")

try:
    print("7. Attempting langchain_huggingface...")
    from langchain_huggingface import HuggingFaceEndpoint
    print("✅ langchain_huggingface SUCCESS")
except Exception as e:
    print(f"❌ langchain_huggingface FAILED: {e}")

try:
    print("8. Attempting langchain_community (Ollama)...")
    from langchain_community.chat_models import ChatOllama
    print("✅ langchain_community SUCCESS")
except Exception as e:
    print(f"❌ langchain_community FAILED: {e}")

print("9. DONE.")