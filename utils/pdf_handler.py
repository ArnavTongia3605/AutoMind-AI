from pypdf import PdfReader

from langchain.text_splitter import RecursiveCharacterTextSplitter


def get_pdf_text(uploaded_files):
  
  text = ""
  for file in uploaded_files:
    reader = PdfReader(file)
    for page in reader.pages:
      text += page.extract_text() or ""
  return text

def get_text_chunks(text):
  
  splitter = RecursiveCharacterTextSplitter(chunk_size=2500, chunk_overlap=250)
  return splitter.split_text(text)
