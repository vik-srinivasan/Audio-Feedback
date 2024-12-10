from backend.transcriber import Transcriber

def test_transcription():
    # Instantiate the transcriber
    transcriber = Transcriber()

    # Path to the test audio file
    audio_file = "output4.wav"

    # Transcribe the audio and print the result
    transcription = transcriber.transcribe_audio(audio_file)
    print("Transcription Result:", transcription)

# Run the test
if __name__ == "__main__":
    test_transcription()
