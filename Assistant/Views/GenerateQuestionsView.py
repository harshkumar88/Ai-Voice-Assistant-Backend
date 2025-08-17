import os
import json
import requests
from dotenv import load_dotenv
from AiVoice.BaseClasses.CrofarmView import CrofarmView

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.5-pro"
GEMINI_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
)


class GenerateQuestionsView(CrofarmView):
    def post(self, request, version_id):
        try:
            prompt = request.data.get("prompt")
            if not prompt:
                return self.getFailureWithData({"error": "Prompt is required"}, 400)

            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [
                            {
                                "text": (
                                    f"Generate exactly 5 interview-style questions based on: {prompt}.\n"
                                    "Return ONLY valid JSON (no markdown) strictly in this format:\n"
                                    "{\n"
                                    "  \"questions\": [\n"
                                    "    {\n"
                                    "      \"heading\": \"string\",\n"
                                    "      \"question\": \"string\",\n"
                                    "      \"assesses\": [\"string\", \"string\"]\n"
                                    "    }\n"
                                    "  ]\n"
                                    "}\n"
                                    "Do not include any explanation or extra text."
                                )
                            }
                        ]
                    }
                ]
            }

            response = requests.post(
                GEMINI_URL,
                json=payload,
                headers={"Content-Type": "application/json"}
            )

            data = response.json()

            if "candidates" not in data or not data["candidates"]:
                return self.getFailureWithData({"error": data}, 500)

            # ✅ Handle both content structure types
            candidate = data["candidates"][0]
            if isinstance(candidate.get("content"), dict):
                parts = candidate["content"].get("parts", [])
            elif isinstance(candidate.get("content"), list):
                parts = candidate["content"].get("parts", [])
            else:
                parts = []

            if not parts or "text" not in parts[0]:
                return self.getFailureWithData({"error": "No text found in AI response", "raw": data}, 500)

            raw_text = parts[0]["text"].strip()

            # ✅ Try strict JSON parsing
            try:
                parsed_data = json.loads(raw_text)
            except json.JSONDecodeError:
                # If AI added extra text, extract JSON block
                import re
                json_match = re.search(r"\{[\s\S]*\}", raw_text)
                if json_match:
                    parsed_data = json.loads(json_match.group(0))
                else:
                    return self.getFailureWithData({"error": "Invalid JSON returned", "raw": raw_text}, 500)

            # ✅ Add success flag
            parsed_data["success"] = True
            return self.getResWithData(parsed_data)

        except Exception as e:
            return self.getFailureWithData({"error": str(e)}, 500)
