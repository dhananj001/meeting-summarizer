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

        # ✅ Truncate transcript to 1000 words to reduce token cost
        words = transcript.split()
        if len(words) > 1000:
            transcript = " ".join(words[:1000])

        # ✅ More concise prompt (reduced input token usage)
        prompt = (
            "You are an AI meeting assistant. Summarize the following business meeting in 3–5 sentences. "
            "Then extract action items as markdown collapsible cards using <details>. "
            "Each card should contain:\n"
            "- Task\n- Point of Contact (POC)\n- Deadline\n\n"
            f"Meeting Transcript:\n{transcript}"
        )

        # Optional: Log token estimate before sending
        tokens = model.count_tokens(prompt).total_tokens
        print("Estimated token usage (input):", tokens)

        # 🔁 Call Gemini
        response = model.generate_content(prompt)
        content = response.text.strip()

        # ✅ Split into summary and action items
        parts = content.split("Action Items:")
        summary = parts[0].replace("Summary:", "").strip()
        action_items_raw = parts[1] if len(parts) > 1 else ""

        # ✅ Extract each <details> block separately (preserving markdown)
        action_items = []
        blocks = action_items_raw.split("<details>")
        for block in blocks:
            block = block.strip()
            if block:
                item = "<details>" + block if not block.startswith("<details>") else block
                action_items.append(item)

        return jsonify({
            "summary": summary,
            "action_items": action_items
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Something went wrong on the server."}), 500

if __name__ == "__main__":
    app.run(debug=True)
