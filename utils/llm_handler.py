from utils.config import GOOGLE_API_KEY

from langchain.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

from langchain_google_genai import ChatGoogleGenerativeAI


def get_llm_chain(model_provider, model, vectorstore):
  # Define prompt template with system and user message format
  prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer as detailed as possible using the context below. If unknown, say 'I don't know.'"),
    ("human", "Context:\n{context}\n\n\nQuestion:\n{input}")
  ])

  if not model:
    return None
    # raise ValueError("Model must be selected before initializing the LLM chain.")

  # Initialize LLM instance based on provider
  if model_provider == "groq":
    print(model, GROQ_API_KEY)
    llm = ChatGroq(model=model, api_key=GROQ_API_KEY)
  elif model_provider == "gemini":
    llm = ChatGoogleGenerativeAI(model=model, api_key=GOOGLE_API_KEY)
  else:
    return None
    # raise ValueError("Unsupported Model Provider")

  # Convert vectorstore into a retriever, pulling top 3 relevant chunks
  retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

  # Build the full RAG chain: retrieval + prompt + LLM
  chain = create_retrieval_chain(
    retriever,
    create_stuff_documents_chain(llm, prompt=prompt)
  )

  return chain
