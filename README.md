# PDF-Insights Developer API

Turn any PDF into a programmable AI assistant — with built-in cost tracking.

Upload a document, send chat-style prompts, control behavior with system prompts, and get structured answers.

**No RAG pipeline required. No cost guesswork.**

---

## Why This Exists

Most tools handle retrieval.

This API handles the full pipeline:

- Document querying (RAG)
- LLM reasoning (chat-style responses)
- Real-time token cost tracking
- Multi-user usage tracking (session-based)

Build AI features without rebuilding the backend every time.

---

## Try It Free (No Risk)

Every account includes a **$1 free wallet credit**.

- No credit card required  
- Full API access available  
- Test real queries immediately  

Build and validate your integration before spending anything.

---

## Plans and Feature Access

| Feature | Free | Budget | Standard | Pro |
|---|---|---|---|---|
| Trial wallet credit | $1 | — | — | — |
| API access | Yes | Yes | Yes | Yes |
| Storage limit | 50 MB | 100 MB | 250 MB | 1 GB |
| Max PDFs | 2 | 10 | 20 | 100 |
| Voice features | No | No | Yes | Yes |
| Custom `system_prompt` / personality | No | No | Yes | Yes |
| Agents | No | No | Yes | Yes |
| Allowed models | `gpt-4o-mini` | `gpt-4o-mini` | `gpt-4o-mini`, `gpt-4o` | `gpt-4o-mini`, `gpt-4o` |

### Important

If a custom `system_prompt` is provided on **Free or Budget plans**, it will be ignored and replaced with the default assistant behavior.

---

## Quick Start

### Python Example

```python
import requests
import uuid

API_KEY = "pdi_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
BASE_URL = "https://users.pdf-insights.ai"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

# -------------------------------
# 1. Upload PDF
# -------------------------------
with open("example.pdf", "rb") as f:
    upload_resp = requests.post(
        f"{BASE_URL}/pdf/upload",
        headers=headers,
        files={"file": ("example.pdf", f, "application/pdf")}
    )

upload_resp.raise_for_status()
upload_data = upload_resp.json()

pdf_id = upload_data["pdf_id"]
print("Uploaded PDF ID:", pdf_id)

# -------------------------------
# 2. Send chat request
# -------------------------------
payload = {
    "session_id": str(uuid.uuid4()),
    "pdf_id": pdf_id,
    "message": "Summarize this document",
}
