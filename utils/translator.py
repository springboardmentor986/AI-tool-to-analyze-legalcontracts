import ast
import re
import copy  # <--- CRITICAL FIX for Shallow Copy Bug
from utils.universal_llm import universal_llm 

# --- 1. UNIVERSAL CLEANING (Sanitizer) ---
def clean_for_translation(raw_data):
    """
    Strips JSON, List wrappers, and signatures.
    Ensures the LLM only translates pure text.
    """
    if raw_data is None: return ""
    text = str(raw_data).strip()
    
    # Parse Dict/List
    try:
        if (text.startswith("{") and text.endswith("}")) or (text.startswith("[") and text.endswith("]")):
            parsed = ast.literal_eval(text)
            if isinstance(parsed, list) and len(parsed) > 0:
                text = parsed[0].get('text', str(parsed[0])) if isinstance(parsed[0], dict) else str(parsed[0])
            elif isinstance(parsed, dict):
                text = parsed.get('text', str(parsed))
    except:
        pass 

    # Brute force cleanup
    if "{'type': 'text'" in text:
        start = text.find("'text': '")
        if start != -1: text = text[start + 9:]
    
    for marker in ["', 'extras':", '", "extras":', "', 'type':"]:
        if marker in text: text = text.split(marker)[0]

    # Format cleanup
    text = text.replace("\\n", "\n").replace("\\'", "'").replace('"', '"').replace("'", "'")
    text = text.rstrip("'\"}]")
    text = text.replace("**", "").replace("###", "") 
    
    return text.strip()

# --- 2. TRANSLATION LOGIC ---
def translate_report(report_data, target_lang):
    """
    Iterates through the report, cleans text, and translates using the Bulletproof LLM.
    Uses DEEPCOPY to prevent overwriting the original English data.
    """
    if target_lang == "English":
        return report_data

    # CRITICAL FIX: Use deepcopy to unlink from the original data
    # This prevents the "English becomes Tamil permanently" bug.
    translated_data = copy.deepcopy(report_data)

    sections = ["synthesis", "legal", "finance", "compliance", "operations"]
    
    # Prompt Template
    prompt_base = """
    You are an expert legal translator. Translate the following text into {language}.
    Maintain the strict legal meaning but use natural phrasing for that language.
    IMPORTANT: Return ONLY the translated text. Do not add explanations.
    
    Text to translate:
    {text}
    """
    
    for section in sections:
        if section in translated_data:
            # Always grab the summary from the ORIGINAL source to ensure we translate English -> Target
            # (Instead of translating Tamil -> Hindi, which degrades quality)
            raw_original = report_data.get(section, {}).get("summary", "")
            
            # Step A: Clean
            clean_original = clean_for_translation(raw_original)
            
            if clean_original:
                # Format the prompt
                final_prompt = prompt_base.format(language=target_lang, text=clean_original)
                
                try:
                    # Step B: Call Universal LLM
                    response = universal_llm.invoke(final_prompt)
                    translated_data[section]["summary"] = response.content
                except Exception as e:
                    print(f"❌ Translation failed for section {section}: {e}")
                    # Keep original text if translation fails completely
                    translated_data[section]["summary"] = clean_original 

    return translated_data