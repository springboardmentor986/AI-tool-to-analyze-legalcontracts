def build_prompt(content, tone, focus, structure):

    return f"""
    Generate a {structure} contract report.
    Tone: {tone}
    Focus Area: {focus}

    Contract Content:
    {content}
    """
