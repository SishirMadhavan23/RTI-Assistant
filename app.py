import os

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import streamlit as st
from transformers import pipeline

# ---------------- PAGE CONFIG ----------------

st.set_page_config(page_title="RTI Assistant AI", page_icon="⚖️", layout="wide")

# ---------------- LOAD CSS ----------------

with open("assets/style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------- TITLE ----------------

st.markdown(
    """
    <div class='main-title'>
    RTI Assistant AI
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class='subtitle'>
    AI Civic Rights Assistant for India
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------- SIDEBAR ----------------

st.sidebar.title("⚡ RTI Assistant")

st.sidebar.markdown("### Suggested Questions")

questions = ["How to file RTI?", "What is RTI fee?", "Appeal process?", "RTI response time?"]

selected_question = ""

for q in questions:
    if st.sidebar.button(q):
        selected_question = q

st.sidebar.markdown("---")
st.sidebar.markdown("### Features")

st.sidebar.success("AI Answers")
st.sidebar.success("RTI Draft Generator")
st.sidebar.success("Sources Included")
st.sidebar.success("Citizen Friendly")

# ---------------- LOAD DATABASE ----------------


@st.cache_resource
def load_db():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vector_db = FAISS.load_local("vectorstore", embeddings, allow_dangerous_deserialization=True)

    return vector_db


# ---------------- LOAD MODEL ----------------


@st.cache_resource
def load_model():
    return pipeline("text-generation", model="gpt2")


db = load_db()
generator = load_model()

# ---------------- HISTORY ----------------

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- INPUT ----------------

query = st.text_input("Ask your RTI Question", value=selected_question)

# ---------------- PROCESS QUERY ----------------
if query and (
    len(st.session_state.history) == 0
    or st.session_state.history[-1]["question"] != query
):

    with st.spinner("AI is thinking..."):

        # Retrieve PDF chunks
        docs = db.similarity_search(query, k=3)

        context = "\n\n".join(
            [doc.page_content for doc in docs]
        )

        prompt = f"""
You are an RTI legal assistant.

Answer ONLY from the provided RTI documents.

Rules:
- Use only the provided context
- Give one complete answer
- Do not repeat
- Do not repeat question
- No random numbering
- No hallucinations
- If not found say:
"This information is not clearly available in the provided RTI documents."

Context:
{context}

Question:
{query}

Answer:
"""

        result = generator(
            prompt,
            max_new_tokens=10000,
            temperature=0.2,
            do_sample=False,
            repetition_penalty=1.2,
            truncation=True
        )

        generated = result[0]["generated_text"]

        # Remove prompt
        if prompt in generated:
            answer = generated.replace(
                prompt,
                ""
            ).strip()
        else:
            answer = generated.strip()

        # Remove tags
        if "Answer:" in answer:
            answer = answer.split(
                "Answer:"
            )[-1].strip()

        if "Question:" in answer:
            answer = answer.split(
                "Question:"
            )[0].strip()

        # Remove duplicate lines
        cleaned = []

        for line in answer.split("\n"):
            line = line.strip()

            if (
                line
                and line not in cleaned
                and len(line) > 2
            ):
                cleaned.append(line)

        answer = "\n".join(cleaned)

        if len(answer) < 10:
            answer = (
                "This information is not clearly "
                "available in the provided RTI documents."
            )

        # Save ONCE only
        st.session_state.history.append(
            {
                "question": query,
                "answer": answer,
                "docs": docs
            }
        )
# ---------------- DISPLAY CHAT ----------------
for idx, item in enumerate(st.session_state.history):

    st.markdown(
        f"""
        <div class='chat-user'>
        <b>You</b><br>
        {item['question']}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class='chat-ai'>
        <b>AI Assistant</b><br><br>
        {item['answer']}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Sources Used
    with st.expander("📄 Sources Used"):

        if "docs" in item:

            shown = []

            for i, doc in enumerate(item["docs"]):

                source = doc.metadata.get(
                    "source",
                    "Unknown"
                )

                if source not in shown:

                    shown.append(source)

                    st.write(
                        f"📄 {os.path.basename(source)}"
                    )

                    with open(source, "rb") as file:

                        st.download_button(
                            label=f"Open {os.path.basename(source)}",
                            data=file,
                            file_name=os.path.basename(source),
                            mime="application/pdf",
                            key=f"pdf_{idx}_{i}"
                        )

# NEXT QUESTION BUTTON
if st.button("Generate"):

    st.session_state.query = ""

    st.rerun()
# ---------------- DRAFT GENERATOR ----------------

# RTI DRAFT GENERATOR
st.subheader("RTI Draft Generator")

draft_issue = st.text_area(
    "Describe your issue",
    height=120,
    key="draft_issue"
)

if st.button("Generate Draft"):

    if not draft_issue.strip():
        st.warning("Please describe your issue.")

    else:

        with st.spinner("Generating RTI application..."):

            draft_docs = db.similarity_search(
                draft_issue,
                k=3
            )

            draft_context = "\n\n".join(
                [doc.page_content for doc in draft_docs]
            )

            draft_prompt = f"""
You are an expert RTI legal assistant.

Use ONLY the provided RTI documents.

Generate a formal RTI application.

RTI Context:
{draft_context}

Citizen Issue:
{draft_issue}

RTI Application:
"""

            draft_result = generator(
                draft_prompt,
                max_new_tokens=1200,
                temperature=0.2,
                do_sample=False,
                repetition_penalty=1.2,
                truncation=True
            )

            generated = draft_result[0]["generated_text"]

            draft = generated.replace(
                draft_prompt,
                ""
            ).strip()

            st.markdown(
                "### Generated RTI Application"
            )

            st.text_area(
                "",
                value=draft,
                height=400,
                key="draft_output"
            )

            st.download_button(
                label="Download Draft",
                data=draft,
                file_name="RTI_Application.txt",
                mime="text/plain"
            )
