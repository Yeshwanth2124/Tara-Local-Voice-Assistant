from flask import Flask, request, jsonify
from assistant import transcribe_audio, get_response, speak, append_to_memory, load_memory, save_memory
import os
import asyncio
from flask_cors import CORS
from pathlib import Path

app = Flask(__name__)
CORS(app)

from pathlib import Path
from assistant import main as assistant_main  # ✅ import the same pipeline

@app.route("/transcribe", methods=["POST"])
def transcribe():
    try:
        # 🎤 Start full pipeline (record → transcribe → respond → speak)
        asyncio.run(assistant_main())  # 🧠 This is your exact CLI logic!

        # Load transcription from output.txt
        with open("output.txt", "r", encoding="utf-8") as f:
            text = f.read().strip()

        # Load last reply from memory.json
        memory = load_memory()
        reply = memory[-1]["assistant"] if memory else "No reply found."

        return jsonify({"text": text, "reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        if not data or "prompt" not in data:
            return jsonify({"error": "Missing prompt"}), 400

        prompt = data["prompt"]

        if "clear memory" in prompt.lower():
            save_memory([])
            reply = "I have cleared all your memory."
        else:
            reply = get_response(prompt)
            append_to_memory(prompt, reply)

        asyncio.run(speak(reply))
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/memory", methods=["GET"])
def memory():
    return jsonify(load_memory())

if __name__ == "__main__":
    app.run(port=5000)
