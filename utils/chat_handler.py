import streamlit as st

from datetime import datetime


def setup_session_state():
  
  for key, default in {
    "chat_history": [],             # Stores tuples of (question, answer, provider, model, pdfs, timestamp)
    "vector_store": None,           # Stores the vector store instance for PDF embeddings
    "pdf_files": [],                # Currently submitted PDF files
    "last_provider": None,          # Tracks last selected provider for dynamic reloading
    "unsubmitted_files": False,     # Tracks whether new files were uploaded but not submitted
    "uploader_key": 0               # Used to reset file_uploader widget
  }.items():
    if key not in st.session_state:
      st.session_state[key] = default

def render_chat_history():
  
  for q, a, *_ in st.session_state.get("chat_history", []):
    with st.chat_message("user"):
      st.markdown(q)
    with st.chat_message("ai"):
      st.markdown(a)

def handle_user_input(model_provider, model, chain):
  
  # Disable question input if unsubmitted files or no files uploaded
  disable_question_input = (
    st.session_state.get("unsubmitted_files", False) or
    not st.session_state.get(f"uploaded_files_{st.session_state.uploader_key}", []) or
    not chain
  )

  question = st.chat_input(
    "Ask Your Question from the Uploaded Files",
    disabled=disable_question_input
  )

  if not question:
    return

  with st.chat_message("user"):
    st.markdown(question)
  with st.chat_message("ai"):
    with st.spinner("Thinking..."):
      try:
        output = chain.invoke({"input": question})["answer"]
        st.markdown(output)
        pdf_names = [f.name for f in st.session_state.get("pdf_files")]
        st.session_state.chat_history.append((question, output, model_provider, model, pdf_names, datetime.now()))
      except Exception as e:
        st.error(f"Error: {str(e)}")

def render_uploaded_files_expander():
  
  uploaded_files = st.session_state.get(f"uploaded_files_{st.session_state.uploader_key}", [])
  if uploaded_files and not st.session_state.get("unsubmitted_files"):
    with st.expander("📎 Uploaded Files:"):
      for f in uploaded_files:
        st.markdown(f"- {f.name}")
