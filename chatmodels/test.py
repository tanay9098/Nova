from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

from langchain.chat_models import init_chat_model

from langchain_mistralai import ChatMistralAI

model = init_chat_model("gpt-4.1", temperature=0.9, max_tokens=150)
model2=ChatMistralAI(model_name="mistral-small-2506", temperature=0.9, max_tokens=150)

print("Model initialized:", model)
print("Model2 initialized:", model2)


response = model.invoke("Write a short poem about the beauty of nature.")
print("Response:", response)
response2 = model2.invoke("Write a short story about a robot learning to paint.")
print("Response2:", response2)