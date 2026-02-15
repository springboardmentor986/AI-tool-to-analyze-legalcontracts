def calculate_risk_score(text):
    risk_keywords = ["penalty", "termination", "liability", "breach"]

    score = 0
    for word in risk_keywords:
        if word in text.lower():
            score += 1

    return score * 25
