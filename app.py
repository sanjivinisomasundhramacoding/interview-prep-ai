from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
import os
import re

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
        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "reply": "Please enter your question."
            }), 400

        message = data.get("message", "").strip()

        if not message:
            return jsonify({
                "reply": "Please enter your question."
            }), 400

        prompt = f"""
You are InterviewPrep AI, a professional AI interview preparation assistant.

Help students, freshers and job seekers with:

Interview preparation
Technical interview questions
HR interview questions
Python interview questions
C programming interview questions
HTML and CSS interview questions
JavaScript interview questions
Software testing interview questions
Artificial Intelligence interview questions
Machine Learning interview questions
Data Science interview questions
Cybersecurity interview questions
SQL interview questions
Web development interview questions
Data Structures and Algorithms basics
Aptitude preparation
Coding interview preparation
Mock interview practice
Self introduction
Resume-based interview questions
Behavioral interview questions
Common HR questions
Interview tips
Communication skills
Strengths and weaknesses
Why should we hire you
Why do you want this job
Questions to ask the interviewer

Give simple, practical and beginner-friendly answers.

For technical questions:
Explain the concept clearly.
Give a simple example when useful.
Keep the explanation easy for beginners.

For interview questions:
Provide a suitable sample answer.
Keep answers professional and natural.
Do not make answers unnecessarily complicated.

For coding questions:
Explain the logic first.
Then provide a simple code example when appropriate.

For mock interview requests:
Ask one interview question at a time and wait for the user's answer before continuing.

Do not guarantee job selection.
Do not guarantee a specific salary or placement.
Encourage users to prepare according to the requirements of the specific company and job role.

Response formatting rules:

Use plain text only.

Do not use Markdown.

Do not use **bold** formatting.

Do not use *italic* formatting.

Do not use # headings.

Do not use --- horizontal lines.

Do not use bullet points with *.

Do not use backticks.

Do not use decorative symbols.

Do not use unnecessary emojis.

Use numbered points when useful.

Keep answers simple, clean and readable.

User question:

{message}
"""

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        reply = response.text or ""

        # Remove Markdown headings
        reply = re.sub(
            r"^\s*#{1,6}\s*",
            "",
            reply,
            flags=re.MULTILINE
        )

        # Remove bold and underline formatting
        reply = reply.replace("**", "")
        reply = reply.replace("__", "")

        # Remove asterisks
        reply = reply.replace("*", "")

        # Remove backticks
        reply = reply.replace("```", "")
        reply = reply.replace("`", "")

        # Remove horizontal lines
        reply = re.sub(
            r"^\s*[-*_]{3,}\s*$",
            "",
            reply,
            flags=re.MULTILINE
        )

        # Remove Markdown bullet symbols
        reply = re.sub(
            r"^\s*[-+]\s+",
            "",
            reply,
            flags=re.MULTILINE
        )

        # Remove unnecessary emojis
        reply = re.sub(
            r"[\U0001F300-\U0001FAFF]",
            "",
            reply
        )

        # Remove excessive spaces before new lines
        reply = re.sub(
            r"[ \t]+\n",
            "\n",
            reply
        )

        # Remove excessive blank lines
        reply = re.sub(
            r"\n{3,}",
            "\n\n",
            reply
        )

        reply = reply.strip()

        if not reply:
            reply = (
                "Sorry, I could not generate a response. "
                "Please try again."
            )

        return jsonify({
            "reply": reply
        }), 200

    except Exception as e:
        print("ERROR:", repr(e))

        error_message = str(e)

        if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
            return jsonify({
                "reply": (
                    "Gemini API quota exceeded. "
                    "Please check your Gemini API quota."
                )
            }), 429

        if "404" in error_message or "NOT_FOUND" in error_message:
            return jsonify({
                "reply": (
                    "The Gemini model is currently unavailable. "
                    "Please check the configured Gemini model."
                )
            }), 404

        if "401" in error_message or "UNAUTHENTICATED" in error_message:
            return jsonify({
                "reply": (
                    "Gemini API authentication failed. "
                    "Please check the GEMINI_API_KEY."
                )
            }), 401

        if "403" in error_message or "PERMISSION_DENIED" in error_message:
            return jsonify({
                "reply": (
                    "Gemini API permission denied. "
                    "Please check your API key and API access."
                )
            }), 403

        return jsonify({
            "reply": "Sorry, something went wrong. Please try again."
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )