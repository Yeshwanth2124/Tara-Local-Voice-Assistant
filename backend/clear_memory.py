import os
import json

MEMORY_PATH = "memory.json"

def clear_memory():
    if os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, "w") as f:
            json.dump([], f)
        print("🧠 Memory cleared.")
    else:
        print("ℹ️ No memory file found to clear.")

if __name__ == "__main__":
    clear_memory()
