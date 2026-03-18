Get an API Key

👉 https://users.pdf-insights.ai/ui/

Click:

Build with API

Authentication
Authorization: Bearer pdi_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Core Workflow

Create API key

Upload PDF

Store pdf_id

Query with /chat

Use system_prompt to specialize behavior

Endpoints
POST /pdf/upload
with open("example.pdf", "rb") as f:
    upload_resp = requests.post(
        f"{BASE_URL}/pdf/upload",
        headers=headers,
        files={"file": ("example.pdf", f, "application/pdf")}
    )

Response

{
  "pdf_id": "your-pdf-id"
}
POST /chat

Request

{
  "pdf_id": "your-pdf-id",
  "question": "Summarize this document.",
  "system_prompt": "You are a concise technical assistant."
}

Response

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
system_prompt = Your Superpower

Turn the same PDF into different assistants:

"You are a refrigeration engineer diagnosing failures."
"You are a compliance auditor."
"You are a pirate refrigeration engineer."
cURL Example
Upload
curl -X POST "https://users.pdf-insights.ai/pdf/upload" \
  -H "Authorization: Bearer pdi_live_xxx" \
  -F "file=@example.pdf;type=application/pdf"
Chat
curl -X POST "https://users.pdf-insights.ai/chat" \
  -H "Authorization: Bearer pdi_live_xxx" \
  -H "Content-Type: application/json" \
  -d '{
    "pdf_id": "your-pdf-id",
    "question": "Summarize this document",
    "system_prompt": "You are a concise assistant"
  }'
Minimal Example File
import os
import requests

API_KEY = "pdi_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
BASE_URL = "https://users.pdf-insights.ai"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}


def upload_pdf(file_path):
    filename = os.path.basename(file_path)

    with open(file_path, "rb") as f:
        resp = requests.post(
            f"{BASE_URL}/pdf/upload",
            headers=headers,
            files={"file": (filename, f, "application/pdf")}
        )

    resp.raise_for_status()
    return resp.json()["pdf_id"]


def ask_question(pdf_id, question, system_prompt=None):
    payload = {
        "pdf_id": pdf_id,
        "question": question
    }

    if system_prompt:
        payload["system_prompt"] = system_prompt

    resp = requests.post(
        f"{BASE_URL}/chat",
        headers=headers,
        json=payload
    )

    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    pdf_id = upload_pdf("example.pdf")

    response = ask_question(
        pdf_id,
        "Summarize the document.",
        system_prompt="You are a helpful assistant."
    )

    print(response["answer"])
