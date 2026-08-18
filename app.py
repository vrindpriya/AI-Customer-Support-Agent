import streamlit as st

from src.rag import load_knowledge_base, search_knowledge_base
from src.llm import generate_reply
from src.database import(create_database, save_conversation, get_conversations)

# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="AI Customer Support Agent",
    page_icon="🤖",
    layout="wide"
)

# Create database
create_database()

# Load knowledge base
documents = load_knowledge_base()
# -----------------------------
# Sidebar History
# -----------------------------

with st.sidebar:

    st.title("📜 History")

    history = get_conversations()

     # Live Metrics
    st.metric("Knowledge Docs", len(documents))
    st.metric("Approved Replies", len(history))

    st.write(f"{len(history)} Approved Replies")

    st.divider()

    for chat in history:

        with st.expander(chat[0][:35] + "..."):

            st.caption("Retrieved Document")
            st.write(chat[1])

            st.caption("Status")
            st.success(chat[3])

            st.caption("AI Reply")
            st.write(chat[2])

# -----------------------------
# Session State
# -----------------------------

if "draft_reply" not in st.session_state:
    st.session_state.draft_reply = ""

if "document" not in st.session_state:
    st.session_state.document = None

if "customer_email" not in st.session_state:
    st.session_state.customer_email = ""

# -----------------------------
# Title
# -----------------------------

st.title("🤖 AI Customer Support Agent")
st.header("Enterprise AI Customer Support Agent")

st.write("Generate professional customer support replies using AI.")

st.divider()

# -----------------------------
# Knowledge Base
# -----------------------------

st.subheader("📚 Knowledge Base")
st.write(f"Loaded {len(documents)} documents.")

for doc in documents:
    st.write(f"✅ {doc['filename']}")

# -----------------------------
# Customer Email
# -----------------------------

customer_email = st.text_area(
    "📧 Paste Customer Email",
    height=250,
    placeholder="Example:\n\nHi, I purchased Premium yesterday but my account is still locked."
)

# -----------------------------
# Generate Reply
# -----------------------------

if st.button("Generate Reply"):

    if customer_email.strip() == "":
        st.warning("Please enter a customer email.")

    else:
        # Search the knowledge base
        document = search_knowledge_base(customer_email)

        if document:
            # Save values in session state
            st.session_state.customer_email = customer_email
            st.session_state.document = document

            st.session_state.draft_reply = generate_reply(
                customer_email,
                document["content"]
            )

        else:
            st.warning("No relevant document found.")


# -----------------------------
# Display Results
# -----------------------------

if st.session_state.document:

    st.subheader("Customer Email")
    st.info(st.session_state.customer_email)

    st.subheader("📚 Most Relevant Document")
    st.success(st.session_state.document["filename"])

    with st.expander("View Retrieved Knowledge"):
        st.write(st.session_state.document["content"])

    st.subheader("🤖 AI Draft Reply")

    st.session_state.draft_reply = st.text_area(
        "Review & Edit Response",
        value=st.session_state.draft_reply,
        height=250
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Approve ✅"):

            save_conversation(
                st.session_state.customer_email,
                st.session_state.document["filename"],
                st.session_state.draft_reply,
                "Approved"
            )

            st.success("Reply approved and saved!")
            st.balloons()

    with col2:
        if st.button("Reject ❌"):
            st.session_state.draft_reply = ""
            st.session_state.document = None
            st.session_state.customer_email = ""
            st.warning("Draft discarded.")