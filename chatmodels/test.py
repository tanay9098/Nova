from urllib import response

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


from langchain_mistralai import ChatMistralAI

model=ChatMistralAI(model_name="mistral-small-2506", temperature=0.9, max_tokens=150)

messages_history=[]

print("Model initialized:", model)

while True:
    print("Type 'exit' to quit.")

    prompt=input("You: ")
    messages_history.append(prompt)
    if prompt.lower() == "exit":
        break
    response = model.invoke(messages_history)
    messages_history.append(response.content)
    print("Response:", response.content)
