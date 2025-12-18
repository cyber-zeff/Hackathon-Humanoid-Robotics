# Humanoid Robotics Book RAG Chatbot

This directory contains the complete backend and data ingestion pipeline for the RAG (Retrieval-Augmented Generation) chatbot embedded in the Docusaurus book.

## 1. Overview

The chatbot is built with the following technologies:
- **Backend:** FastAPI
- **AI/LLM:** OpenAI
- **Vector Database:** Qdrant Cloud
- **Data Store:** Neon Serverless Postgres (Note: Currently used for configuration, can be extended for chat history)
- **Frontend:** React (via Docusaurus)

The workflow is as follows:
1.  **Ingestion:** A Python script (`ingest.py`) reads all markdown files from the `../docs` directory, splits them into chunks, generates embeddings using OpenAI's API, and stores them in a Qdrant collection.
2.  **Serving:** A FastAPI server (`main.py`) exposes a `/chat` endpoint.
3.  **Retrieval & Generation:** When the user asks a question, the backend retrieves the most relevant text chunks from Qdrant and uses them as context for an OpenAI language model to generate an answer.

## 2. Prerequisites

Before you begin, you will need accounts for the following services:

- **OpenAI:** To get an API key for generating embeddings and answers.
- **Qdrant Cloud:** A free-tier account is sufficient. You will need the cluster URL and an API key.
- **Neon:** A free-tier serverless Postgres database. You'll need the database connection URL.
- **Node.js:** Version 20.0 or higher, installed on your machine.
- **Python:** Version 3.8 or higher, installed on your machine.

## 3. Setup Instructions

### Step 1: Configure Environment Variables

1.  Navigate to the `rag-chatbot` directory.
2.  Create a copy of the `.env.example` file and name it `.env`.
3.  Open the `.env` file and fill in the values you obtained from the services in the "Prerequisites" step:

    ```env
    # OpenAI: Find this in your OpenAI account settings
    OPENAI_API_KEY="sk-..."

    # Qdrant Cloud: Create a new cluster and find the URL and create an API key
    QDRANT_URL="https://your-qdrant-cluster-url.qdrant.tech:6333"
    QDRANT_API_KEY="..."

    # Neon: Create a new project and find the connection string in the "Connection Details" widget
    NEON_DATABASE_URL="postgresql://user:password@host:port/dbname?sslmode=require"
    ```

### Step 2: Install Dependencies

You need to install both Python and Node.js dependencies.

1.  **Python Dependencies (for the backend):**
    Open a terminal in the `rag-chatbot` directory and run:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Node.js Dependencies (for the Docusaurus frontend):**
    Open a terminal in the **root directory** of the project (the one containing `package.json`) and run:
    ```bash
    npm install
    ```

## 4. Running the Application

You will need to run three separate processes in three different terminals.

### Terminal 1: Run the Data Ingestion

**This only needs to be done once**, or whenever you make significant changes to the content of the book in the `docs` directory.

1.  Open a terminal in the `rag-chatbot` directory.
2.  Run the ingestion script:
    ```bash
    python ingest.py
    ```
    This will process all the `.md` and `.mdx` files and load them into your Qdrant database. Wait for it to complete.

### Terminal 2: Run the FastAPI Backend

1.  Open a second terminal in the `rag-chatbot` directory.
2.  Start the backend server:
    ```bash
    uvicorn main:app --reload
    ```
    This will start the server on `http://localhost:8000`. You should see a message like "Application startup complete."

### Terminal 3: Run the Docusaurus Frontend

1.  Open a third terminal in the **root directory** of the project.
2.  Start the Docusaurus development server:
    ```bash
    npm run start
    ```
    This will open your book in a web browser, usually at `http://localhost:3000`.

## 5. Using the Chatbot

Once all three processes are running, open your browser to `http://localhost:3000`. You should see a chat icon in the bottom-right corner. Click it to open the chatbot and ask questions about your book!

You can also select any text on the page, and the chatbot will automatically open, allowing you to ask a question specifically about that selection.
