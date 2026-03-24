import os
import re
import uuid
import tempfile
import textwrap
from pathlib import Path

import requests
import streamlit as st
from fpdf import FPDF
from openai import OpenAI

BASE_URL = "https://users.pdf-insights.ai"

st.set_page_config(
    page_title="Transcript Assistant",
    page_icon="🎙️",
    layout="wide",
)

DEFAULT_SYSTEM_PROMPT = """You are a helpful transcript analysis assistant.

Your job is to answer questions based ONLY on the uploaded transcript PDF.

Goals:
1. Summarize the main points clearly.
2. Identify decisions, action items, objections, deadlines, and key themes when asked.
3. Stay grounded in the transcript.
4. Do not invent details that are not supported by the document.
5. If the transcript does not clearly contain the answer, say so.

Preferred response structure when appropriate:
- Direct answer
- Supporting details from the transcript
- Action items or follow-up points
"""


if "pdf_id" not in st.session_state:
    st.session_state.pdf_id = None

if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "question_box" not in st.session_state:
    st.session_state.question_box = ""

if "raw_transcript" not in st.session_state:
    st.session_state.raw_transcript = ""

if "structured_transcript" not in st.session_state:
    st.session_state.structured_transcript = ""

if "generated_pdf_path" not in st.session_state:
    st.session_state.generated_pdf_path = None

if "generated_pdf_name" not in st.session_state:
    st.session_state.generated_pdf_name = None

if "audio_filename" not in st.session_state:
    st.session_state.audio_filename = None



def get_openai_client(api_key: str) -> OpenAI:
    if not api_key.strip():
        raise ValueError("Enter your OpenAI API key first.")
    return OpenAI(api_key=api_key.strip())



def transcribe_to_text(api_key: str, audio_bytes: bytes, filename_hint: str = "speech.wav") -> str:
    client = get_openai_client(api_key)

    if not audio_bytes or len(audio_bytes) < 5000:
        raise ValueError("Recording too short. Please upload a longer file and try again.")

    _, ext = os.path.splitext(filename_hint.lower())
    if ext not in [".webm", ".ogg", ".wav", ".mp3", ".m4a", ".mp4"]:
        ext = ".wav"

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmpf:
        tmpf.write(audio_bytes)
        tmp_path = tmpf.name

    try:
        with open(tmp_path, "rb") as f:
            result = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                response_format="text",
            )
        return result
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass



def structure_transcript_text(raw_text: str) -> str:
    text = (raw_text or "").strip()
    if not text:
        return ""

    text = re.sub(r"\s+", " ", text).strip()
    sentences = re.split(r"(?<=[.!?])\s+", text)

    paragraphs = []
    current = []

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        current.append(sentence)
        if len(current) >= 3:
            paragraphs.append(" ".join(current))
            current = []

    if current:
        paragraphs.append(" ".join(current))

    return "\n\n".join(paragraphs)



def _safe_pdf_text(text: str) -> str:
    """
    Normalize text so the basic PDF font can handle it reliably.
    """
    if not text:
        return ""

    # Normalize common unicode punctuation to plain ASCII
    replacements = {
        "\u2018": "'",   # left single quote
        "\u2019": "'",   # right single quote
        "\u201c": '"',   # left double quote
        "\u201d": '"',   # right double quote
        "\u2013": "-",   # en dash
        "\u2014": "-",   # em dash
        "\u2026": "...", # ellipsis
        "\xa0": " ",     # non-breaking space
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Collapse weird whitespace but preserve paragraph breaks
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Latin-1 safe fallback for built-in fonts
    text = text.encode("latin-1", "replace").decode("latin-1")

    return text.strip()


def create_transcript_pdf(
    transcript_text: str,
    title: str = "Transcript",
    source_note: str = ""
) -> str:
    """
    Create a simple readable PDF from transcript text.
    Returns the path to the generated PDF file.
    """
    transcript_text = _safe_pdf_text(transcript_text)
    title = _safe_pdf_text(title)
    source_note = _safe_pdf_text(source_note)

    if not transcript_text.strip():
        raise ValueError("Transcript text is empty.")

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    left_margin = 15
    right_margin = 15
    usable_width = 210 - left_margin - right_margin  # A4 width assumptions
    pdf.set_left_margin(left_margin)
    pdf.set_right_margin(right_margin)

    # Title
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_x(left_margin)
    pdf.multi_cell(usable_width, 10, title)
    pdf.ln(2)

    # Optional source note
    if source_note.strip():
        pdf.set_font("Helvetica", "", 10)
        pdf.set_x(left_margin)
        pdf.multi_cell(usable_width, 6, source_note)
        pdf.ln(3)

    # Body
    pdf.set_font("Helvetica", "", 11)

    paragraphs = [p.strip() for p in transcript_text.split("\n\n") if p.strip()]
    if not paragraphs:
        paragraphs = [transcript_text]

    for para in paragraphs:
        pdf.set_x(left_margin)
        pdf.multi_cell(usable_width, 6, para)
        pdf.ln(2)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpf:
        pdf.output(tmpf.name)
        return tmpf.name
def upload_pdf(api_key: str, pdf_path: str, filename: str) -> tuple[bool, str]:
    headers = {"Authorization": f"Bearer {api_key}"}

    with open(pdf_path, "rb") as f:
        files = {"file": (filename, f, "application/pdf")}
        resp = requests.post(
            f"{BASE_URL}/pdf/upload",
            headers=headers,
            files=files,
            timeout=120,
        )

    if resp.status_code != 200:
        return False, f"Upload failed ({resp.status_code}): {resp.text}"

    data = resp.json()
    st.session_state.pdf_id = data["pdf_id"]
    st.session_state.uploaded_filename = filename
    st.session_state.chat_history = []
    st.session_state.session_id = str(uuid.uuid4())
    return True, f"Uploaded successfully: {filename}"



def ask_pdf_assistant(api_key: str, model: str, system_prompt: str, question: str) -> tuple[bool, str]:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "session_id": st.session_state.session_id,
        "pdf_id": st.session_state.pdf_id,
        "message": question.strip(),
        "model": model,
        "system_prompt": system_prompt,
    }

    resp = requests.post(
        f"{BASE_URL}/chat",
        headers=headers,
        json=payload,
        timeout=180,
    )

    if resp.status_code != 200:
        return False, f"Chat failed ({resp.status_code}): {resp.text}"

    data = resp.json()
    answer = data.get("answer", "(No answer returned)")
    return True, answer



