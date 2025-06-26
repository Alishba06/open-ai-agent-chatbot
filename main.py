import os
import chainlit as cl
import requests
from dotenv import load_dotenv

# Load .env and get API key
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# Model name
model_name = "mistralai/mistral-7b-instruct"

headers = {
    "Authorization": f"Bearer {api_key}",
    "HTTP-Referer": "http://localhost:8000",  # Optional
    "Content-Type": "application/json"
}

@cl.on_chat_start
async def start():
    cl.user_session.set("history", [])
    await cl.Message(" Chatbot is ready using Mistral 7B!").send()

@cl.on_message
async def on_message(message: cl.Message):
    history = cl.user_session.get("history")
    history.append({"role": "user", "content": message.content})

    payload = {
        "model": model_name,
        "messages": history
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload
    )

    res = response.json()
    bot_msg = res["choices"][0]["message"]["content"]
    history.append({"role": "assistant", "content": bot_msg})
    await cl.Message(bot_msg).send()