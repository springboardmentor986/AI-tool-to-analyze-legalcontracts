print("--- SYSTEM START ---")
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEndpoint
from langchain_community.chat_models import ChatOllama

# Load environment variables
load_dotenv()

class BulletproofLLM:
    def __init__(self):
        # PRIORITY 1: GROQ (Fastest, Best for Demo)
        # ---------------------------------------------------------
        self.groq = {
            "name": "Groq (Llama 3.1)",
            "builder": lambda: ChatGroq(
                model="llama-3.1-8b-instant",
                api_key=os.getenv("groq_api_key"),
                temperature=0.3
            )
        }

        # PRIORITY 2: GOOGLE (Your Backup that passed testing)
        # ---------------------------------------------------------
        self.google = {
            "name": "Google (Gemini 3 Flash)",
            "builder": lambda: ChatGoogleGenerativeAI(
                model="gemini-3-flash-preview", 
                google_api_key=os.getenv("gemini_api_key"),
                temperature=0.3
            )
        }

        # PRIORITY 3: OPENROUTER (Universal Backup)
        # ---------------------------------------------------------
        self.openrouter = {
            "name": "OpenRouter (DeepSeek)",
            "builder": lambda: ChatOpenAI(
                model="tngtech/deepseek-r1t2-chimera:free",
                api_key=os.getenv("openrouter_api_key"),
                base_url="https://openrouter.ai/api/v1",
                temperature=0.3
            )
        }

        # PRIORITY 4: HUGGING FACE (FIXED)
        # ---------------------------------------------------------
        # Fix: Removed 'task' parameter to let HF auto-detect.
        # Changed model to Zephyr (very stable on free tier) if Mistral fails.
        self.hf = {
            "name": "Hugging Face (Mistral/Zephyr)",
            "builder": lambda: HuggingFaceEndpoint(
                repo_id="HuggingFaceH4/zephyr-7b-beta", # Extremely reliable free model
                huggingfacehub_api_token=os.getenv("hugging_face_api_key"),
                temperature=0.1
                # Removed 'task' param so it defaults correctly
            )
        }

        # PRIORITY 5: LOCAL OLLAMA (The "Nuclear Option")
        # ---------------------------------------------------------
        # Works even if WiFi is disconnected!
        self.ollama = {
            "name": "Local Laptop (Ollama Llama2)",
            "builder": lambda: ChatOllama(
                model="llama3.2",
                temperature=0.3
            )
        }

        # The Order of Battle: Groq -> Google -> OpenRouter -> HF -> Ollama
        self.providers = [self.groq, self.google, self.openrouter, self.hf, self.ollama]

    def invoke(self, prompt):
        errors = []
        for provider in self.providers:
            try:
                # 1. Build the model
                llm = provider["builder"]()
                
                # 2. Try to run it
                print(f"🔄 Trying {provider['name']}...")
                response = llm.invoke(prompt)
                
                # 3. Success!
                print(f"✅ Success with {provider['name']}")
                return response
                
            except Exception as e:
                # Log error but KEEP GOING
                print(f"⚠️ Failed {provider['name']}: {str(e)}")
                errors.append(f"{provider['name']}: {str(e)}")
                continue
        
        # If we get here, literally everything failed (even your laptop).
        raise Exception(f"💀 All 5 AI Models Failed. Errors: {errors}")

# Export the singleton
universal_llm = BulletproofLLM()