def set_example_question(text: str):
    st.session_state.question_box = text


st.title("🎙️ Transcript Assistant")
st.write(
    "Upload an audio file, transcribe it, turn it into a PDF, and ask questions using the PDF-Insights.ai API."
)

with st.sidebar:
    st.header("API Settings")

    openai_api_key = st.text_input(
        "OpenAI API Key (for transcription)",
        type="password",
        placeholder="sk-...",
    )

    pdf_insights_api_key = st.text_input(
        "PDF-Insights API Key (for upload + query)",
        type="password",
        placeholder="pdi_live_...",
    )

    model = st.selectbox(
        "Query Model",
        ["gpt-4o-mini", "gpt-4o"],
        index=0,
    )

    st.markdown("---")
    st.header("Assistant Behavior")

    system_prompt = st.text_area(
        "System Prompt",
        value=DEFAULT_SYSTEM_PROMPT,
        height=260,
    )

    st.caption(
        "Customize this prompt to make the assistant behave like a transcript analyst, meeting assistant, legal reviewer, or research assistant."
    )

st.subheader("1) Upload audio file")

audio_file = st.file_uploader(
    "Choose an audio file",
    type=["wav", "mp3", "m4a", "ogg", "webm", "mp4"],
    help="Upload a recording from your phone, Zoom, Teams, interview, meeting, or other source.",
)

transcript_title = st.text_input("Transcript title", value="Transcript")
source_note = st.text_input("Optional source note", value="")

col_t1, col_t2 = st.columns([1, 4])
with col_t1:
    transcribe_clicked = st.button("Transcribe Audio", use_container_width=True)
with col_t2:
    if audio_file is not None:
        st.info(f"Selected audio file: {audio_file.name}")

if transcribe_clicked:
    if not openai_api_key:
        st.error("Enter your OpenAI API key first.")
    elif audio_file is None:
        st.error("Choose an audio file first.")
    else:
        try:
            with st.spinner("Transcribing audio..."):
                audio_bytes = audio_file.getvalue()
                transcript = transcribe_to_text(
                    api_key=openai_api_key,
                    audio_bytes=audio_bytes,
                    filename_hint=audio_file.name,
                )

            st.session_state.raw_transcript = (transcript or "").strip()
            st.session_state.structured_transcript = structure_transcript_text(st.session_state.raw_transcript)
            st.session_state.audio_filename = audio_file.name
            st.success("Transcription complete.")
        except Exception as e:
            st.error(f"Transcription failed: {e}")

st.subheader("2) Review transcript")

transcript_preview = st.text_area(
    "Structured transcript",
    value=st.session_state.structured_transcript,
    height=250,
    help="You can edit the transcript here before creating the PDF.",
)

col_p1, col_p2 = st.columns([1, 4])
with col_p1:
    create_pdf_clicked = st.button("Create Transcript PDF", use_container_width=True)
with col_p2:
    if st.session_state.generated_pdf_name:
        st.success(f"Generated PDF: {st.session_state.generated_pdf_name}")

