import wave
from wyoming.client import AsyncTcpClient
from wyoming.audio import AudioChunk, AudioStop
from wyoming.event import Event
import asyncio
from dataclasses import dataclass
import simpleaudio as sa
@dataclass
class Synthesize:
    text: str

    def to_event(self) -> Event:
        return Event(type="synthesize", data={"text": self.text})

    @staticmethod
    def from_event(event: Event) -> "Synthesize":
        assert event.type == "synthesize"
        return Synthesize(text=event.data["text"])
async def speak(text, output_file="test_output.wav"):
    client = AsyncTcpClient("localhost", 10200)
    await client.connect()

    await client.write_event(Synthesize(text=text).to_event())

    with wave.open(output_file, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(22050)

        while True:
            event = await client.read_event()
            if event is None:
                break
            if AudioChunk.is_type(event.type):
                chunk = AudioChunk.from_event(event)
                wav_file.writeframes(chunk.audio)
            elif AudioStop.is_type(event.type):
                break

    await client.disconnect()

    # 🔊 Auto-play after TTS synthesis
    wave_obj = sa.WaveObject.from_wave_file(output_file)
    play_obj = wave_obj.play()
    play_obj.wait_done()
