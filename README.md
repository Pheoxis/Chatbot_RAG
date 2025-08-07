Based on your three Python files, here's a comprehensive GitHub README for your RAG (Retrieval-Augmented Generation) system with voice capabilities:

```markdown
# PDF RAG System with Voice Integration

A Retrieval-Augmented Generation (RAG) system that allows you to query PDF documents using both text and voice input, with text-to-speech response capabilities. Built with LangChain, ChromaDB, and Ollama.

## Features

- 🔍 **PDF Document Processing**: Automatically load and process PDF documents from a directory
- 🧠 **Vector Database**: Store document embeddings using ChromaDB for efficient similarity search
- 🎤 **Voice Input**: Ask questions using speech-to-text functionality
- 🔊 **Text-to-Speech**: Get spoken responses to your queries
- 📝 **Text Input**: Traditional text-based querying
- 🔄 **Incremental Updates**: Add new documents without duplicating existing ones
- 🧹 **Database Management**: Reset/clear database functionality

## Prerequisites

- Python 3.8+
- Ollama installed and running
- Required Ollama models:
  - `llama3.2` (for text generation)
  - `nomic-embed-text` (for embeddings)

## Installation

1. Clone this repository:
```
git clone 
cd pdf-rag-voice-system
```

2. Install required dependencies:
```
pip install langchain langchain-community langchain-text-splitters chromadb pypdf pyttsx3 RealtimeSTT argparse
```

3. Install and start Ollama:
```
# Install Ollama (follow instructions at https://ollama.ai)
ollama pull llama3.2
ollama pull nomic-embed-text
```

## Project Structure

```
├── populate_database.py    # Database population and management
├── query_data.py          # Query interface with voice capabilities
├── get_embedding_function.py  # Embedding configuration
├── data/                  # Directory for PDF files
└── chroma/               # ChromaDB storage (auto-created)
```

## Usage

### 1. Populate the Database

Place your PDF files in the `data/` directory, then run:

```
# Initial population
python populate_database.py

# Reset database and repopulate
python populate_database.py --reset
```

### 2. Query the System

#### Text Input with Spoken Response:
```
python query_data.py "What is the main topic of the document?"
```

#### Voice Input:
```
python query_data.py --voice
```

## Configuration

### Document Processing
- **Chunk Size**: 800 characters
- **Chunk Overlap**: 80 characters
- **Similarity Search**: Top 3 most relevant chunks

### Voice Settings
- **STT Model**: Medium accuracy model
- **Language**: English
- **TTS**: Configurable voice selection with English preference
- **Speech Rate**: 150 WPM

### Embedding Model
The system uses Ollama's `nomic-embed-text` model for generating embeddings. You can modify this in `get_embedding_function.py`.

## File Descriptions

### `populate_database.py`
- Loads PDF documents from the `data/` directory
- Splits documents into chunks using RecursiveCharacterTextSplitter
- Stores embeddings in ChromaDB with unique chunk IDs
- Supports incremental updates (only adds new documents)

### `query_data.py`
- Provides text and voice query interfaces
- Performs similarity search against the vector database
- Uses Ollama's LLaMA 3.2 for response generation
- Includes text-to-speech functionality

### `get_embedding_function.py`
- Configures the embedding model (Ollama nomic-embed-text)
- Centralized embedding function for consistency

## Customization

### Change the LLM Model
Modify the model in `query_data.py`:
```
model = Ollama(model="your-preferred-model")
```

### Adjust Chunk Settings
Edit parameters in `populate_database.py`:
```
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # Increase for larger chunks
    chunk_overlap=100,  # Adjust overlap
    # ...
)
```

### Modify Voice Settings
Update voice parameters in `query_data.py`:
```
recorder = AudioToTextRecorder(
    model="large",  # Use larger STT model
    language="en",
    # ... other settings
)
```

## Troubleshooting

### Common Issues:
1. **Ollama not running**: Ensure Ollama is installed and the required models are pulled
2. **No microphone access**: Check system permissions for microphone usage
3. **TTS not working**: Verify pyttsx3 installation and system audio settings
4. **Database errors**: Try resetting with `--reset` flag

### Dependencies Issues:
If you encounter import errors, ensure all packages are installed:
```
pip install --upgrade langchain langchain-community chromadb
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Built with [LangChain](https://langchain.com/)
- Vector storage by [ChromaDB](https://www.trychroma.com/)
- LLM inference by [Ollama](https://ollama.ai)
- Voice processing with RealtimeSTT and pyttsx3
```

This README provides a comprehensive overview of your RAG system, including installation instructions, usage examples, and customization options. It's structured to help users quickly understand and implement your voice-enabled PDF querying system.