if create_pdf_clicked:
    if not transcript_preview.strip():
        st.error("Transcribe audio first, or enter transcript text.")
    else:
        try:
            with st.spinner("Creating PDF..."):
                pdf_path = create_transcript_pdf(
                    transcript_text=transcript_preview,
                    title=transcript_title.strip() or "Transcript",
                    source_note=source_note.strip(),
                )

            st.session_state.structured_transcript = transcript_preview
            st.session_state.generated_pdf_path = pdf_path
            safe_title = re.sub(r"[^A-Za-z0-9_-]+", "_", transcript_title.strip() or "transcript")
            st.session_state.generated_pdf_name = f"{safe_title}.pdf"
            st.success("Transcript PDF created.")
        except Exception as e:
            st.error(f"PDF creation failed: {e}")

if st.session_state.generated_pdf_path and Path(st.session_state.generated_pdf_path).exists():
    with open(st.session_state.generated_pdf_path, "rb") as f:
        st.download_button(
            label="Download Transcript PDF",
            data=f.read(),
            file_name=st.session_state.generated_pdf_name or "transcript.pdf",
            mime="application/pdf",
        )

st.subheader("3) Upload transcript PDF to PDF-Insights.ai")

col_u1, col_u2 = st.columns([1, 4])
with col_u1:
    upload_pdf_clicked = st.button("Upload Transcript PDF", use_container_width=True)
with col_u2:
    if st.session_state.pdf_id:
        st.success(f"Current PDF: {st.session_state.uploaded_filename}")

if upload_pdf_clicked:
    if not pdf_insights_api_key:
        st.error("Enter your PDF-Insights API key first.")
    elif not st.session_state.generated_pdf_path or not Path(st.session_state.generated_pdf_path).exists():
        st.error("Create the transcript PDF first.")
    else:
        try:
            with st.spinner("Uploading transcript PDF..."):
                ok, message = upload_pdf(
                    api_key=pdf_insights_api_key,
                    pdf_path=st.session_state.generated_pdf_path,
                    filename=st.session_state.generated_pdf_name or "transcript.pdf",
                )
            if ok:
                st.success(message)
            else:
                st.error(message)
        except Exception as e:
            st.error(f"Upload error: {e}")

st.subheader("4) Example questions")

example_prompts = [
    "Summarize the key points.",
    "What decisions were made?",
    "What action items were mentioned?",
    "What deadlines were discussed?",
    "What concerns or objections were raised?",
    "What did the speaker say about pricing?",
    "Pull out the most important technical points.",
    "What follow-up steps are implied by this transcript?",
]

for i in range(0, len(example_prompts), 2):
    cols = st.columns(2)
    for j in range(2):
        idx = i + j
        if idx < len(example_prompts):
            with cols[j]:
                st.button(
                    example_prompts[idx],
                    key=f"example_{idx}",
                    use_container_width=True,
                    on_click=set_example_question,
                    args=(example_prompts[idx],),
                )

st.subheader("5) Ask the assistant")

if st.session_state.get("_clear_question"):
    st.session_state["question_box"] = ""
    st.session_state["_clear_question"] = False

question = st.text_area(
    "Your question",
    key="question_box",
    height=120,
    placeholder="Example: Summarize the main points and list any action items or deadlines.",
)

col_a1, col_a2 = st.columns([1, 5])
with col_a1:
    ask_clicked = st.button("Ask", use_container_width=True)

if ask_clicked:
    if not pdf_insights_api_key:
        st.error("Enter your PDF-Insights API key first.")
    elif not st.session_state.pdf_id:
        st.error("Upload the transcript PDF first.")
    elif not question.strip():
        st.error("Enter a question.")
    else:
        try:
            with st.spinner("Thinking..."):
                ok, result = ask_pdf_assistant(
                    api_key=pdf_insights_api_key,
                    model=model,
                    system_prompt=system_prompt,
                    question=question,
                )

            if ok:
                st.session_state.chat_history.append(
                    {
                        "question": question.strip(),
                        "answer": result,
                    }
                )
                st.session_state["_clear_question"] = True
                st.rerun()
            else:
                st.error(result)
        except Exception as e:
            st.error(f"Chat error: {e}")

if st.session_state.chat_history:
    st.subheader("Conversation")
    for item in reversed(st.session_state.chat_history):
        with st.container():
            st.markdown(f"**Question:** {item['question']}")
            st.markdown("**Answer:**")
            st.write(item["answer"])
            st.markdown("---")

with st.expander("How to customize this example"):
    st.markdown(
        """
**This app is intentionally simple.**

You can adapt it for many transcript-driven workflows by changing the **System Prompt**.

Examples:
- **Meeting Assistant** — summarize decisions, deadlines, and action items
- **Journalist Research Assistant** — pull themes, quotes, and contradictions
- **Legal Review Assistant** — identify statements, issues, and timeline references
- **Technical Interview Assistant** — extract important technical details and follow-up questions

This example is designed as a quick-start reference implementation and front-end demo, not a production deployment.
""" 

    )
