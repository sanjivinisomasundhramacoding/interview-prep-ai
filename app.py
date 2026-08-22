from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

app = Flask(__name__)

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
            return jsonify({"reply": "Please enter your question."})

        prompt = f"""
You are CareerGuide AI, a professional AI career guidance assistant.

Help students and freshers with:
- Career selection
- Career roadmaps
- Skills to learn
- Python careers
- Software testing
- Web development
- Artificial Intelligence
- Data Science
- Cybersecurity
- Resume improvement
- Interview preparation
- Job preparation

Give simple, practical and beginner-friendly answers.

If the user asks for a roadmap, provide clear step-by-step guidance.
If the user asks about skills, provide a useful skill list.
Do not guarantee jobs or salaries.

User question:
{message}
"""

        response = client.models.generate_content(
            model="gemini-3.6-flash",
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