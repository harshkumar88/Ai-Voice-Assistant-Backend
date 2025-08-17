import os
import requests
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
import json
import re
import time

from AiVoice.BaseClasses.CrofarmView import CrofarmView

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini API endpoint
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

# Initialize recognizer and speaker
recognizer = sr.Recognizer()
speaker = pyttsx3.init()


class VoiceBotView(CrofarmView):

    def post(self, request, version_id):
        while True:
            print("\n--- Listening ---")
            user_input = self.speech_to_text()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit", "bye"]:
                print("👋 Ending chat")
                break

            print(user_input)

            ai_response = self.get_ai_response(user_input)
            print("🤖 AI says:", ai_response)

            self.text_to_speech(ai_response)

            # Delay after speaking to avoid capturing bot's speech as input
            time.sleep(1)

    def speech_to_text(self):
        with sr.Microphone() as source:
            # Recalibrate ambient noise after bot finishes speaking
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("🎤 Speak something...")

            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)
                print("📝 You said:", text)
                return text
            except sr.UnknownValueError:
                print("❌ Could not understand audio")
            except sr.RequestError as e:
                print("⚠️ STT API error:", e)
        return None

    def get_ai_response(self, text, expect_json=False):
        headers = {"Content-Type": "application/json"}
        data = {"contents": [{"parts": [{"text": "give response in just 1-2 lines which looks like human answers and use very baisc language"+text}]}]}
        response = requests.post(ENDPOINT, headers=headers, json=data)

        if response.status_code == 200:
            try:
                res_json = response.json()
                candidates = res_json.get("candidates", [])
                if not candidates:
                    return "Sorry, no candidates returned by AI."

                candidate = candidates[0]
                content = candidate.get("content", {})
                parts = content.get("parts", [])
                if not parts:
                    return "Sorry, no content parts returned by AI."

                texts_field = parts[0].get("text")

                # Depending on structure, extract AI reply
                if isinstance(texts_field, str):
                    final_text = texts_field
                elif isinstance(texts_field, list) and texts_field and isinstance(texts_field[0], dict):
                    final_text = texts_field.get("text", "")
                else:
                    return "Sorry, unexpected AI response format."

                final_text = final_text.strip()

                if expect_json:
                    try:
                        return json.loads(final_text)
                    except json.JSONDecodeError:
                        json_match = re.search(r"\{[\s\S]*\}", final_text)
                        if json_match:
                            try:
                                return json.loads(json_match.group(0))
                            except Exception as e:
                                print("⚠️ Could not parse JSON block:", e)
                        return {"error": "Invalid JSON returned", "raw": final_text}

                return final_text

            except Exception as e:
                print("⚠️ API response parsing error:", e)
                return "Sorry, I couldn't understand the response from AI."
        else:
            print("⚠️ API error:", response.status_code, response.text)
            return "Sorry, there was an error contacting the AI service."

    def text_to_speech(self, text):
        print("🔊 Speaking...")
        speaker.say(text)
        speaker.runAndWait()
