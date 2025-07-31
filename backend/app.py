from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize model
model = genai.GenerativeModel("models/gemini-1.5-flash")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        data = request.get_json()
        transcript = data.get("transcript", "").strip()

        if not transcript:
            return jsonify({"error": "Transcript is required."}), 400

        prompt = (
            "Summarize the following meeting transcript in a few sentences. "
            "Then list clear action items, including responsible persons and deadlines if mentioned.\n\n"
            f"{transcript}"
        )

        response = model.generate_content(prompt)

        content = response.text.strip()

        # Try to split into summary and action items
        parts = content.split("Action Items:")
        summary = parts[0].replace("Summary:", "").strip()
        action_items = [item.strip("-• ").strip() for item in parts[1].split("\n") if item.strip()] if len(parts) > 1 else []

        return jsonify({
            "summary": summary,
            "action_items": action_items
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Something went wrong on the server."}), 500

if __name__ == "__main__":
    app.run(debug=True)
