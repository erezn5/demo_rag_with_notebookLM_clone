import streamlit as st
import tempfile
from config import settings
from core import file_handler, rag_pipeline, audio_pipeline, web_scraper

# 1. Init Settings
settings.init()

# 2. Page Setup
st.set_page_config(page_title="NotebookLLM Clone", layout="wide")
st.title("📚 NotebookLLM Clone (RAG)")

# 3. Sidebar
with st.sidebar:
    st.header("Source Material")
    tab1, tab2 = st.tabs(["📄 Upload PDF", "🌐 URL Scraper"])

    uploaded_file = None
    url_input = None
    process_url_clicked = False

    with tab1:
        uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

    with tab2:
        url_input = st.text_input("Enter Company Website URL", placeholder="https://openai.com/about")
        process_url_clicked = st.button("Scrape & Process")

# 4. Main App Logic

# A. Handle File Upload (Priority 1)
if uploaded_file is not None:
    # Check if this is a new file or the same one
    if "current_source" not in st.session_state or st.session_state.current_source != uploaded_file.name:
        with st.spinner("Processing PDF..."):
            file_path = file_handler.save_uploaded_file(uploaded_file)
            docs, splits = rag_pipeline.load_and_split_pdf(file_path)

            # Save to Session State
            st.session_state.rag_chain = rag_pipeline.create_rag_chain(splits)
            st.session_state.docs = docs
            st.session_state.current_source = uploaded_file.name
            st.success("PDF Processed!")

# B. Handle URL Scraper (Priority 2)
# We check if the button was clicked OR if we already scraped this specific URL
elif url_input and (process_url_clicked or st.session_state.get("current_source") == url_input):

    # Only scrape if we haven't done this URL yet
    if "current_source" not in st.session_state or st.session_state.current_source != url_input:
        with st.spinner(f"Scraping {url_input}..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                scrape_path = tmp.name

            success = web_scraper.scrape_url_to_pdf(url_input, scrape_path)

            if success:
                docs, splits = rag_pipeline.load_and_split_pdf(scrape_path)

                # Save to Session State
                st.session_state.rag_chain = rag_pipeline.create_rag_chain(splits)
                st.session_state.docs = docs
                st.session_state.current_source = url_input
                st.success("Website scraped and processed!")
            else:
                st.error("Failed to scrape URL.")

# 5. Render Chat Interface (If Data Exists)
# We check if 'rag_chain' exists in session state. If yes, we show the chat.
if "rag_chain" in st.session_state:

    # --- AUDIO OVERVIEW SIDEBAR ---
    with st.sidebar:
        st.markdown("---")
        st.subheader("🎧 Audio Overview")
        if st.button("Generate Audio Briefing"):
            with st.spinner("Generating Audio..."):
                try:
                    audio_path = audio_pipeline.generate_audio_overview(st.session_state.docs)
                    st.audio(audio_path)
                except Exception as e:
                    st.error(f"Error generating audio: {e}")

    # --- CHAT UI ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_input := st.chat_input("Ask about your document..."):
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.rag_chain.invoke({"input": user_input})
                answer = response['answer']
                st.markdown(answer)

                with st.expander("Sources"):
                    for i, doc in enumerate(response['context']):
                        st.markdown(f"**Source {i + 1}:** {doc.page_content[:200]}...")

        st.session_state.messages.append({"role": "assistant", "content": answer})

else:
    # Initial State Hint
    st.info("Please upload a PDF or scrape a URL to begin.")