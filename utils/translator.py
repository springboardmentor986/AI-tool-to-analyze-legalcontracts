import streamlit as st
from deep_translator import GoogleTranslator
import requests
import urllib3
import ssl

# Suppress SSL warnings due to corporate proxies
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Universally bypass SSL verification at the standard library level (covers requests, urllib, etc.)
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Gujarati": "gu"
}

@st.cache_data(show_spinner=False)
def translate_text(text, target_lang_code):
    """
    Translates text to the target language chunk by chunk to bypass module limits.
    Returns the original text if target is 'en' or if translation fails.
    """
    if not text or not isinstance(text, str) or target_lang_code == 'en':
        return text
        
    try:
        translator = GoogleTranslator(source='auto', target=target_lang_code)
        
        # Split by double newline to preserve markdown paragraphs
        paragraphs = text.split('\n\n')
        translated_paragraphs = []
        
        for p in paragraphs:
            if not p.strip():
                translated_paragraphs.append("")
                continue
                
            # Deep translator has a length limit per request (usually 5000 chars)
            if len(p) > 4800:
                # Chunk large paragraphs
                chunks = [p[i:i+4800] for i in range(0, len(p), 4800)]
                trans_chunks = []
                for c in chunks:
                    res = translator.translate(c)
                    # If translation fails and returns None, fallback to the original chunk
                    trans_chunks.append(res if res is not None else c)
                translated_paragraphs.append("".join(trans_chunks))
            else:
                res = translator.translate(p)
                translated_paragraphs.append(res if res is not None else p)
                
        return '\n\n'.join(translated_paragraphs)
    except Exception as e:
        # Fallback to original text with an error note if API fails
        return f"*(Translation Engine Unavailable: {e})*\n\n{text}"
