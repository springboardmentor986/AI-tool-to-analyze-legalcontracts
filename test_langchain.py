from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a legal assistant"),
    ("human", "Explain a contract clause")
])

print("LangChain core loaded successfully")
print("Prompt created:", prompt is not None)
