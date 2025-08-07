## Script Descriptions and Core Functionality

This project features three main Python scripts that together implement a voice-enabled PDF Retrieval-Augmented Generation (RAG) pipeline. Here’s a detailed description of each script—their most important functions, and an explanation of how the system operates from data ingestion to interactive querying.

### 1. **populate_database.py**
**Purpose:**  
Processes and indexes PDF documents for retrieval by splitting text into semantic chunks, generating vector embeddings, and storing them in a ChromaDB vector database.

**Key Components:**
- **Arguments**:  
  - `--reset`: Optional. Resets/clears the database directory before re-population.

- **Functions:**
  - `main()`: Entry point.
    - Checks for the `--reset` flag to optionally clear the database.
    - Loads PDFs, splits them into chunks, computes embeddings, and adds only new chunks to the ChromaDB database.
  - `load_documents()`: Loads all PDF files from the `data/` directory using LangChain’s PDF loader.
  - `split_documents(documents)`: Uses `RecursiveCharacterTextSplitter` to break documents into text chunks (default: 800 characters, 80 overlap).
  - `calculate_chunk_ids(chunks)`: Assigns each chunk a unique deterministic ID (format: `source:page:chunk_index`), enabling deduplication and incremental updates.
  - `add_to_chroma(chunks)`: 
    - Initializes the ChromaDB vector store with the configured embedding function.
    - Checks for chunks not yet present in the database.
    - Adds only genuinely new chunks for efficiency.
  - `clear_database()`: Removes all files from the vector store directory to allow complete re-population.

**How it works:**  
Runs as a one-off data preparation utility. Place PDFs in the `data/` subdirectory, then execute the script to build or incrementally update the vector store that powers the search capabilities.

### 2. **query_data.py**
**Purpose:**  
Enables querying of the indexed PDF database using both text and voice. Delivers answers as text and/or spoken output, using Retrieval-Augmented Generation via LLM and TTS technology.

**Key Components:**
- **Arguments**:
  - `--voice`: Launches voice query mode.
  - `query_text`: (Positional) Query using text input.
  
- **Functions:**
  - `main()`: Orchestrates user interaction. Runs in either text or voice mode.
  - `query_rag(query_text)`:  
    - Fetches the ChromaDB with the proper embedding function.
    - Performs similarity search to get the most relevant chunks.
    - Composes a custom prompt with the chunks as retrieval context for the LLM.
    - Uses Ollama’s local model (`llama3.2`) for answer generation.
    - Returns the model’s response along with document source chunk IDs.
  - `speak_response(text)`: Uses `pyttsx3` for text-to-speech synthesis—selecting English voices if available.
  - `get_voice_input()`: Captures and transcribes a single user question using `RealtimeSTT` in “medium” recognition mode (English).

**How it works:**  
Run the script directly.  
- **Text mode:** `python query_data.py "your question"`—get spoken answer.
- **Voice mode:** `python query_data.py --voice`—speak your question, listen to the answer.  
All responses are retrieved from indexed PDF content.

### 3. **get_embedding_function.py**
**Purpose:**  
Centralizes vector embedding model configuration, making it easy to switch or standardize embedding providers.

**Key Component:**
- **Function:**
  - `get_embedding_function()`: Returns an instance of Ollama’s embedding model wrapper, using the `nomic-embed-text` model, configured for the RAG pipeline.

**How it works:**  
Used internally by both `populate_database.py` and `query_data.py` to ensure consistent embeddings for both indexing and querying.

## System Workflow Overview

1. **Ingestion/Indexing:**  
   - Place PDFs in the `data/` directory.
   - Run `populate_database.py` to generate and store chunked vector embeddings.

2. **Interactive Retrieval:**
   - Run `query_data.py` for user queries (either typed or spoken).
   - Script retrieves relevant PDF chunks via vector similarity, forms a context/QA prompt for an LLM, and returns/generated answers as speech and text.

## Most Important Functions – At a Glance

| Script                  | Key Function(s)             | What It Does                                                                        |
|-------------------------|-----------------------------|-------------------------------------------------------------------------------------|
| populate_database.py    | `main`, `split_documents`, `add_to_chroma`, `calculate_chunk_ids` | Reads, splits, embeds, ID-tags, and stores document chunks incrementally            |
| query_data.py           | `main`, `query_rag`, `get_voice_input`, `speak_response`          | Runs interactive QA pipeline: similarity search, LLM prompt, TTS answer             |
| get_embedding_function.py| `get_embedding_function`   | Returns standardized embedding model instance for retrieval pipeline                 |

This modular setup ensures efficient document indexing, robust retrieval, and seamless voice interaction—all essential for a user-friendly, locally-operated RAG solution for PDF search and Q&A.
