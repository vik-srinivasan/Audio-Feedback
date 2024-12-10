import os
from dotenv import load_dotenv
from .recorder import AudioRecorder
from .transcriber import Transcriber
from .ner_manager import NERManager
from .playback import Playback
import google.generativeai as genai
from .utils import spell_out

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_KEY'))

class VoiceDictationTool:
    """Main class for handling the voice dictation tool with NER functionality."""

    def __init__(self, proper_nouns=False):
        """Initialize the VoiceDictationTool with necessary parameters."""
        self.audio_recorder = AudioRecorder()
        self.transcriber = Transcriber()
        self.ner_manager = NERManager()
        self.playback = Playback()
        self.transcription = ""
        self.proper_nouns = []
        self.proper_nouns_enabled = proper_nouns

    def start_recording(self):
        """Start recording the user's voice for the dictated text."""
        self.audio_recorder.start_recording()

    def stop_recording(self):
        """Stop recording and process the audio for transcription and NER."""

        print("Recording stopped...")
        self.audio_recorder.stop_recording()
        self.audio_recorder.save_audio()

        self.transcription = self.transcriber.transcribe_audio(self.audio_recorder.audio_file)
        if self.transcription:
            print(f"Transcription: {self.transcription}")
            self.proper_nouns = self.ner_manager.extract_proper_nouns(self.transcription)
            print(f"Proper Nouns: {self.proper_nouns}")

            if self.proper_nouns_enabled == 0:
                self.playback.playback_transcription(self.transcription)
            elif self.proper_nouns_enabled == 1:
                self.playback.playback_transcription(self.transcription)
                self.playback.playback_transcription('Proper nouns are: ' + ', '.join(self.proper_nouns))
            elif self.proper_nouns_enabled == 2:
                self.playback.playback_transcription(self.transcription)
                self.playback.playback_transcription('Proper nouns are: ' + ', '.join(self.proper_nouns))
                for noun in self.proper_nouns:
                    spelled_out = spell_out(noun)
                    self.playback.playback_transcription(f"{noun} is {spelled_out}")
                self.playback.playback_transcription('Is there anything you would like to fix?')

            self.playback.cleanup()
        else:
            print("Transcription failed.")
        return self.transcription, self.proper_nouns

    def start_fix_recording(self):
        """Start recording the user's voice for the fix."""
        self.audio_recorder.start_fix_recording()

    def process_fix(self, original_transcription):
        """Process the fix recording to correct the original transcription."""
        self.audio_recorder.stop_fix_recording()
        self.audio_recorder.save_fix_audio()

        fix_transcription = self.transcriber.transcribe_audio(self.audio_recorder.fix_audio_file)
        if fix_transcription:
            print(f"Fix Transcription: {fix_transcription}")

            # Use LLM to correct the original transcription based on fix_transcription
            self.corrected_transcription = self.ner_manager.correct_transcription(original_transcription, fix_transcription)
            print(f"Corrected Transcription: {self.corrected_transcription}")

            # Playback the corrected transcription
            self.corrected_proper_nouns = self.ner_manager.extract_proper_nouns(self.corrected_transcription)
            self.playback.playback_transcription(self.corrected_transcription)
            self.playback.playback_transcription('Proper nouns are: ' + ', '.join(self.corrected_proper_nouns))
            for noun in self.corrected_proper_nouns:
                spelled_out = spell_out(noun)
                self.playback.playback_transcription(f"{noun} is {spelled_out}")

            self.playback.cleanup()
        else:
            print("Fix transcription failed.")
            self.corrected_transcription = None

        return self.corrected_transcription
