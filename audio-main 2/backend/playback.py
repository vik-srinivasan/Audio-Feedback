import os
import pyaudio
import wave
import gtts
import pydub
from gtts import gTTS
from pydub import AudioSegment

class Playback:
    """Class for handling text-to-speech playback."""

    def __init__(self):
        """Initialize Playback settings."""
        self.audio_file_mp3 = "transcription_playback.mp3"
        self.audio_file_wav = "transcription_playback.wav"

    def text_to_speech(self, text, speed):
        """Convert text to speech and save it as an MP3 file, then convert to WAV."""
        # Generate speech and save as MP3
        tts = gtts.gTTS(text=text, lang='en')
        tts.save(self.audio_file_mp3)

        # Convert MP3 to WAV
        sound = pydub.AudioSegment.from_mp3(self.audio_file_mp3)
        if speed != 1.0:
            sound = sound.speedup(playback_speed=speed)
        sound.export(self.audio_file_wav, format="wav")

    def play_audio(self):
        """Play the generated WAV audio file using pyaudio."""
        chunk = 1024  # Define chunk size for playback
        wf = wave.open(self.audio_file_wav, 'rb')
        p = pyaudio.PyAudio()

        # Open a stream to play audio
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        # Read audio in chunks and play
        data = wf.readframes(chunk)
        while data:
            stream.write(data)
            data = wf.readframes(chunk)

        # Cleanup
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf.close()

    def playback_transcription(self, text):
        """Convert text to speech, convert format, and play it back."""
        self.text_to_speech(text, speed=1.3)
        self.play_audio()

    def cleanup(self):
        """Remove the audio files after playback."""
        if os.path.exists(self.audio_file_mp3):
            os.remove(self.audio_file_mp3)
        if os.path.exists(self.audio_file_wav):
            os.remove(self.audio_file_wav)
