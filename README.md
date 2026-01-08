# 🤖 TARA – Memo-Local Voice Assistant

TARA is a fully offline, privacy-first voice assistant that listens, thinks, speaks, and remembers — without relying on cloud services. It uses **Whisper.cpp** for speech-to-text, **LLaMA3** (via Ollama) for intelligence, and **Piper TTS** for voice output.

---

## 📌 Features

- 🎙️ **Voice-to-Text (STT)**: High-performance local transcription via Whisper.cpp.
- 🤖 **Local Intelligence**: Powered by LLaMA3:8B using Ollama.
- 🧠 **Persistent Memory**: Remembers your conversations in a local `memory.json` file.
- 🔊 **Text-to-Speech (TTS)**: High-quality, low-latency speech using Piper (running in Docker).
- 🌐 **Flask API**: Web interface for interaction and memory management.
- 🔐 **100% Offline**: No data leaves your machine.
  
---

## 🛠️ Technologies Used

| Component            |        Tool / Framework             |
|----------------------|-------------------------------------|
| **Audio Recording**  | `sounddevice`, `wave` (Python)      |
| **Transcription**    | `whisper.cpp` + `ggml-base.en.bin`  |
| **LLM Inference**    | `LLaMA3` via `Ollama` (localhost API)|
| **Backend**          | `Flask`, `asyncio`, `json`          |
| **TTS**              | `Piper` (Docker) + Wyoming Protocol |
| **Memory Storage**   | Local `memory.json` file            |
| **API Testing**      | Postman, Browser                    |

---

## 🧩 Architecture Overview

![archtara1](https://github.com/user-attachments/assets/27b45a43-6838-40f1-9dd0-1ecdc252e5cf)

## WorkFlow

1. 🎧 **`record_audio.py`** captures user audio as `output.wav`
2. 🧠 **`whisper.cpp`** transcribes the audio → `output.txt`
3. 🧩 **`assistant.py`** processes the text:
   - If "clear memory" → clears `memory.json`
   - Else → sends context + prompt to LLaMA3 via Ollama
4. 🧠 Response is saved in memory (`memory.json`)
5. 🔊 Reply is spoken via Piper TTS and played back
6. 🌐 Optional: Interact via REST API

---

## 🌐 Flask API Endpoints

| Method | Route         | Description                                   |
|--------|---------------|---------------------------------------------- |
| POST   | `/transcribe` | Runs full pipeline (record → respond → speak) |
| POST   | `/ask`        | Accepts direct text input, responds & speaks  |
| GET    | `/memory`     | Returns recent conversation history           |

---

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:

1.  **Python 3.9+**: [Download Python](https://www.python.org/downloads/)
2.  **Docker Desktop**: [Download Docker](https://www.docker.com/products/docker-desktop/) (Required for Piper TTS)
3.  **Git**: [Download Git](https://git-scm.com/downloads)
4.  **Ollama**: [Download Ollama](https://ollama.com/) (For running LLaMA3)
5.  **C++ Build Tools**: (Required for building Whisper.cpp)
    *   *Windows*: Install Visual Studio 2019/2022 Community with "Desktop development with C++".

---

## 🚀 Installation & Setup

### 1. Clone the Repository

Open your terminal (PowerShell or Command Prompt) and run:

```bash
git clone https://github.com/your-username/tara-voice-assistant.git
cd tara-voice-assistant
```

### 2. Set Up Python Environment

Create a virtual environment to keep dependencies isolated:

```bash
python -m venv venv
```

Activate the virtual environment:
*   **Windows**: `.\venv\Scripts\activate`
*   **Mac/Linux**: `source venv/bin/activate`

### 3. Install Python Dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Build Whisper.cpp (Speech-to-Text)

You need to compile the Whisper engine locally.

1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```
2.  Clone and build `whisper.cpp`:
    ```bash
    git clone https://github.com/ggerganov/whisper.cpp
    cd whisper.cpp
    cmake -B build
    cmake --build build --config Release
    ```
    *(Note: This creates the `whisper-cli.exe` executable inside `build/bin/Release/`).*

### 5. Download the Whisper Model

While inside the `whisper.cpp` directory, download the base English model:

*   **Windows (PowerShell)**:
    ```powershell
    # Download the model downloader script if not present, then run it
    python models/download-ggml-model.py base.en
    ```
    *Alternatively, manually download `ggml-base.en.bin` from [Hugging Face](https://huggingface.co/ggerganov/whisper.cpp) and place it in `backend/models/` folder.*

    **Important**: Ensure `ggml-base.en.bin` is moved to the `backend/models/` folder so the application can find it.
    ```bash
    # Move model to correct location (adjust path as needed)
    move models/ggml-base.en.bin ../models/
    ```

### 6. Set Up Piper TTS (Text-to-Speech)

We use Docker to run the Piper TTS server. This is the easiest and most reliable method.

Run the following command in your terminal:

```bash
docker run -it --rm -v "$HOME/piper/voices:/voices" -p 10200:10200 rhasspy/wyoming-piper --voice en/en_US-lessac-medium
```

*   **What this does**:
    *   Downloads the `rhasspy/wyoming-piper` image.
    *   Starts a server on port `10200`.
    *   Uses the `en_US-lessac-medium` voice.

### 7. Set Up Ollama (LLaMA3 Model)

1.  Ensure Ollama is running (check your system tray or run `ollama serve`).
2.  Pull the LLaMA3 model:
    ```bash
    ollama run llama3:8b
    ```
    *(After the model downloads and you see a prompt `>>>`, you can type `/bye` to exit the chat, but keep the Ollama background service running).*

---

## ▶️ Running the Assistant

Once everything is set up:

1.  **Start the Backend**:
    Make sure your virtual environment is activated (`.\venv\Scripts\activate`).
    ```bash
    cd backend
    python assistant.py
    ```

    *The assistant will now be listening. Speak into your microphone!*

2.  **Start the Flask API (Optional)**:
    If you want to use the web interface or API endpoints:
    ```bash
    python app.py
    ```

## 📁 Project Structure

```
.
├── backend/                  # Python backend
│   ├── app.py                # Flask API
│   ├── assistant.py          # Main logic (STT -> LLM -> TTS)
│   ├── record_audio.py       # Audio recorder script
│   ├── my_tts.py             # Client for Piper TTS (Wyoming protocol)
│   ├── llm.py                # Interface for Ollama (LLaMA3)
│   ├── memory.json           # Conversation memory
│   ├── models/               # Directory for Whisper binary models
│   └── whisper.cpp/          # Source code for Whisper engine
├── frontend/                 # React frontend
│   ├── src/
│   └── public/
└── README.md
```

## 🤝 Contributions
Contributions are welcome!
1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Submit a pull request.

## Author

**Yeshwanth Goud**

*Data Scientist | Full Stack & ML Enthusiast*
