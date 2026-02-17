"""
Multilingual Translation Engine for ClauseAI
Supports: English, Tamil, Hindi, Telugu, Malayalam

Translates AI-generated legal analysis into multiple languages using IndicTrans2
"""

import os
import sys
import json
from typing import Dict, List, Any, Optional

# Fix Windows console UTF-8 encoding for emoji support
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
import hashlib
import pickle
from pathlib import Path

load_dotenv()

# Argos Translate - Ultra-fast offline translation without API limits
try:
    import argostranslate.package
    import argostranslate.translate
    ARGOS_AVAILABLE = True
except ImportError:
    ARGOS_AVAILABLE = False
    print("[WARNING] Argos Translate not available")

# IndicTrans2 not used - Argos Translate is fast enough
INDICTRANS_AVAILABLE = False


class OllamaLLMWrapper:
    """Wrapper to provide LangChain-like interface for local Ollama API"""
    def __init__(self, base_url, model):
        self.base_url = base_url
        self.model = model
        import requests
        self.requests = requests
    
    def invoke(self, messages, timeout=30):
        """Invoke Ollama API with LangChain-compatible message format
        
        Args:
            messages: LangChain-format messages
            timeout: Request timeout in seconds (default: 30s for gemma3:1b)
        """
        # Convert LangChain messages to Ollama format
        ollama_messages = []
        for msg in messages:
            if isinstance(msg, SystemMessage):
                ollama_messages.append({"role": "system", "content": msg.content})
            elif isinstance(msg, HumanMessage):
                ollama_messages.append({"role": "user", "content": msg.content})
        
        if not ollama_messages:
            raise Exception("Failed to convert messages")
        
        # Call local Ollama API
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": ollama_messages,
            "stream": False,
            "temperature": 0.1
        }
        
        # Use REDUCED timeout for fast gemma3:1b model (30 seconds max by default)
        # This prevents hanging on translation fallbacks
        response = self.requests.post(url, json=payload, timeout=timeout)
        response.raise_for_status()
        
        # Wrap response in LangChain format
        class OllamaResponse:
            def __init__(self, content):
                self.content = content
        
        data = response.json()
        return OllamaResponse(data.get('message', {}).get('content', ''))


class ArgosTranslator:
    """
    Fast offline translator using Argos Translate
    Lightweight ML models for instant translation
    """
    
    def __init__(self):
        """Initialize Argos Translate"""
        self.available = ARGOS_AVAILABLE
        
        if self.available:
            print("✅ Argos Translate ready (INSTANT translations - EN→TA/HI/TE/ML)")
        else:
            print("[WARNING] Argos Translate not available")
    
    def translate(self, text: str, src_lang: str, tgt_lang: str) -> str:
        """
        Translate text with Argos Translate
        Ultra-fast, offline translation with no API limits
        """
        if not self.available or not text:
            return text
        
        if src_lang == tgt_lang or tgt_lang == 'en':
            return text
        
        try:
            # Use Argos Translate - models download automatically on first use
            translated = argostranslate.translate.translate(text, src_lang, tgt_lang)
            
            # Return translation if successful
            if translated and isinstance(translated, str) and len(translated.strip()) > 0:
                return translated
            else:
                return text
            
        except Exception as e:
            # Silently fail and return original - models still downloading
            return text



class IndicTrans2Translator:
    """Specialized translator for Indian languages using IndicTrans2"""
    
    # Language code mapping for IndicTrans2
    LANGUAGE_CODES = {
        'ta': 'tam_Taml',  # Tamil
        'hi': 'hin_Deva',  # Hindi
        'te': 'tel_Telu',  # Telugu
        'ml': 'mal_Mlym',  # Malayalam
        'en': 'eng_Latn'   # English
    }
    
    def __init__(self):
        """Initialize IndicTrans2 translator"""
        self.available = False
        try:
            if INDICTRANS_AVAILABLE:
                print("🚀 Loading IndicTrans2 (specialized for Tamil/Hindi/Telugu/Malayalam)...")
                self.client = IndicTransClient(language="indic")
                self.available = True
                print("✅ IndicTrans2 initialized successfully")
            else:
                print("[WARNING] IndicTrans2 not available")
        except Exception as e:
            self.available = False
            print(f"[WARNING] IndicTrans2 init failed: {e}")
    
    def translate(self, text: str, src_lang: str, tgt_lang: str) -> str:
        """
        Translate text using IndicTrans2
        
        Args:
            text: Text to translate
            src_lang: Source language code (ta, hi, te, ml, en)
            tgt_lang: Target language code (ta, hi, te, ml, en)
            
        Returns:
            Translated text
        """
        if not self.available:
            return text
        
        if src_lang == tgt_lang or tgt_lang == 'en':
            return text
        
        try:
            src_code = self.LANGUAGE_CODES.get(src_lang, 'eng_Latn')
            tgt_code = self.LANGUAGE_CODES.get(tgt_lang, 'eng_Latn')
            
            # Split into chunks if too long
            if len(text) > 500:
                chunks = [text[i:i+500] for i in range(0, len(text), 500)]
                translated_chunks = []
                for chunk in chunks:
                    result = self.client.translate_paragraph(
                        chunk,
                        src_lang=src_code,
                        tgt_lang=tgt_code
                    )
                    translated_chunks.append(result)
                return ' '.join(translated_chunks)
            else:
                result = self.client.translate_paragraph(
                    text,
                    src_lang=src_code,
                    tgt_lang=tgt_code
                )
                return result
        except Exception as e:
            print(f"[WARNING] IndicTrans2 translation failed: {e}")
            return text





