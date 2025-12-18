import os
import glob
from typing import List
from dotenv import load_dotenv
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from qdrant_client import QdrantClient, models

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
DOCS_PATH = "../docs"
QDRANT_COLLECTION_NAME = "humanoid_robotics_book"
EMBEDDING_MODEL = "text-embedding-ada-002"

# --- Qdrant Client Initialization ---
# Ensure QDRANT_URL and QDRANT_API_KEY are set in your .env file
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

# --- OpenAI Embeddings Initialization ---
# Ensure OPENAI_API_KEY is set in your .env file
embeddings = OpenAIEmbeddings(
    model=EMBEDDING_MODEL,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

def load_markdown_documents(path: str) -> List[Document]:
    """Loads all markdown files from the specified path."""
    all_files = glob.glob(os.path.join(path, "**/*.md"), recursive=True)
    all_files.extend(glob.glob(os.path.join(path, "**/*.mdx"), recursive=True))
    
    documents = []
    for file_path in all_files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        # Create a LangChain Document object
        # The page_content is the text, and metadata contains the source
        doc = Document(page_content=content, metadata={"source": file_path})
        documents.append(doc)
    print(f"Loaded {len(documents)} documents from {path}")
    return documents

def split_documents(documents: List[Document]) -> List[Document]:
    """Splits documents into smaller chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""],
    )
    split_docs = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(split_docs)} chunks.")
    return split_docs

def create_and_store_embeddings(documents: List[Document]):
    """Creates embeddings for documents and stores them in Qdrant."""
    texts = [doc.page_content for doc in documents]
    metadatas = [doc.metadata for doc in documents]

    print("Creating embeddings for document chunks...")
    # This will make a call to OpenAI's API to get the embeddings
    vectors = embeddings.embed_documents(texts)
    print(f"Successfully created {len(vectors)} embeddings.")

    # Before uploading, we need to ensure the collection exists in Qdrant
    vector_size = len(vectors[0])
    qdrant_client.recreate_collection(
        collection_name=QDRANT_COLLECTION_NAME,
        vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
    )
    print(f"Qdrant collection '{QDRANT_COLLECTION_NAME}' created or recreated.")

    print("Uploading vectors and payloads to Qdrant...")
    qdrant_client.upsert(
        collection_name=QDRANT_COLLECTION_NAME,
        points=models.Batch(
            # The id for each point can be a simple counter
            ids=[i for i in range(len(texts))],
            # The vector is the embedding we created
            vectors=vectors,
            # The payload is the original text and its metadata (source)
            payloads=metadatas
        ),
        wait=True, # Wait for the upload to complete
    )
    print("Upload to Qdrant complete.")

def main():
    """Main function to run the ingestion process."""
    print("Starting data ingestion process...")
    documents = load_markdown_documents(DOCS_PATH)
    chunks = split_documents(documents)
    create_and_store_embeddings(chunks)
    print("Data ingestion process finished successfully!")

if __name__ == "__main__":
    main()
