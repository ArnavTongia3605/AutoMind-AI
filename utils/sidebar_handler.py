import streamlit as st

from utils.config import MODEL_OPTIONS
from utils.vectorstore_handler import get_or_create_vectorstore


def render_model_selector():
  
  model_provider = st.selectbox(
    "Model Provider",
    options=list(MODEL_OPTIONS.keys()),
    index=None,
    placeholder="Select a model provider",
    key="model_provider",
  )

  models = MODEL_OPTIONS.get(model_provider, {}).get("models", [])
  model = st.selectbox(
    "Select a model",
    options=models,
    index=None,
    placeholder="Select a model",
    disabled=(not model_provider),
    key="model",
  )

  return model_provider.lower() if model_provider else "", model

def render_upload_files_button():
  
  uploaded_files = st.file_uploader(
    "Upload Your Documents",
    type=["pdf"],
    accept_multiple_files=True,
    disabled=(not st.session_state.get("model")),
    key=f"uploaded_files_{st.session_state.uploader_key}"
  )

  if uploaded_files and uploaded_files != st.session_state.get("pdf_files"):
    st.session_state.update(unsubmitted_files=True)

  submitted = st.button(
    "Submit",
    disabled=(not st.session_state.get("model"))
  )

  return uploaded_files, submitted

def sidebar_file_upload(model_provider):
  
  uploaded_files, submitted = render_upload_files_button()

  if submitted:
    if uploaded_files:
      with st.spinner("Processing PDFs..."):
        try:
          vector_store = get_or_create_vectorstore(uploaded_files, model_provider)
        except Exception as e:
          st.error(f"Error: {str(e)}")
          return

        st.session_state.update(
          vector_store=vector_store,
          pdf_files=uploaded_files,
          unsubmitted_files=False
        )
        st.toast("PDFs processed successfully!", icon="✅")
    else:
      st.warning("No files uploaded.")

  return uploaded_files, submitted


def sidebar_provider_change_check(model_provider, model):
  
  if model_provider != st.session_state.get("last_provider") and model:
    st.session_state.update(last_provider=model_provider)
    if st.session_state.get("pdf_files"):
      with st.spinner(f"Reprocessing PDFs with {model_provider}..."):
        try:
          vector_store = get_or_create_vectorstore(st.session_state.get("pdf_files"), model_provider)
        except Exception as e:
          st.error(f"Error: {str(e)}")
          return

        st.session_state.update(vector_store=vector_store)
        st.toast("PDFs reprocessed successfully!", icon="🔁")

def sidebar_utilities():
  
  with st.expander("Utilities", expanded=False):
    col1, col2, col3 = st.columns(3)

    if col1.button("Reset"):
      st.session_state.clear()
      st.session_state["model_provider"] = None
      st.rerun()

    if col2.button("Clear Chat"):
      st.session_state.chat_history = []
      st.session_state.update(pdf_files=None, vector_store=None)
      st.session_state.uploader_key += 1
      st.toast("Chat and PDF cleared.", icon="🧼")
      st.rerun()

    if col3.button("Undo") and st.session_state.get("chat_history"):
      st.session_state.chat_history.pop()
      st.toast("Last message removed.", icon="↩️")
      st.rerun()
