# 📘 Transcript Assistant (Example 2)

Turn an audio recording into a **queryable AI assistant**.

This example demonstrates how to:
- Transcribe audio using OpenAI Whisper
- Convert the transcript into a PDF
- Upload it to PDF-Insights.ai
- Ask questions about the content

---

## 🚀 Quick Start (Clone & Run)

```bash
git clone https://github.com/rnborland/pdf-insights-docs.git
cd pdf-insights-docs/API_examples/Example2
📦 Install Requirements
pip install -r requirements.txt
▶️ Run the App
streamlit run streamlit_transcript_assistant.py

The app will open in your browser (usually at http://localhost:8501
)

🔑 API Keys Required

You will need:

1. OpenAI API Key

Used for transcription (Whisper)

2. PDF-Insights API Key

Used for:

Uploading the transcript PDF
Querying the document

Enter both keys in the sidebar when the app starts.

🧭 How It Works
Upload an audio file (WAV, MP3, M4A, etc.)
Transcribe the audio into text
Convert the transcript into a structured PDF
Upload the PDF to PDF-Insights.ai
Ask questions about the content
💡 Example Questions
Summarize the key points
What decisions were made?
What action items were mentioned?
What concerns or objections were raised?
What deadlines were discussed?
What technical topics were covered?
⚙️ Custom Instructions (Optional)

You can customize how the assistant responds using a system prompt.

Example:

You are a transcript analysis assistant.

- Answer clearly and concisely
- Base answers only on the document
- Highlight key decisions, risks, and action items
- Do not invent information
🧱 What This Example Shows

This is a simple demonstration of a broader pattern:

Audio → Transcript → PDF → AI Assistant

It shows how unstructured content can be turned into something you can query like ChatGPT.

⚠️ Notes
This is a demo / reference implementation, not a production app
It uses direct API keys (no authentication layer)
PDF formatting is intentionally simple
Transcription cost is billed through your OpenAI account
🔄 Possible Extensions
Add live microphone recording
Add speaker detection (multi-speaker transcripts)
Add timestamps in transcript
Automatically detect action items
Integrate with meeting tools (Zoom, Teams, etc.)
📬 Want a Production Version?

This example is designed to be simple and easy to try.

If you want:

a hosted version
multi-user support
integrated billing
custom workflows

You can build on top of PDF-Insights.ai or reach out for a custom deployment.
