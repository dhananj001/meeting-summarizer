from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from dotenv import load_dotenv
import requests
import re

load_dotenv()

app = Flask(__name__)
CORS(app)

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
    "Content-Type": "application/json"
}

def split_into_bullets(text, max_points=5):
    # Split text into sentences and return up to max_points bullets
    sentences = re.split(r'(?<=[.!?]) +', text.strip())
    bullets = [f"- {s.strip()}" for s in sentences if s.strip()]
    return "\n".join(bullets[:max_points])

def extract_action_items(text):
    # Extract lines that look like action items in a flexible way
    action_items = []
    lines = text.split('\n')
    for line in lines:
        line_lower = line.lower()
        if line.strip().startswith('-') or any(k in line_lower for k in ['task', 'deadline', 'poc', 'action item']):
            cleaned = line.strip('- ').strip()
            # Optional: further parse for task/poc/deadline if structured
            action_items.append(cleaned)
    return action_items

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

        # Truncate to 1000 words max to save tokens
        words = transcript.split()
        if len(words) > 1000:
            transcript = " ".join(words[:1000])

        # Call Hugging Face summarization API
        response = requests.post(HUGGINGFACE_API_URL, headers=headers, json={"inputs": transcript})
        if response.status_code != 200:
            print("HuggingFace API error:", response.text)
            return jsonify({"error": "Failed to get summary from API."}), 500

        summary_text = response.json()[0]['summary_text']

        # Format summary as bullet points for clarity
        formatted_summary = split_into_bullets(summary_text)

        # Extract action items from transcript (fallback if none structured)
        action_items = extract_action_items(transcript)

        return jsonify({
            "summary": formatted_summary,
            "action_items": action_items
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Server error occurred."}), 500

if __name__ == "__main__":
    app.run(debug=True)
