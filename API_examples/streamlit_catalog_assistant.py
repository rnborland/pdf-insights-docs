import uuid
import requests
import streamlit as st

BASE_URL = "https://users.pdf-insights.ai"

st.set_page_config(
    page_title="PDF Catalog Assistant",
    page_icon="📘",
    layout="wide"
)

# -----------------------------
# Default configurable prompt
# -----------------------------
DEFAULT_SYSTEM_PROMPT = """You are a professional sales assistant and technical product advisor.

Your job is to help the user find the best product or solution based ONLY on the uploaded PDF catalog, product guide, or price list.

Goals:
1. Recommend the best matching product for the user's stated need.
2. Suggest required companion products, accessories, or related items when appropriate.
3. Guide the user toward a complete solution, not just a single item.
4. Explain why the recommendation fits the application.
5. Provide a quote-style summary when requested.
6. If pricing is available in the PDF, include it. If not, clearly say pricing was not found.
7. Do not invent specifications, pricing, policies, discounts, or availability.
8. If the document supports multiple possible options, explain the tradeoffs clearly.
9. Stay grounded in the uploaded document at all times.

Preferred response structure when appropriate:
- Recommended product
- Why it fits
- Required companion products
- Optional add-ons
- Quote-style summary

If the answer is not clearly supported by the PDF, say so.
"""

# -----------------------------
# Session state
# -----------------------------
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

# -----------------------------
# Helper functions
# -----------------------------
def upload_pdf(api_key: str, uploaded_file) -> tuple[bool, str]:
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    files = {
        "file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")
    }

    resp = requests.post(
        f"{BASE_URL}/pdf/upload",
        headers=headers,
        files=files,
        timeout=120
    )

    if resp.status_code != 200:
        return False, f"Upload failed ({resp.status_code}): {resp.text}"

    data = resp.json()
    st.session_state.pdf_id = data["pdf_id"]
    st.session_state.uploaded_filename = uploaded_file.name
    st.session_state.chat_history = []
    st.session_state.session_id = str(uuid.uuid4())  # fresh conversation for new PDF

    return True, f"Uploaded successfully: {uploaded_file.name}"


def ask_pdf_assistant(api_key: str, model: str, system_prompt: str, question: str) -> tuple[bool, str]:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "session_id": st.session_state.session_id,
        "pdf_id": st.session_state.pdf_id,
        "message": question.strip(),
        "model": model,
        "system_prompt": system_prompt
    }

    resp = requests.post(
        f"{BASE_URL}/chat",
        headers=headers,
        json=payload,
        timeout=180
    )

    if resp.status_code != 200:
        return False, f"Chat failed ({resp.status_code}): {resp.text}"

    data = resp.json()
    answer = data.get("answer", "(No answer returned)")
    return True, answer


def set_example_question(text: str):
    st.session_state.question_box = text


# -----------------------------
# Page header
# -----------------------------
st.title("📘 PDF Catalog Assistant")
st.write(
    "Upload a product catalog, guide, or price list PDF and ask sales, technical, "
    "product recommendation, and quote-style questions."
)

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.header("API Settings")

    api_key = st.text_input(
        "API Key",
        type="password",
        placeholder="pdi_live_..."
    )

    model = st.selectbox(
        "Model",
        ["gpt-4o-mini", "gpt-4o"],
        index=0
    )

    st.markdown("---")
    st.header("Assistant Behavior")

    system_prompt = st.text_area(
        "System Prompt",
        value=DEFAULT_SYSTEM_PROMPT,
        height=320
    )

    st.caption(
        "Customize this prompt to turn the assistant into a sales engineer, "
        "technical rep, customer service agent, quoting assistant, or industry-specific advisor."
    )

# -----------------------------
# Upload section
# -----------------------------
st.subheader("1) Upload a catalog PDF")

uploaded_file = st.file_uploader(
    "Choose a PDF",
    type=["pdf"],
    help="Use a catalog, guide, manual, price list, or combined product document."
)

col_upload_1, col_upload_2 = st.columns([1, 4])

with col_upload_1:
    upload_clicked = st.button("Upload PDF", use_container_width=True)

with col_upload_2:
    if st.session_state.pdf_id:
        st.success(f"Current PDF: {st.session_state.uploaded_filename}")

if upload_clicked:
    if not api_key:
        st.error("Enter your API key first.")
    elif not uploaded_file:
        st.error("Choose a PDF file first.")
    else:
        try:
            with st.spinner("Uploading PDF..."):
                ok, message = upload_pdf(api_key, uploaded_file)

            if ok:
                st.success(message)
            else:
                st.error(message)

        except Exception as e:
            st.error(f"Upload error: {e}")

# -----------------------------
# Example prompts
# -----------------------------
st.subheader("2) Example questions")

example_prompts = [
    "Which product best fits this application?",
    "Recommend a complete solution based on this catalog.",
    "What companion products should be included with this item?",
    "Prepare a quote-style recommendation for this customer need.",
    "Compare two possible product options from the catalog.",
    "What accessories or related items should be offered with this product?",
    "Which option is the best value based on the document?",
    "Summarize the best package for a new customer."
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
                    args=(example_prompts[idx],)
                )

# -----------------------------
# Ask section
# -----------------------------
st.subheader("3) Ask the assistant")

question = st.text_area(
    "Your question",
    key="question_box",
    height=120,
    placeholder="Example: Recommend a complete solution and include any companion products or accessories that should be offered."
)

col_ask_1, col_ask_2 = st.columns([1, 5])

with col_ask_1:
    ask_clicked = st.button("Ask", use_container_width=True)

if ask_clicked:
    if not api_key:
        st.error("Enter your API key first.")
    elif not st.session_state.pdf_id:
        st.error("Upload a PDF first.")
    elif not question.strip():
        st.error("Enter a question.")
    else:
        try:
            with st.spinner("Thinking..."):
                ok, result = ask_pdf_assistant(
                    api_key=api_key,
                    model=model,
                    system_prompt=system_prompt,
                    question=question
                )

            if ok:
                st.session_state.chat_history.append({
                    "question": question.strip(),
                    "answer": result
                })

                # clear input safely BEFORE rerun
                st.session_state["question_box"] = ""

    st.rerun()
            else:
                st.error(result)

        except Exception as e:
            st.error(f"Chat error: {e}")

# -----------------------------
# Conversation display
# -----------------------------
if st.session_state.chat_history:
    st.subheader("Conversation")

    for item in reversed(st.session_state.chat_history):
        with st.container():
            st.markdown(f"**Question:** {item['question']}")
            st.markdown("**Answer:**")
            st.write(item["answer"])
            st.markdown("---")

# -----------------------------
# Customization notes
# -----------------------------
with st.expander("How to customize this example"):
    st.markdown(
        """
**This app is intentionally generic.**  
You can adapt it for almost any catalog-driven workflow by changing the **System Prompt**.

Examples:
- **Sales Engineer Assistant** — recommend best-fit products and complete packages
- **Technical Rep Assistant** — explain differences, compatibility, and accessories
- **Customer Service Agent** — answer product and support questions
- **Quoting Assistant** — guide answers toward quote-style package summaries
- **Distributor Support Assistant** — recommend related items and upsell bundles

You can use the same code with many different product categories:
- pumps
- HVAC equipment
- electrical products
- lab equipment
- industrial components
- replacement parts
- service kits

For example, in a pump catalog you might customize the prompt so the assistant recommends:
- the pump
- required valves
- check valve
- filter/strainer assembly
- controls or accessories

That way the assistant helps guide the user toward a **complete package**, not just a single item.
"""
    )
