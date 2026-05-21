import streamlit as st


def inspect_vectorstore(vectorstore):
  
  with st.sidebar.expander("ChromaDB Inspector", expanded=False):
    # Show document count
    try:
      doc_count = vectorstore._collection.count()
      st.success(f"{doc_count} documents stored in ChromaDB.")
    except Exception as e:
      st.error("Could not fetch document count.")
      st.code(str(e))

    # Input box for similarity query
    query = st.text_input("Test a query against ChromaDB")

    if query:
      try:
        results = vectorstore.similarity_search(query, k=3)
        if results:
          st.markdown("### Top Matching Chunks:")
          for i, doc in enumerate(results):
            content = getattr(doc, "page_content", str(doc))[:300]
            st.markdown(f"**Result {i + 1}:**\n\n{content}...")
            st.markdown("---")
        else:
          st.info("No matching chunks found.")
      except Exception as e:
        st.error("Error querying ChromaDB")
        st.code(str(e))
