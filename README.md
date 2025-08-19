# 🤖 AI Meeting Summarizer

AI-powered web application that **summarizes business meeting transcripts** into clear, actionable insights using the **Gemini 1.5 Flash model** from Google AI Studio.

---

## ✨ Live Demo

> This is how starting page looks like.. (Subtle starfield animation)
![homepage](https://github.com/user-attachments/assets/888a223b-ea28-4a11-8431-6afa9f6902d5)


> Paste your meeting transcript → Click **Summarize** → Get a clean markdown-style summary with action items! 
![process](https://github.com/user-attachments/assets/107517d4-2676-4334-8d99-859cf698335f)

---

## Why This Project?

Built as a practical demonstration for roles like **AI Platform Engineer**, this project showcases:

* Prompt engineering for high-quality, structured outputs
* Integration of **LLM APIs** using Google AI Studio
* End-to-end **LLM-based workflow** with UX-friendly frontend
* Compliance-friendly output structuring (Markdown, POC, Deadline)

---

## 🔍 Features

* ✍️ **Dynamic Prompt Engineering** for business meeting transcripts
* 🤖 Powered by **Gemini 1.5 Flash** via **Google Generative AI**
* ⚡ Markdown-formatted, structured outputs
* 🧹 Summarization + Action Item Extraction
* 🌌 Subtle starfield animation (futuristic UX)
* 🚠 Modern UI with **TailwindCSS** + **Glassmorphism**

---

## 🧠 Tech Stack

| Layer           | Tech                          |
| --------------- | ----------------------------- |
| Frontend        | HTML, TailwindCSS, Vanilla JS |
| Backend         | Python, Flask, Flask-CORS     |
| AI Platform     | Google Gemini 1.5 Flash API   |
| Environment     | dotenv                        |
| Hosting (local) | Flask Dev Server              |

---

## Architecture Overview

```
[User Transcript]
     ⬇
[Frontend UI] — Tailwind + JS
     ⬇
[POST /summarize]
     ⬇
[Flask Backend] → Gemini API
     ⬇
[LLM Response Parsing (Summary + Actions)]
     ⬇
[Frontend Render]
```

---

## Prompt Logic

The app sends structured instructions to the LLM to:

1. Generate a **summary** (3–5 concise lines)
2. Extract **action items** with:

   * Task
   * Point of Contact
   * Deadline
3. Return Markdown-style output

**Sample Prompt:**

```
You are an expert AI meeting assistant. Given the following transcript...
```

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/ai-meeting-summarizer.git
cd ai-meeting-summarizer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup `.env`

```
GOOGLE_API_KEY=your_google_ai_studio_key
```

### 4. Run the Flask app

```bash
python app.py
```

### 5. Open in browser

```
http://localhost:5000/
```

---

## Sample Output

### Summary:

* Discussed upcoming Q3 product roadmap and resourcing.
* Identified issues with current sales pipeline reporting.
* Reviewed marketing performance from last quarter.

### Action Items:

* **Task**: Redesign sales pipeline dashboard
  **POC**: Rahul Shah
  **Deadline**: Aug 15

* **Task**: Prepare Q3 OKRs proposal
  **POC**: Neha Sharma
  **Deadline**: Aug 7

---

## 📌 Future Enhancements

* Export summary as PDF/Markdown
* Chrome extension integration for Google Meet
* Add authentication and user history
* Vector DB storage for semantic search

---

## Optional Alternative: Hugging Face API

You can experiment with the same prompt on Hugging Face's hosted LLMs like Mistral, Phi-3, or LLaMA models. This may be useful if:

* You’ve hit Google Gemini token limits (free tier)
* You want to benchmark open models

### Steps:

1. Create a free Hugging Face account
2. Go to [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) and generate an API key
3. Update your `.env` file:

```
HF_API_KEY=your_token_here
```

4. In `app.py`, uncomment the HuggingFace section and comment out Gemini-related code.

**Note**: Hugging Face models may not match Gemini’s summarization performance, but are a great fallback for prototyping.

---

## 📈 Skills Demonstrated (Relevant to AI Platform Engineer Role)

* 🔧 LLM API Integration (Gemini 1.5 + optional HuggingFace via Python)
* 🧠 Prompt Engineering & Output Structuring
* 🖥️ UI/UX for AI Tooling (glassmorphism + Tailwind)
* 📊 Instrumentation-ready design (modular response parsing)
* 🔐 Compliant with safe prompt structure (no PII leakage)

---

## 🧑‍💼 Author

**Dhananjay Borse**
🌐 [Portfolio](https://github.com/dhananj001) • 💼 [LinkedIn](https://www.linkedin.com/in/dhananjayborse001/) • ✉️ [Email](dhananjayborsebld@gmail.com)

---

## 📄 License

This project is licensed under the MIT License.

