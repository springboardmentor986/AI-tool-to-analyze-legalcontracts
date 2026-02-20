from modules.parallel_processor import analyze_parallel

def run_clauseai(text, tone, focus):
    result = analyze_parallel(text, tone, focus)
    return result
