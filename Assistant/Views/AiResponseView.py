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


class AiResponseView(CrofarmView):

    def post(self, request, version_id):

        self.setJsonEncodedBody()
        user_input = self.body['message']
        print(user_input)
        ai_response = self.get_ai_response(user_input)
        print("🤖 AI says:", ai_response)
        return self.getResWithData({"data": ai_response})

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


