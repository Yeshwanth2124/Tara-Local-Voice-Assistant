import asyncio
import wave
from wyoming.client import AsyncTcpClient
from wyoming.tts import Synthesize
from wyoming.audio import AudioChunk, AudioStart, AudioStop
import audioop  # at the top
import simpleaudio as sa

VOLUME_SCALING = 0.5  # 50% volume (0.0 to 1.0)


async def main():
    client = AsyncTcpClient("localhost", 10200)
    await client.connect()

    await client.write_event(Synthesize(text="Hello Yeshwanth, this is Piper speaking!").event())

    # Prepare for writing WAV file
    audio_data = bytearray()
    sample_rate = 22050  # Default Piper rate
    sample_width = 2     # 16-bit PCM
    channels = 1

    while True:
        event = await client.read_event()
        if event is None:
            break

        if AudioStart.is_type(event.type):
            print("🔊 Audio started")
            start = AudioStart.from_event(event)
            sample_rate = start.rate
            sample_width = start.width
            channels = start.channels

        elif AudioChunk.is_type(event.type):
            chunk = AudioChunk.from_event(event)
            print(f"🟩 Received audio chunk of {len(chunk.audio)} bytes")

            # Reduce volume here
            scaled_audio = audioop.mul(chunk.audio, sample_width, VOLUME_SCALING)
            audio_data.extend(scaled_audio)


        elif AudioStop.is_type(event.type):
            print("🔴 Audio stopped")
            break

    await client.disconnect()

    # Write audio to WAV file
    with wave.open("test_output.wav", "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data)

    print("✅ Audio saved as test_output.wav")


    # After writing to "output.wav"
    wave_obj = sa.WaveObject.from_wave_file("output.wav")
    play_obj = wave_obj.play()
    play_obj.wait_done()

if __name__ == "__main__":
    asyncio.run(main())
