# PDF-Insights Developer API

Turn any PDF into a programmable AI assistant.

Upload a document, ask questions, control behavior with system prompts, and get structured answers.

---

## Quick Start

### Python Example

```python
import requests

API_KEY = "pdi_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
BASE_URL = "https://users.pdf-insights.ai"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

# Upload PDF
with open("example.pdf", "rb") as f:
    upload_resp = requests.post(
        f"{BASE_URL}/pdf/upload",
        headers=headers,
        files={"file": ("example.pdf", f, "application/pdf")}
    )

upload_resp.raise_for_status()
pdf_id = upload_resp.json()["pdf_id"]

# Ask a question
chat_resp = requests.post(
    f"{BASE_URL}/chat",
    headers=headers,
    json={
        "pdf_id": pdf_id,
        "question": "Summarize this document",
        "system_prompt": "You are a helpful assistant"
    }
)

chat_resp.raise_for_status()
print(chat_resp.json()["answer"])
```

---

## Get an API Key

Go to:

https://users.pdf-insights.ai/ui/

Then click:

Build with API

Notes:

- API keys begin with `pdi_live_`
- The key is shown once only
- Store it securely

---

## Authentication

Use your API key as a Bearer token:

```
Authorization: Bearer pdi_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## Workflow

1. Create API key  
2. Upload PDF  
3. Save `pdf_id`  
4. Ask questions via `/chat`  
5. Optionally use `system_prompt`  

---

## Endpoints

### POST /pdf/upload

Upload a PDF:

```python
with open("example.pdf", "rb") as f:
    requests.post(
        f"{BASE_URL}/pdf/upload",
        headers=headers,
        files={"file": ("example.pdf", f, "application/pdf")}
    )
```

Response:

```json
{
  "pdf_id": "your-pdf-id"
}
```

---

### POST /chat

Request:

```json
{
  "pdf_id": "your-pdf-id",
  "question": "Summarize this document",
  "system_prompt": "You are a helpful assistant"
}
```

Response:

```json
{
  "answer": "...",
  "status": "ok",
  "model_used": "gpt-4o-mini",
  "system_prompt_used": "...",
  "cost": {
    "charged_usd": 0.0021,
    "wallet_balance_usd": 4.9979
  }
}
```

---

## system_prompt

Use `system_prompt` to control behavior:

- "You are a refrigeration engineer diagnosing failures."
- "You are a compliance auditor."
- "You are a pirate refrigeration engineer."

The PDF becomes a programmable assistant.

---

## cURL Example

Upload:

```bash
curl -X POST "https://users.pdf-insights.ai/pdf/upload" \
  -H "Authorization: Bearer pdi_live_xxx" \
  -F "file=@example.pdf;type=application/pdf"
```

Chat:

```bash
curl -X POST "https://users.pdf-insights.ai/chat" \
  -H "Authorization: Bearer pdi_live_xxx" \
  -H "Content-Type: application/json" \
  -d '{
    "pdf_id": "your-pdf-id",
    "question": "Summarize this document",
    "system_prompt": "You are a helpful assistant"
  }'
```

---

## Status

- API keys working  
- Upload working  
- Chat working  

---

## Key Idea

Turn any PDF into a programmable AI assistant.
