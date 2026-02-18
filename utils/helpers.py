import ast
import re

def clean_raw_output(raw_data):
    """
    Robust cleaner for AI outputs, handling Lists, Dicts, and Strings.
    """
    text = str(raw_data).strip()
    
    # 1. Try standard Python parsing (SAFE)
    try:
        # If it looks like a list or dict, parse it
        if (text.startswith("{") and text.endswith("}")) or (text.startswith("[") and text.endswith("]")):
            parsed = ast.literal_eval(text)
            
            # Case: List of dicts [{'type': 'text', 'text': '...'}]
            if isinstance(parsed, list) and len(parsed) > 0:
                if isinstance(parsed[0], dict):
                    return parsed[0].get('text', str(parsed[0]))
                return str(parsed[0])
            
            # Case: Dict {'text': '...'}
            if isinstance(parsed, dict):
                return parsed.get('text', str(parsed))
    except:
        pass

    # 2. Brute Force Cleaning (Fallback)
    # Remove [{...}] wrappers if parsing failed
    text = re.sub(r"^\[\s*\{'type':\s*'text',\s*'text':\s*", "", text) # Start
    text = re.sub(r"\}\]\s*$", "", text) # End
    
    # Remove simple dict wrappers
    if "{'type': 'text', 'text':" in text:
        start = text.find("'text': '")
        if start != -1: text = text[start + 9:]
    
    # Remove signatures
    extras_markers = ["', 'extras':", '", "extras":', "', 'type':"]
    for marker in extras_markers:
        if marker in text: text = text.split(marker)[0]

    # 3. Final Polish
    # Fix escaped newlines and quotes
    text = text.replace("\\n", "\n").replace("\\'", "'")
    
    # Remove trailing quotes/brackets from sloppy slicing
    text = text.rstrip("'\"}]")
    
    return text.strip()