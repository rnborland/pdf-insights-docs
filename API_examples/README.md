📄 API_examples/README.md
# PDF Catalog Assistant (API Example)

This example shows how to turn a product catalog, guide, or price list PDF into a working AI-powered assistant using the PDF-Insights.ai API.

The assistant can:
- answer product and technical questions
- recommend best-fit products
- suggest companion products (upsell bundles)
- generate quote-style responses

---

# 🚀 Quick Start (5–10 minutes)

## 1) Get an API Key

Go to:
https://users.pdf-insights.ai

- Create an account (if needed)
- Generate an API key
- It will look like:


pdi_live_xxxxxxxxxxxxxxxxxxxxxxxxx


---

## 2) Clone or Download This Repo

```bash
git clone https://github.com/rnborland/pdf-insights-docs.git
cd pdf-insights-docs/API_examples

Or download just this folder.

3) Install Requirements

Make sure Python is installed (3.9+ recommended)

Then install dependencies:

pip install -r requirements.txt
4) Run the Streamlit App

Default (port 8501):

streamlit run streamlit_catalog_assistant.py

Custom port (example: 8502):

streamlit run streamlit_catalog_assistant.py --server.port 8502 --server.address 0.0.0.0

Then open your browser:

http://localhost:8501

(or your EC2 IP if running remotely)

5) Upload Your Catalog PDF

Prepare a PDF that contains:

product catalog
price list (optional but recommended)
product specifications
accessories / companion items

👉 Best results come from combining catalog + pricing into one PDF

In the app:

Enter your API key
Upload the PDF
Click Upload PDF
6) Ask Questions

Try questions like:

Which product best fits this application?
Recommend a complete solution, not just a single item.
What companion products should be included?
Prepare a quote-style recommendation.
Compare two options from the catalog.
What accessories should be offered with this product?
🧠 What This Example Demonstrates

This app turns a static PDF into a:

Customer Service Agent
Sales Assistant
Sales Engineer
Technical Rep
Product Recommendation Engine

Instead of just answering questions, the assistant can guide users toward:

👉 complete solutions and product bundles

⚙️ How It Works
Upload PDF → /pdf/upload
Ask question → /chat
Send system_prompt to guide assistant behavior
Receive structured answer

All logic is handled by the API — the app is intentionally simple.

🔧 Customizing the Assistant

The behavior of the assistant is controlled by the system prompt in the sidebar.

You can easily adapt this for different industries.

Example: Generic Catalog Assistant

Default behavior:

recommends products
suggests related items
provides quote-style summaries
Example: Pump System (Upsell to Full Package)

Modify the prompt to encourage:

pump selection
isolation valves
check valves
strainers / filters
control systems

Goal:
👉 sell a complete pump package, not just the pump

Example: HVAC
recommend units
suggest thermostats, filters, fittings
build install-ready packages
Example: Electrical
panels, breakers, disconnects
compatible accessories
full system recommendations
Example: Lab Equipment
instruments
required accessories
consumables
calibration kits
💡 Key Concept

The app is generic.

👉 The PDF + system prompt define the business logic.

That means:

same code
different industries
different behavior
📦 Requirements
streamlit
requests

Install with:

pip install -r requirements.txt
🧪 Troubleshooting
Upload fails
check API key
confirm PDF is valid
check network access
Chat fails
confirm PDF uploaded successfully
check API key
check backend is reachable
No useful answers
improve your PDF (combine catalog + pricing)
refine the system prompt
🚀 Next Steps
Customize the system prompt for your business
Integrate into your web app or backend
Build a product recommendation or quoting workflow
Deploy as internal tool or customer-facing assistant
🌐 About PDF-Insights.ai

PDF-Insights.ai turns documents into programmable AI assistants via API.

Use cases:

product catalogs
technical manuals
internal knowledge bases
compliance documents
quoting systems
