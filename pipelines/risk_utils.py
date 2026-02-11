#Common helper functions 
#Convert text risk → numeric risk and Shared by all pipelines


def assess_risk_level(risk_level: str) -> int:
    mapping = {
        "low": 1,
        "medium": 2,
        "high": 3
    }
    return mapping.get(risk_level.lower(), 0)
