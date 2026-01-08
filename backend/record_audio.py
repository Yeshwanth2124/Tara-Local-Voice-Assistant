import sounddevice as sd
import wave

# Recording parameters
duration = 5  # seconds
samplerate = 16000  # Whisper's expected sample rate
channels = 1  # mono

filename = "output.wav"

print("🎙️ Recording started... Speak now.")
recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels, dtype='int16')
sd.wait()
print("✅ Recording finished.")

# Save to WAV file
with wave.open(filename, 'wb') as wf:
    wf.setnchannels(channels)
    wf.setsampwidth(2)  # 16-bit = 2 bytes
    wf.setframerate(samplerate)
    wf.writeframes(recording.tobytes())

print(f"📁 Audio saved as: {filename}")