class MultilingualEngine:
    """
    Multilingual translation engine for ClauseAI
    Uses IndicTrans2 for Indian languages (Tamil, Hindi, Telugu, Malayalam)
    When user selects a language in app - entire analysis translates instantly!
    """
    
    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'ta': 'Tamil',
        'hi': 'Hindi',
        'te': 'Telugu',
        'ml': 'Malayalam'
    }
    
    # Maximum tokens per chunk for translation
    MAX_CHUNK_TOKENS = 1000
    
    def __init__(self, google_api_key: str = None):
        """Initialize the multilingual engine with Argos Translate (PRIMARY) + Ollama (FALLBACK ONLY)"""
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "gemma3:1b")
        
        if not self.ollama_base_url or not self.ollama_model:
            raise ValueError("Ollama configuration missing")
        
        # Ollama wrapper - FALLBACK ONLY (gemma3:1b is 1.1B params, FAST)
        # Used only for language detection & query translation (NOT main translation)
        self.llm = OllamaLLMWrapper(self.ollama_base_url, self.ollama_model)
        
        # Initialize Argos Translate (PRIMARY TRANSLATOR - INSTANT, offline, no API limits)
        self.translator = ArgosTranslator()
        
        self.current_llm_name = f"Argos Translate (PRIMARY: EN→TA/HI/TE/ML instant) + {self.ollama_model} (fallback only)"
        
        # Initialize cache directory
        self.cache_dir = Path(".translation_cache")
        self.cache_dir.mkdir(exist_ok=True)
        
        print(f"[OK] ✨ Multilingual Engine Ready!")
        print(f"   📊 Primary Translator: Argos Translate (INSTANT)")
        print(f"   🔄 Fallback LLM: {self.ollama_model} (fast, lightweight)")
        print(f"   ⚡ Translation: EN→TA/HI/TE/ML (0.01-1s per text)")

    
    def translate_text(self, text: str, target_language: str) -> str:
        """
        Translate text to target language - ENTIRE app content translates instantly!
        
        Args:
            text: Text to translate
            target_language: Target language code (ta, hi, te, ml, en)
            
        Returns:
            Translated text
        """
        if not text or target_language == 'en':
            return text
        
        if target_language not in self.SUPPORTED_LANGUAGES:
            print(f"[WARNING] Unsupported language: {target_language}, returning original text")
            return text
        
        # Check cache first
        cached = self._get_from_cache(text, target_language)
        if cached:
            return cached
        
        try:
            # Split long text into chunks
            if len(text) > 3000:  # Approximate token limit
                return self._translate_long_text(text, target_language)
            
            # Translate single chunk using IndicTrans2
            translated = self._translate_chunk(text, target_language)
            
            # Cache the translation
            self._save_to_cache(text, target_language, translated)
            
            return translated
            
        except Exception as e:
            print(f"[ERROR] Translation error: {str(e)}")
            return text  # Fallback to original text
    
    def _translate_chunk(self, text: str, target_language: str) -> str:
        """Translate a single chunk using Gemma LLM (for better quality) or Argos Translate (for speed)"""
        # Use LLM (Gemma) for all Indian languages - BETTER QUALITY
        if target_language in ['ta', 'hi', 'te', 'ml']:
            # Try Argos Translate first (fast)
            try:
                argos_translated = self.translator.translate(text, 'en', target_language)
                # If Argos translation looks good, use it
                if argos_translated and argos_translated != text and len(argos_translated.strip()) > 0:
                    # For short texts, use Argos directly (it's fast)
                    if len(text) < 200:
                        return argos_translated
                    # For longer texts, use LLM for better quality
            except Exception as e:
                print(f"[WARNING] Argos translation failed for {target_language}: {str(e)[:60]}")
            
            # Use Gemma LLM for better quality translation
            try:
                llm_translated = self._translate_with_llm(text, target_language)
                if llm_translated and llm_translated != text and len(llm_translated.strip()) > 0:
                    return llm_translated
            except Exception as e:
                print(f"[WARNING] LLM translation failed for {target_language}: {str(e)[:60]}")
        
        # If all methods fail, return original text
        return text
    
    def _translate_with_llm(self, text: str, target_language: str) -> str:
        """Translate text using Gemma LLM for better quality"""
        language_names = {
            'ta': 'Tamil',
            'hi': 'Hindi',
            'te': 'Telugu',
            'ml': 'Malayalam'
        }
        
        target_lang_name = language_names.get(target_language, target_language)
        
        system_prompt = f"""You are a professional translator specializing in translating English to {target_lang_name}.

Your task is to translate the following English text to {target_lang_name}. Provide ONLY the translation, no explanations or additional text.

Rules:
1. Preserve all numbers, percentages, and technical terms
2. Maintain the tone and formality of the original text
3. Ensure legal and business terminology is accurately translated
4. Keep proper nouns in their original form
5. Preserve formatting and structure"""

        user_prompt = f"""Translate this English text to {target_lang_name}:

{text}

Provide ONLY the {target_lang_name} translation:"""
        
        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            # Use longer timeout for translation (60 seconds for gemma3:1b)
            response = self.llm.invoke(messages, timeout=60)
            
            if response and response.content:
                translated = response.content.strip()
                # Remove any English text that might be in the response
                if translated and len(translated) > 0:
                    return translated
            
            return text
        except Exception as e:
            print(f"[ERROR] LLM translation error: {str(e)}")
            return text
    
    def _translate_long_text(self, text: str, target_language: str) -> str:
        """Translate long text by splitting into chunks"""
        # Split by paragraphs/sections
        chunks = []
        current_chunk = ""
        
        for line in text.split('\n'):
            if len(current_chunk) + len(line) > 2500:  # Leave buffer
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = line
            else:
                current_chunk += '\n' + line if current_chunk else line
        
        if current_chunk:
            chunks.append(current_chunk)
        
        # Translate each chunk
        translated_chunks = []
        for i, chunk in enumerate(chunks):
            print(f"   Translating to {self.SUPPORTED_LANGUAGES[target_language]} ({i+1}/{len(chunks)} sections)...")
            translated = self._translate_chunk(chunk, target_language)
            translated_chunks.append(translated)
        
        return '\n'.join(translated_chunks)
    
    def translate_json(self, data: Any, target_language: str) -> Any:
        """
        Recursively translate JSON data
        
        Args:
            data: Data to translate (dict, list, str, or primitive)
            target_language: Target language code
            
        Returns:
            Translated data with same structure
        """
        if target_language == 'en':
            return data
        
        if isinstance(data, dict):
            translated = {}
            for key, value in data.items():
                # Don't translate specific metadata keys
                if key in ['contract_id', 'file_type', 'timestamp', 'confidence', 
                          'overall_score', 'domain_scores', 'severity_breakdown']:
                    translated[key] = value
                else:
                    # Recursively translate all other values
                    translated[key] = self.translate_json(value, target_language)
            return translated
        
        elif isinstance(data, list):
            return [self.translate_json(item, target_language) for item in data]
        
        elif isinstance(data, str):
            # Translate all non-empty strings longer than 3 chars
            # Skip very short strings (likely codes/IDs)
            if len(data) > 3 and not data.isnumeric() and data not in ['en', 'ta', 'hi', 'te', 'ml']:
                return self.translate_text(data, target_language)
            return data
        
        else:
            # Primitives (numbers, booleans, None)
            return data
    
    def detect_language(self, text: str) -> str:
        """
        Detect language of text using gemma3:1b (FAST fallback only)
        
        Args:
            text: Text to analyze
            
        Returns:
            Language code (en, ta, hi, te, ml)
        """
        if not text or len(text) < 10:
            return 'en'
        
        try:
            system_prompt = """You are a language detection expert.
            
Detect the language of the given text and respond with ONLY the language code:
- 'en' for English
- 'ta' for Tamil
- 'hi' for Hindi
- 'te' for Telugu
- 'ml' for Malayalam

Respond with only the 2-letter code, nothing else."""

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"TEXT: {text[:500]}")  # First 500 chars
            ]
            
            # SHORT timeout (15s) for language detection - gemma3:1b is FAST
            response = self.llm.invoke(messages, timeout=15)
            detected = response.content.strip().lower()
            
            if detected in self.SUPPORTED_LANGUAGES:
                return detected
            return 'en'
            
        except Exception as e:
            print(f"[WARNING] Language detection timed out or failed: {str(e)[:50]}")
            return 'en'  # Fallback to English
    
    def translate_query_for_chat(self, query: str, source_language: str = None) -> str:
        """
        Translate user query to English for RAG/agent processing using gemma3:1b (FAST)
        
        Args:
            query: User query in any language
            source_language: Optional source language code
            
        Returns:
            Query in English
        """
        if not source_language:
            source_language = self.detect_language(query)
        
        if source_language == 'en':
            return query
        
        try:
            lang_name = self.SUPPORTED_LANGUAGES[source_language]
            
            system_prompt = f"""You are a translator.
            
The user asked a question about a legal contract in {lang_name}.
Translate this question to English for processing.

Requirements:
1. Preserve the meaning exactly
2. Keep legal terminology
3. Output only the English translation, nothing else"""

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"QUESTION: {query}")
            ]
            
            # SHORT timeout (20s) - gemma3:1b is lightweight model
            response = self.llm.invoke(messages, timeout=20)
            return response.content.strip()
            
        except Exception as e:
            print(f"[WARNING] Query translation timed out or failed: {str(e)[:50]}")
            # Fallback: return original query if translation fails
            return query
    
    def _get_cache_key(self, text: str, language: str) -> str:
        """Generate cache key for text and language"""
        content = f"{text}_{language}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _get_from_cache(self, text: str, language: str) -> Optional[str]:
        """Get translation from cache"""
        try:
            cache_key = self._get_cache_key(text, language)
            cache_file = self.cache_dir / f"{cache_key}.pkl"
            
            if cache_file.exists():
                with open(cache_file, 'rb') as f:
                    cached_data = pickle.load(f)
                    return cached_data.get('translation')
        except Exception as e:
            print(f"[WARNING] Cache read error: {str(e)}")
        
        return None
    
    def _save_to_cache(self, text: str, language: str, translation: str):
        """Save translation to cache"""
        try:
            cache_key = self._get_cache_key(text, language)
            cache_file = self.cache_dir / f"{cache_key}.pkl"
            
            cache_data = {
                'text': text,
                'language': language,
                'translation': translation
            }
            
            with open(cache_file, 'wb') as f:
                pickle.dump(cache_data, f)
        except Exception as e:
            print(f"[WARNING] Cache write error: {str(e)}")
    
    def clear_cache(self):
        """Clear translation cache"""
        try:
            for cache_file in self.cache_dir.glob("*.pkl"):
                cache_file.unlink()
            print("[OK] Translation cache cleared")
        except Exception as e:
            print(f"[ERROR] Error clearing cache: {str(e)}")


# Test function
if __name__ == "__main__":
    print("Multilingual Engine Test")
    print("=" * 60)
    
    engine = MultilingualEngine()
    
    # Test translation
    test_text = """The contract has identified several critical risks that require immediate attention. 
    The compliance risk score is 8.5 out of 10, indicating high regulatory concerns."""
    
    print("\nOriginal (English):")
    print(test_text)
    
    for lang_code, lang_name in engine.SUPPORTED_LANGUAGES.items():
        if lang_code != 'en':
            print(f"\n{lang_name} ({lang_code}):")
            translated = engine.translate_text(test_text, lang_code)
            print(translated)
    
    # Test JSON translation
    print("\n" + "=" * 60)
    print("JSON Translation Test:")
    test_json = {
        'summary': 'This is a critical contract',
        'risk_score': 7.5,
        'risks': ['Payment terms unclear', 'Missing liability clause']
    }
    
    print("\nOriginal JSON:")
    print(json.dumps(test_json, indent=2))
    
    print("\nTranslated to Tamil:")
    translated_json = engine.translate_json(test_json, 'ta')
    print(json.dumps(translated_json, indent=2, ensure_ascii=False))
