import { useState } from "react";
import "./App.css";

function App() {
  const [transcript, setTranscript] = useState("");
  const [reply, setReply] = useState("");
  const [loading, setLoading] = useState(false);

  const handleRecord = async () => {
    setLoading(true);
    setTranscript("");
    setReply("");

    try {
      const res = await fetch("http://localhost:5000/transcribe", {
        method: "POST",
      });
      const data = await res.json();

      if (data.error) {
        alert("❌ Transcription failed: " + data.error);
        setLoading(false);
        return;
      }

      setTranscript(data.text || "");

      setReply("⌛ Thinking...");

      // Wait a bit to simulate assistant typing
      setTimeout(() => {
        setReply(data.reply || "Assistant did not respond.");
      }, 800);
    } catch (error) {
      alert("⚠️ Something went wrong: " + error.message);
    }

    setLoading(false);
  };

  const handleClearMemory = async () => {
    const confirmClear = window.confirm("Are you sure you want to clear memory?");
    if (!confirmClear) return;

    await fetch("http://localhost:5000/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt: "clear memory" }),
    });

    setTranscript("");
    setReply("");
    alert("🧹 Memory cleared!");
  };

  return (
    <div className="app-container">
      <div className="card-ui">
        <h1>🧠 Local Voice Assistant: Tara</h1>

        <button
          className={`record-btn ${loading ? "loading" : ""}`}
          onClick={handleRecord}
          disabled={loading}
        >
          {loading ? "🎧 Listening & Thinking..." : "🎙️ Record & Ask"}
        </button>

        <div className="output">
          {transcript && (
            <p className="fade-in user-text">
              <strong>🗣️ You said:</strong> {transcript}
            </p>
          )}
          {reply && (
            <p className="fade-in bot-reply">
              <strong>🤖 Assistant:</strong> {reply}
            </p>
          )}
        </div>

        <button className="clear-btn" onClick={handleClearMemory}>
          🧼 Clear Memory
        </button>
      </div>
    </div>
  );
}

export default App;
