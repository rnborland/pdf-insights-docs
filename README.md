# 🚀 PDF-Insights Developer API

Turn any PDF into a queryable AI assistant in minutes.

## ⚡ 60-Second Quick Start

```python
import requests

API_KEY = "pdi_live_xxxxx"
BASE_URL = "https://users.pdf-insights.ai"

headers = {"Authorization": f"Bearer {API_KEY}"}

# Upload PDF
with open("manual.pdf", "rb") as f:
    r = requests.post(
        f"{BASE_URL}/pdf/upload",
        headers=headers,
        files={"file": f}
    )

pdf_id = r.json()["pdf_id"]

# Ask a question
resp = requests.post(
    f"{BASE_URL}/chat",
    headers=headers,
    json={
        "pdf_id": pdf_id,
        "question": "What are the safety warnings?",
        "system_prompt": "You are a safety compliance expert."
    }
)

print(resp.json()["answer"])
