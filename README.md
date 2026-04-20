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
|--------|------|--------|----------|-----|
| Trial wallet credit | $1 | — | — | — |
| API access | Yes | Yes | Yes | Yes |
| Storage limit | 50 MB | 100 MB | 250 MB | 1 GB |
| Max PDFs | 2 | 10 | 20 | 100 |
| Voice features | No | No | Yes | Yes |
| Custom `system_prompt` / personality | No | No | Yes | Yes |
| Agents | No | No | Yes | Yes |
| Allowed models | gpt-4o-mini | gpt-4o-mini | gpt-4o-mini, gpt-4o | gpt-4o-mini, gpt-4o |

---

## Important

If a custom `system_prompt` is provided on **Free or Budget plans**, it will be ignored and replaced with the default assistant behavior.

---

## Quick Start

### Step 1 — Create an Account

Go to:

https://users.pdf-insights.ai/ui/

- Register and log in  
- No credit card required  
- Includes $1 free usage credit  

---

### Step 2 — Create an API Key

After logging in:

1. Click **Advanced**
2. Scroll to the bottom
3. Open **Developer API**
4. Click **Create API Key**

Your key will look like:


pdi_live_xxxxxxxxxxxxxxxxxxxxxxxxx


---

### Step 3 — Upload a PDF and Get `pdf_id`

Use the Python script below to:

- upload your document
- automatically return the `pdf_id`
- test a chat request

---

## Python Example

```python
import requests
import uuid
import time

API_KEY = "pdi_live_your_key_here"
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

# Optional: wait briefly for processing
time.sleep(3)

# -------------------------------
# 2. Send chat request
# -------------------------------
chat_headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "session_id": str(uuid.uuid4()),
    "pdf_id": pdf_id,
    "message": "Summarize this document",
    "model": "gpt-4o-mini",
    "system_prompt": "You are a helpful assistant. Base your answer only on the uploaded document."
}

chat_resp = requests.post(
    f"{BASE_URL}/chat",
    headers=chat_headers,
    json=payload
)

chat_resp.raise_for_status()
chat_data = chat_resp.json()

print("\nChat response:")
print(chat_data.get("answer", chat_data))
Using Your Own PDF

Place your PDF in the same folder as the script and rename it:

example.pdf

Or modify this line:

with open("example.pdf", "rb") as f:

Example:

with open("my_catalog.pdf", "rb") as f:
What This Script Does
Uploads your PDF
Returns a pdf_id
Sends a chat request
Prints the response
Next Step

Once you have your:

API key
pdf_id

You can:

build applications
embed chatbots
create agents
integrate into workflows
