import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from qdrant_client import QdrantClient

# Load environment variables
load_dotenv()

# --- Configuration ---
QDRANT_COLLECTION_NAME = "humanoid_robotics_book"
EMBEDDING_MODEL = "text-embedding-ada-002"
LLM_MODEL = "gpt-3.5-turbo"

# --- Initialize Clients ---
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

embeddings = OpenAIEmbeddings(
    model=EMBEDDING_MODEL,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

chat_llm = ChatOpenAI(
    model_name=LLM_MODEL,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.1
)

# --- FastAPI App ---
app = FastAPI(
    title="Humanoid Robotics Book RAG Chatbot",
    description="A chatbot that can answer questions about the humanoid robotics book.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models ---
class ChatRequest(BaseModel):
    query: str
    selected_text: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]

# --- RAG Logic ---
def perform_rag(query: str, selected_text: Optional[str]) -> ChatResponse:
    if selected_text:
        # Case 1: User has selected text. Use it as the only context.
        context = selected_text
        sources = ["User Selection"]
    else:
        # Case 2: No selected text. Retrieve context from Qdrant.
        query_embedding = embeddings.embed_query(query)
        
        search_results = qdrant_client.search(
            collection_name=QDRANT_COLLECTION_NAME,
            query_vector=query_embedding,
            limit=3  # Retrieve top 3 most relevant chunks
        )
        
        context_chunks = [result.payload['page_content'] for result in search_results]
        source_files = list(set([result.payload['source'] for result in search_results]))

        context = "\n\n---\n\n".join(context_chunks)
        sources = source_files

    # Create the prompt for the LLM
    prompt_template = f"""
    You are an expert assistant for the 'Humanoid Robotics' book. 
    Answer the user's question based *only* on the provided context.
    If the context doesn't contain the answer, say "I'm sorry, but I cannot answer that question based on the provided text."

    CONTEXT:
    ---
    {context}
    ---

    QUESTION: {query}
    
    ANSWER:
    """

    # Generate the answer
    response = chat_llm.predict(prompt_template)

    return ChatResponse(answer=response, sources=sources)

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        return perform_rag(request.query, request.selected_text)
    except Exception as e:
        print(f"Error during RAG process: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your request.")

@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG Chatbot API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
