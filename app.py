from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

app = Flask(__name__)

# Gemini API
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=api_key)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data.get("message", "").strip()

        if not message:
            return jsonify({"reply": "Please enter a question."})

        prompt = f"""
You are InterviewPrep AI, a professional interview preparation assistant.

Help students prepare for:
- HR interviews
- Technical interviews
- Python
- C
- HTML/CSS/JavaScript
- AI and Data Science
- Software Testing
- Freshers interview questions

Give simple, clear and practical answers.
For technical questions, include examples when useful.
For interview questions, provide a sample answer.

User question:
{message}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return jsonify({"reply": response.text})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({
            "reply": "Sorry, something went wrong. Please try again."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)