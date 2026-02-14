class BaseAgent:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def analyze(self, text: str):
        raise NotImplementedError("Each agent must implement analyze()")
