from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="qwen2.5:3b",   # replace with your model
)

print(llm.invoke("Hello"))