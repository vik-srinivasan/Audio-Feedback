import google.generativeai as genai
import os

class NERManager:
    """Class for managing Named Entity Recognition and memory of proper nouns."""

    def __init__(self):
        self.memory = {}

    def extract_proper_nouns(self, transcription):
        prompt = (
            "You are a proper noun extractor. Extract all proper nouns from the following text and return them in a list:\n"
            f"{transcription}\n"
            "Please return only the proper nouns, with no additional words."
            "Here are 3 examples:"
            "If the text is 'John and Mary are students at Stanford', you would return: ['John', 'Mary', 'Stanford']."
            "If the text is 'Vikram and Sanjay are brothers from Brooklyn, New York', you would return: ['Vikram', 'Sanjay', 'Brooklyn', 'New York']."
            "If the text is 'There are no proper nouns in this sentence', you would return: []."
        )
        response = self.call_gpt_api(prompt)
        if response:
            # Remove brackets and split by commas
            proper_nouns = response.replace('[', '').replace(']', '').replace("'", "").split(",")
            proper_nouns = [noun.strip() for noun in proper_nouns if noun.strip()]
            self.update_memory(proper_nouns)
            return proper_nouns
        else:
            print("No response received from Gemini API.")
            return []

    def call_gpt_api(self, prompt):
        """Call the Gemini API with the given prompt to extract proper nouns."""
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            return response.text if response else ""
        except Exception as e:
            print(f"An error occurred while calling the Gemini API: {e}")
            return ""

    def update_memory(self, proper_nouns):
        for noun in proper_nouns:
            self.memory[noun] = self.memory.get(noun, 0) + 1

    def clear_memory(self):
        """Clear the memory of proper nouns."""
        self.memory = {}

    def correct_transcription(self, original_transcription, fix_transcription):
        """Use LLM to correct the original transcription based on fix transcription."""
        prompt = (
            "You are an assistant that corrects transcriptions based on user's corrections.\n"
            "Given the original transcription and the user's correction, output the corrected transcription.\n"
            "Make minimal changes needed to the original transcription to incorporate the corrections.\n"
            f"Original transcription: \"{original_transcription}\"\n"
            f"User's correction: \"{fix_transcription}\"\n"
            "Corrected transcription:"
        )
        response = self.call_gpt_api(prompt)
        if response:
            corrected_transcription = response.strip()
            return corrected_transcription
        else:
            print("No response received from LLM for correction.")
            return original_transcription
