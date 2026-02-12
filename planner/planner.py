def create_plan(domains: list[str]) -> list[str]:
    allowed = {"legal", "finance", "compliance", "operations"}
    return [d for d in domains if d in allowed]


