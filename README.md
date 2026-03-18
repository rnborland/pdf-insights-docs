# PDF-Insights Developer API

Turn any PDF into a programmable AI assistant.

Upload a document, send chat-style prompts, control behavior with system prompts, and get structured answers.

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
    "system_prompt": "You are a helpful assistant"
}

chat_resp = requests.post(
    f"{BASE_URL}/chat",
    headers=headers,
    json=payload
)

chat_resp.raise_for_status()
data = chat_resp.json()

# -------------------------------
# 3. Output
# -------------------------------
print("\nANSWER:\n")
print(data["answer"])

print("\nCOST:\n")
print(data.get("cost"))
```

---

## Get an API Key

Go to:

https://users.pdf-insights.ai/ui/

Create an account (username, email, and password), then click:

**Developer API (Get API Key)**

### Notes

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
4. Send a chat request to `/chat`  
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
  "session_id": "your-session-id",
  "pdf_id": "your-pdf-id",
  "message": "Summarize this document",
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

### Notes on `/chat`

- Use `message` for the user prompt  
- Include a `session_id` with each request  
- A new `session_id` can be generated for a new conversation  

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
    "session_id": "123e4567-e89b-12d3-a456-426614174000",
    "pdf_id": "your-pdf-id",
    "message": "Summarize this document",
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
