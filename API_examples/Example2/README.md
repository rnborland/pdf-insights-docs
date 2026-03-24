# Transcript Assistant (API Example)

This example shows how to turn an audio recording into a queryable AI assistant using:

- an **OpenAI API key** for transcription
- a **PDF-Insights.ai API key** for PDF upload and querying

The workflow is intentionally simple:

1. Upload an audio file (`.wav`, `.mp3`, `.m4a`, `.ogg`, `.webm`, `.mp4`)
2. Transcribe it with OpenAI Whisper
3. Structure the transcript into readable paragraphs
4. Save it as a PDF
5. Upload the PDF to PDF-Insights.ai
6. Ask questions using the transcript assistant

This is a **starter / demo application**, not a production deployment.

---

## What this example demonstrates

- turn recordings into searchable knowledge
- summarize long interviews or meetings
- extract decisions, action items, deadlines, and objections
- ask custom questions about a transcript
- customize the assistant behavior using a system prompt

Typical use cases:

- interviews
- meetings
- journalism
- legal or deposition prep
- technical reviews
- research notes

---

## Quick Start

### 1) Get your API keys

You will need:

- **OpenAI API key** for transcription
- **PDF-Insights.ai API key** for PDF upload and querying

Get your PDF-Insights.ai API key from:

`https://users.pdf-insights.ai`

---

### 2) Install requirements

From inside this folder:

```bash
pip install -r requirements.txt
```

---

### 3) Run the app

Default port 8501:

```bash
streamlit run streamlit_transcript_assistant.py
```

Custom port example (8502):

```bash
streamlit run streamlit_transcript_assistant.py --server.port 8502 --server.address 0.0.0.0
```

Open in your browser:

```text
http://localhost:8501
```

If running on a remote server, use that server's IP or hostname and chosen port.

---

## App Workflow

### 1) Upload audio file

Upload one audio file such as:

- WAV
- MP3
- M4A
- OGG
- WEBM
- MP4

Tip: you can record on your phone or in Zoom/Teams, then upload the file here.

---

### 2) Transcribe audio

Enter your OpenAI API key and click **Transcribe Audio**.

The app uses Whisper to convert the recording into text.

---

### 3) Create transcript PDF

After transcription, click **Create Transcript PDF**.

The app will:

- clean the transcript
- structure it into paragraphs
- generate a readable PDF
- prepare it for upload to PDF-Insights.ai

---

### 4) Upload transcript PDF to PDF-Insights.ai

Enter your PDF-Insights.ai API key and click **Upload Transcript PDF**.

This sends the generated transcript PDF to the API and returns a `pdf_id`.

---

### 5) Ask questions

Use standard prompts or your own questions, such as:

- Summarize the key points.
- What decisions were made?
- What action items were mentioned?
- What deadlines were discussed?
- What concerns or objections were raised?
- Pull out the most important technical points.
- What did the speaker say about pricing?

---

## Customizing the assistant

This example includes a **System Prompt** box in the sidebar.

You can use it to make the assistant behave like:

- a transcript analyst
- a meeting assistant
- a legal review assistant
- a journalist research assistant
- a technical interview summarizer

The same app can support many transcript-driven workflows by changing the system prompt.

---

## Notes

- This example uses your **OpenAI API key directly** for transcription.
- It uses your **PDF-Insights.ai API key** for PDF upload and transcript querying.
- This keeps the example simple and avoids the need for JWT/session handling.
- It is intended as an easy-to-run example and starting point.

---

## Requirements

```text
streamlit
requests
openai
fpdf2
```

---

## Troubleshooting

### Transcription fails

- verify your OpenAI API key
- confirm the audio file is valid
- try a longer recording if the file is too short

### PDF upload fails

- verify your PDF-Insights.ai API key
- confirm the API is reachable

### Answers are weak

- use a cleaner transcript
- improve the system prompt
- ask more specific questions

---

## Why this matters

This example shows how to turn recordings into **queryable, reusable knowledge**.

Instead of rereading long recordings or transcripts, you can upload them and ask direct questions.

That makes it useful for:

- time savings
- knowledge extraction
- internal workflow simplification
- faster review of long-form content
