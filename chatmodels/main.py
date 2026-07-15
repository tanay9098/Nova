from urllib import response

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file




from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
model=ChatMistralAI(model_name="mistral-small-2506", temperature=0.9, max_tokens=150)

messages_history=[
    SystemMessage(content="You are an extraterrestrial species from an advanced civilization helping human beings to navigate their day to day life problems with philosophical insights."),
]

print("Model initialized:", model)

while True:
    print("Type 'exit' to quit.")

    prompt=input("You: ")
    messages_history.append(HumanMessage(content=prompt))
    if prompt.lower() == "exit":
        break
    response = model.invoke(messages_history)
    messages_history.append(AIMessage(content=response.content))
    print("Response:", response.content)
