import speech_recognition
import os

class Transcriber:
    """Class responsible for transcribing recorded audio using Google Web Speech API."""

    def __init__(self):
        """Initialize the recognizer for Google Web Speech API."""
        self.recognizer = speech_recognition.Recognizer()

    def transcribe_audio(self, audio_file):
        """Transcribe the given audio file using Google Web Speech API."""
        try:
            # Load the audio file
            with speech_recognition.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)  # Record the audio from the file

            # Use Google Web Speech API to transcribe the audio
            text = self.recognizer.recognize_google(audio)
            return text  # Return the transcribed text

        except speech_recognition.UnknownValueError:
            print("Google Web Speech API could not understand the audio")
            return "Transcription failed: Audio not understood."

        except speech_recognition.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")
            return f"Transcription failed: {e}"

