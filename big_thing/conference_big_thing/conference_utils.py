import pyaudio
import wave
import time


class AudioRecorder:
    def __init__(self, rate=44100, channels=2, chunk_size=1024) -> None:
        self.rate = rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.frames = []
        self.p = None
        self.stream = None

    def record(self, filename, duration):
        self.record_start()

        print("Recording...")

        start_time = time.time()
        while time.time() - start_time < duration:
            self.record_chunk()

        print("Finished recording.")

        self.record_end()
        self.save(filename)

    def record_start(self) -> None:
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk_size,
        )

        print("Recording started...")

    def record_end(self) -> None:
        print("Finished recording.")

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def save(self, filename: str) -> None:
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()

        print(f"Audio saved as {filename}")

    def record_chunk(self):
        data = self.stream.read(self.chunk_size)
        self.frames.append(data)


if __name__ == "__main__":
    recorder = AudioRecorder()
    recorder.record(filename='output.wav', duration=5)
