import streamlit as st

from utils.chat_handler import (
  setup_session_state,
  render_chat_history,
  render_download_chat_history,
  handle_user_input,
  render_uploaded_files_expander
)
from utils.sidebar_handler import (
  render_model_selector,
  sidebar_file_upload,
  sidebar_provider_change_check,
  sidebar_utilities
)
from utils.developer_mode import inspect_vectorstore
from utils.llm_handler import get_llm_chain


def main():
  st.set_page_config(page_title="AutoMind AI", layout="centered")

  st.markdown("""
  <style>
  #MainMenu {visibility: hidden;}
  header {visibility: hidden;}
  footer {visibility: hidden;}

  .block-container {
    padding-top: 2rem;
    padding-left: 1rem;
    padding-right: 1rem;
    max-width: 900px;
  }

  h1 {
    font-size: 3rem !important;
    font-weight: 800 !important;
  }

  @media (max-width: 768px) {
    .block-container {
      padding-top: 1.5rem;
      padding-left: 1rem;
      padding-right: 1rem;
    }

    h1 {
      font-size: 2.3rem !important;
    }
  }
  </style>
  """, unsafe_allow_html=True)

  st.markdown(
    """
    <h1 style='text-align: center; margin-bottom: 0.2rem;'>
        AutoMind AI
    </h1>
    """,
    unsafe_allow_html=True
  )

  st.markdown(
      """
      <p style='text-align: center; color: gray; font-size: 18px;'>
          Chat With Your Uploaded Vehicle Manuals Regarding Any Query
      </p>
      """,
      unsafe_allow_html=True
  )

  setup_session_state()

  with st.expander("Configuration", expanded=True):
    model_provider, model = render_model_selector()
    sidebar_file_upload(model_provider)
    sidebar_provider_change_check(model_provider, model)

  with st.expander("Utilities", expanded=False):
    sidebar_utilities()

  if not st.session_state.get(f"uploaded_files_{st.session_state.uploader_key}", []):
    st.info("Please Upload Vehicle Manuals and Ask Questions About Vehicle Manuals.")

  if st.session_state.get("unsubmitted_files", False):
    st.warning("New PDFs uploaded. Please submit before chatting.")

  if st.session_state.get("vector_store", None) and st.session_state.get("pdf_files", []):
    render_uploaded_files_expander()

  if st.session_state.get("chat_history", []):
    render_chat_history()

  if st.session_state.get("vector_store"):
    handle_user_input(
      model_provider,
      model,
      get_llm_chain(model_provider, model, st.session_state.get("vector_store"))
    )

  if st.session_state.vector_store:
    inspect_vectorstore(st.session_state.vector_store)


if __name__ == "__main__":
  main()