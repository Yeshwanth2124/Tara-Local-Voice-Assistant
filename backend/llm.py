import requests
import json
import os

MEMORY_PATH = "memory.json"

def load_memory(limit=5):
    if not os.path.exists(MEMORY_PATH):
        return []
    with open(MEMORY_PATH, "r") as f:
        memory = json.load(f)
    return memory[-limit:]  # Keep only the latest `limit` interactions

def save_to_memory(user: str, assistant: str):
    memory = load_memory(limit=100)  # Keep longer memory but limit context window
    memory.append({"user": user, "assistant": assistant})
    with open(MEMORY_PATH, "w") as f:
        json.dump(memory, f, indent=2)

def get_response(user_input: str) -> str:
    memory = load_memory(limit=5)  # Load only the last 5 for prompt context

    # Build conversation context
    context = ""
    for turn in memory:
        context += f"User: {turn['user']}\nAssistant: {turn['assistant']}\n"
    context += f"User: {user_input}\nAssistant:"

    # Call Ollama API
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3:8b",  # Change if using a different model
            "prompt": context,
            "stream": False
        }
    )

    data = response.json()

    if "response" not in data or not isinstance(data["response"], str):
        print("⚠️ Unexpected response format:", data)
        return "Sorry, I couldn't process your request."

    reply = data["response"].strip()

    # Save the interaction
    save_to_memory(user_input, reply)

    return reply
