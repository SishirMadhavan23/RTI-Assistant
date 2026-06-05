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
    return pipeline(
        "text2text-generation",
        model="google/flan-t5-base"
    )


db = load_db()
generator = load_model()

# ---------------- HISTORY ----------------

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- INPUT ----------------

query = st.text_input("Ask your RTI Question", value=selected_question)

# ---------------- PROCESS QUERY ----------------
if query and (
    len(st.session_state.history) == 0 or st.session_state.history[-1]["question"] != query
):

    with st.spinner("AI is thinking..."):

        # Retrieve PDF chunks
        docs = db.similarity_search(query, k=3)

        context = "\n\n".join([doc.page_content for doc in docs])

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
            truncation=True,
        )

        generated = result[0]["generated_text"]

        # Remove prompt
        if prompt in generated:
            answer = generated.replace(prompt, "").strip()
        else:
            answer = generated.strip()

        # Remove tags
        if "Answer:" in answer:
            answer = answer.split("Answer:")[-1].strip()

        if "Question:" in answer:
            answer = answer.split("Question:")[0].strip()

        # Remove duplicate lines
        cleaned = []

        for line in answer.split("\n"):
            line = line.strip()

            if line and line not in cleaned and len(line) > 2:
                cleaned.append(line)

        answer = "\n".join(cleaned)

        if len(answer) < 10:
            answer = "This information is not clearly " "available in the provided RTI documents."

        # Save ONCE only
        st.session_state.history.append({"question": query, "answer": answer, "docs": docs})
# ---------------- DISPLAY CHAT ----------------
for idx, item in enumerate(st.session_state.history):

    st.markdown(
        f"""
        <div class='chat-user'>
        <b>You</b><br>
        {item['question']}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class='chat-ai'>
        <b>AI Assistant</b><br><br>
        {item['answer']}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Sources Used
    with st.expander("📄 Sources Used"):

        if "docs" in item:

            shown = []

            for i, doc in enumerate(item["docs"]):

                source = doc.metadata.get("source", "Unknown")

                if source not in shown:

                    shown.append(source)

                    st.write(f"📄 {os.path.basename(source)}")

                    try:
                        if os.path.exists(source):
                            with open(source, "rb") as file:
                                st.download_button(
                                    label=f"Download {os.path.basename(source)}",
                                    data=file.read(),
                                    file_name=os.path.basename(source),
                                    mime="application/pdf",
                                    key=f"pdf_{idx}_{i}",
                                )
                        else:
                            st.info(
                                f"Source document '{os.path.basename(source)}' is not available on the deployment server."
                            )

                    except Exception as e:
                        st.warning(f"Unable to open source file: {e}")

# NEXT QUESTION BUTTON
if st.button("Generate"):

    st.session_state.query = ""

    st.rerun()
# ---------------- DRAFT GENERATOR ----------------

# RTI DRAFT GENERATOR
st.subheader("RTI Draft Generator")

draft_issue = st.text_area("Describe your issue", height=120, key="draft_issue")

if st.button("Generate Draft"):

    if not draft_issue.strip():
        st.warning("Please describe your issue.")

    else:

        with st.spinner("Generating RTI application..."):

            draft_docs = db.similarity_search(draft_issue, k=3)

            draft_context = "\n\n".join([doc.page_content for doc in draft_docs])

            draft_prompt = f"""
You are an expert RTI legal assistant.

Use ONLY the provided RTI documents and the citizen's issue.

Generate a complete RTI application in proper Indian RTI letter format.

RTI Context:
{draft_context}

Citizen Issue:
{draft_issue}

Instructions:
- Start with "To,"
- Address the Public Information Officer (PIO)
- Include a clear Subject line
- Begin with "Respected Sir/Madam,"
- Mention the Right to Information Act, 2005
- Convert the citizen's issue into 5-8 numbered information requests
- Use formal government letter language
- End with:
  Yours faithfully,
  [Applicant Name]
  [Address]
  [Mobile Number]
  [Email]
  Date: __________
  Place: __________

Return ONLY the RTI application letter.
Do not provide explanations, notes, commentary, or any text outside the letter.

RTI Application:
"""

            draft_result = generator(
                draft_prompt,
                max_new_tokens=800,
                temperature=0.1,
                do_sample=False,
                repetition_penalty=1.2,
                truncation=True,
            )

            generated = draft_result[0]["generated_text"]

            draft = f"""
To,
The Public Information Officer (PIO)
[Concerned Department]

Subject: RTI Application regarding {draft_issue[:50]}

Respected Sir/Madam,

Under the Right to Information Act, 2005, I seek the following information regarding the issue described below:

Issue:
{draft_issue}

Information Requested:

1. Please provide all records related to the above issue.
2. Please provide the action taken report.
3. Please provide copies of relevant orders, notices, and correspondence.
4. Please provide details of the responsible officer/department.
5. Please provide the current status and expected resolution timeline.

I request that the information be provided within the period prescribed under the RTI Act, 2005.

Yours faithfully,

[Applicant Name]
[Address]
[Mobile Number]
[Email Address]

Date: __________
Place: __________
"""

            st.markdown("### Generated RTI Application")

            st.text_area("", value=draft, height=400, key="draft_output")

            st.download_button(
                label="Download Draft",
                data=draft,
                file_name="RTI_Application.txt",
                mime="text/plain",
            )
