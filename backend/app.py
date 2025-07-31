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

        hf_json = response.json()
        summary_text = hf_json[0].get("summary_text", "").strip()

        # Convert summary to bullet points by splitting sentences
        sentences = re.split(r'(?<=[.!?])\s+', summary_text)
        sentences = [s.strip() for s in sentences if s.strip()]
        summary_points = "\n".join(f"- {s}" for s in sentences)

        # Extract action items from transcript using regex
        tasks = []
        pattern = re.compile(
            r"-\s*Task:\s*(?P<task>.*?);?\s*POC:\s*(?P<poc>.*?);?\s*Deadline:\s*(?P<deadline>.*)", re.IGNORECASE)

        for line in transcript.split('\n'):
            match = pattern.match(line.strip())
            if match:
                tasks.append({
                    "task": match.group("task").strip(),
                    "poc": match.group("poc").strip(),
                    "deadline": match.group("deadline").strip()
                })

        # Return the bullet-point summary and extracted tasks
        return jsonify({
            "summary": summary_points,
            "action_items": tasks
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Server error occurred."}), 500


if __name__ == "__main__":
    app.run(debug=True)
